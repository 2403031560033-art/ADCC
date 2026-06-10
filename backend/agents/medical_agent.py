from datetime import datetime
import uuid
from backend.agents.state import ADCCState, AgentDecision, TimelineEvent
from backend.db.database import SessionLocal
from backend.db.models import Hospital

def medical_node(state: ADCCState) -> dict:
    zones = state.get("zones", [])
    
    db = SessionLocal()
    try:
        hospitals_db = db.query(Hospital).all()
        hospitals = [{"hospital_id": h.hospital_id, "name": h.name, "capacity": h.capacity, "available_beds": h.available_beds} for h in hospitals_db]
    finally:
        db.close()
    
    medical_actions = []
    critical_zones = [z for z in zones if z['severity'] >= 8]
    
    for z in critical_zones:
        if hospitals:
            h = hospitals[0]
            medical_actions.append({
                "zone_id": z['zone_id'],
                "hospital_id": h['hospital_id'],
                "supplies": "Medical team dispatched"
            })
            
    timestamp = datetime.utcnow().isoformat() + "Z"
    decision: AgentDecision = {
        "agent": "medical",
        "action": "Assigned medical teams",
        "target_zone": None,
        "reasoning": f"Dispatched medical support to {len(critical_zones)} critical zones.",
        "timestamp": timestamp
    }
    
    event: TimelineEvent = {
        "event_id": f"EVT-{uuid.uuid4().hex[:8]}",
        "timestamp": timestamp,
        "agent": "medical",
        "event_type": "dispatch",
        "description": "Medical teams assigned to critical zones",
        "zone_id": None
    }
    
    return {
        "medical_actions": medical_actions,
        "agent_decisions": [decision],
        "timeline_events": [event]
    }
