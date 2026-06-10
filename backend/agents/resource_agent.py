from datetime import datetime
import uuid
from backend.agents.state import ADCCState, AgentDecision, TimelineEvent
from backend.services.allocation_engine import allocate_resources
from backend.db.database import SessionLocal
from backend.db.models import Warehouse

def resource_node(state: ADCCState) -> dict:
    pq = state.get("priority_queue", [])
    zones = state.get("zones", [])
    
    db = SessionLocal()
    try:
        warehouses_db = db.query(Warehouse).all()
        warehouses = [{"warehouse_id": w.warehouse_id, "lat": w.lat, "lon": w.lon, "food_units": w.food_units, "medicine_units": w.medicine_units, "rescue_kits": w.rescue_kits} for w in warehouses_db]
    finally:
        db.close()
    
    allocations = allocate_resources(pq, zones, warehouses)
    
    timestamp = datetime.utcnow().isoformat() + "Z"
    decision: AgentDecision = {
        "agent": "resource",
        "action": "Allocated inventory to priority zones",
        "target_zone": None,
        "reasoning": f"Distributed supplies to {len(pq)} zones based on severity.",
        "timestamp": timestamp
    }
    
    event: TimelineEvent = {
        "event_id": f"EVT-{uuid.uuid4().hex[:8]}",
        "timestamp": timestamp,
        "agent": "resource",
        "event_type": "allocate",
        "description": "Food and medicine allocated from closest warehouses",
        "zone_id": None
    }
    
    return {
        "resources": allocations,
        "agent_decisions": [decision],
        "timeline_events": [event]
    }
