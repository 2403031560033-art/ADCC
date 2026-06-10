from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
import asyncio
import random

from backend.db.database import get_db, SessionLocal
from backend.db.models import Zone
from backend.services.simulation_engine import load_scenario
from backend.agents.graph import app as adcc_graph
from backend.services.socket_manager import (
    emit_agent_update, emit_timeline_event,
    emit_state_update, emit_metrics_update, sio
)

async def emit_simulation_complete():
    await sio.emit('simulation_complete', {})

router = APIRouter(prefix="/api/disaster", tags=["disaster"])

# All available scenarios: name → emoji + display label
SCENARIOS = {
    "operation_brahmaputra":     {"label": "Operation Brahmaputra",    "disaster_type": "flood",      "region": "Assam",             "emoji": "🌊"},
    "operation_himalayan_quake": {"label": "Operation Himalayan Quake","disaster_type": "earthquake", "region": "Uttarakhand",       "emoji": "🌍"},
    "operation_sikkim_slide":    {"label": "Operation Sikkim Slide",   "disaster_type": "landslide",  "region": "Sikkim",            "emoji": "⛰️"},
    "operation_cyclone_amphan":  {"label": "Operation Cyclone Amphan", "disaster_type": "cyclone",    "region": "Odisha",            "emoji": "🌀"},
    "operation_white_death":     {"label": "Operation White Death",    "disaster_type": "avalanche",  "region": "Himachal Pradesh",  "emoji": "❄️"},
}

class CreateDisasterRequest(BaseModel):
    scenario: Optional[str] = None  # if None, a random one is selected

import logging
logger = logging.getLogger("uvicorn.error")

# ──────────────────────────────────────────────────────────
# Global simulation state — only ONE simulation at a time
# ──────────────────────────────────────────────────────────
_current_simulation_task: Optional[asyncio.Task] = None
_cancel_event = asyncio.Event()   # set → running sim should stop


async def run_simulation(scenario_info: dict, disaster_id: str, sim_id: str):
    """
    Executes the agent graph step-by-step and streams events over Socket.IO.
    Checks `_cancel_event` before every node so a new trigger kills this run cleanly.
    """
    global _cancel_event
    disaster_type = scenario_info["disaster_type"]
    region        = scenario_info["region"]

    try:
        logger.warning(f"[{sim_id}] Simulation START  disaster={disaster_id}")
        await asyncio.sleep(0.8)  # brief pause so UI can receive reset event first

        # Abort immediately if already cancelled
        if _cancel_event.is_set():
            logger.warning(f"[{sim_id}] Cancelled before loading zones.")
            return

        db = SessionLocal()
        try:
            zones = [
                {"zone_id": z.zone_id, "name": z.name, "lat": z.lat, "lon": z.lon,
                 "severity": z.severity, "population": z.population,
                 "status": z.status, "road_accessible": z.road_accessible}
                for z in db.query(Zone).filter(Zone.disaster_id == disaster_id).all()
            ]
            logger.warning(f"[{sim_id}] Loaded {len(zones)} zones for disaster {disaster_id}.")
        finally:
            db.close()

        if _cancel_event.is_set():
            logger.warning(f"[{sim_id}] Cancelled after DB load.")
            return

        initial_state = {
            "disaster_id":   disaster_id,
            "disaster_type": disaster_type,
            "region":        region,
            "triggered_at":  "2025-01-01T10:00:00Z",
            "zones":          zones,
            "resources":      [],
            "routes":         [],
            "priority_queue": [],
            "drone_assignments": [],
            "medical_actions":   [],
            "agent_decisions":   [],
            "timeline_events":   [],
            "final_plan":        {},
            "response_time_reduction": 0.0,
            "delivery_efficiency":     0.0,
            "supplies_delivered":      0.0,
            "lives_impacted":          0,
        }

        await emit_state_update({"zones": zones})

        async for output in adcc_graph.astream(initial_state):
            # ── cancellation check before processing each node ──
            if _cancel_event.is_set():
                logger.warning(f"[{sim_id}] Cancelled mid-graph.")
                return

            for node_name, state_update in output.items():
                logger.warning(f"[{sim_id}] Node {node_name} done.")

                if "agent_decisions" in state_update:
                    for d in state_update["agent_decisions"]:
                        await emit_agent_update(d["agent"], d["action"], d["reasoning"])

                if "timeline_events" in state_update:
                    for ev in state_update["timeline_events"]:
                        await emit_timeline_event(ev)

                if "zones" in state_update:
                    await emit_state_update({"zones": state_update["zones"]})

                if node_name == "coordinator_node":
                    metrics = {
                        "response_time_reduction": state_update.get("response_time_reduction", 0),
                        "delivery_efficiency":     state_update.get("delivery_efficiency", 0),
                        "supplies_delivered":      state_update.get("supplies_delivered", 0),
                        "lives_impacted":          state_update.get("lives_impacted", 0),
                    }
                    logger.warning(f"[{sim_id}] Emitting metrics: {metrics}")
                    await emit_metrics_update(metrics)

            # Pacing delay — also allows cancellation between nodes
            await asyncio.sleep(2)
            if _cancel_event.is_set():
                logger.warning(f"[{sim_id}] Cancelled during sleep.")
                return

        logger.warning(f"[{sim_id}] Simulation COMPLETE.")
        await emit_simulation_complete()

    except asyncio.CancelledError:
        logger.warning(f"[{sim_id}] Task was CancelledError.")
        await emit_simulation_complete()
    except Exception as e:
        import traceback
        logger.error(traceback.format_exc())
        logger.error(f"[{sim_id}] SIMULATION ERROR: {e}")
        await emit_simulation_complete()


@router.post("/create")
async def create_disaster(
    request: CreateDisasterRequest,
    db: Session = Depends(get_db)
):
    global _current_simulation_task, _cancel_event

    # ── 1. Pick a random (or requested) scenario ──
    scenario_key  = (
        request.scenario
        if request.scenario and request.scenario in SCENARIOS
        else random.choice(list(SCENARIOS.keys()))
    )
    scenario_meta = SCENARIOS[scenario_key]

    # ── 2. Cancel any running simulation ──
    if _current_simulation_task and not _current_simulation_task.done():
        logger.warning("Cancelling previous simulation…")
        _cancel_event.set()                        # signal the old task to stop
        _current_simulation_task.cancel()          # hard cancel
        try:
            await asyncio.wait_for(_current_simulation_task, timeout=3)
        except (asyncio.CancelledError, asyncio.TimeoutError):
            pass
        logger.warning("Previous simulation cancelled.")

    # ── 3. Emit reset event so frontend clears ALL old state ──
    await sio.emit("simulation_reset", {
        "label":         scenario_meta["label"],
        "disaster_type": scenario_meta["disaster_type"],
        "region":        scenario_meta["region"],
        "emoji":         scenario_meta["emoji"],
    })

    # ── 4. Seed fresh data ──
    _cancel_event = asyncio.Event()   # fresh event for the new sim
    result      = await load_scenario(scenario_key, db)
    disaster_id = result["disaster_id"]

    # ── 5. Start new simulation as a proper asyncio Task ──
    sim_id = disaster_id[:8]
    loop   = asyncio.get_event_loop()
    _current_simulation_task = loop.create_task(
        run_simulation(scenario_meta, disaster_id, sim_id)
    )

    return {
        "disaster_id":    disaster_id,
        "disaster_type":  scenario_meta["disaster_type"],
        "region":         scenario_meta["region"],
        "scenario":       scenario_key,
        "label":          scenario_meta["label"],
        "emoji":          scenario_meta["emoji"],
        "triggered_at":   "2025-01-01T10:00:00Z",
        "zones_initialized": result["total_zones"],
        "agents_activated":  ["coordinator", "route", "resource", "medical", "drone"],
        "status":         "running",
    }


@router.get("/scenarios")
async def list_scenarios():
    return [{"key": k, **v} for k, v in SCENARIOS.items()]


@router.get("/{disaster_id}")
async def get_disaster(disaster_id: str):
    return {
        "disaster_id":   disaster_id,
        "status":        "running",
    }
