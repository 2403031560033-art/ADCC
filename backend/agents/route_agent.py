from datetime import datetime
import uuid
from backend.agents.state import ADCCState, AgentDecision, TimelineEvent
from backend.services.route_optimizer import optimize_routes
from backend.db.database import SessionLocal
from backend.db.models import Warehouse

def route_node(state: ADCCState) -> dict:
    zones = state.get("zones", [])
    
    db = SessionLocal()
    try:
        warehouses_db = db.query(Warehouse).all()
        warehouses = [{"warehouse_id": w.warehouse_id, "lat": w.lat, "lon": w.lon} for w in warehouses_db]
    finally:
        db.close()
    
    vehicles = [
        {"vehicle_id": "V-001", "base": "WH-001"},
        {"vehicle_id": "V-004", "base": "WH-002"},
        {"vehicle_id": "V-007", "base": "WH-003"}
    ]
    
    priority_zones = [z for z in zones if z['zone_id'] in state.get("priority_queue", [])]
    blocked_zone_ids = [z['zone_id'] for z in zones if not z.get('road_accessible')]
    
    routes = optimize_routes(warehouses, vehicles, priority_zones, blocked_zone_ids)
    
    timestamp = datetime.utcnow().isoformat() + "Z"
    decision: AgentDecision = {
        "agent": "route",
        "action": "Optimized delivery routes",
        "target_zone": None,
        "reasoning": f"Calculated VRP for accessible zones. Skipped {len(blocked_zone_ids)} blocked zones.",
        "timestamp": timestamp
    }
    
    event: TimelineEvent = {
        "event_id": f"EVT-{uuid.uuid4().hex[:8]}",
        "timestamp": timestamp,
        "agent": "route",
        "event_type": "reroute",
        "description": "VRP routes calculated for ground vehicles",
        "zone_id": None
    }
    
    return {
        "routes": routes,
        "agent_decisions": [decision],
        "timeline_events": [event]
    }
