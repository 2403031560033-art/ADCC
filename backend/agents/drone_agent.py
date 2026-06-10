from datetime import datetime
import uuid
from backend.agents.state import ADCCState, AgentDecision, TimelineEvent

def drone_node(state: ADCCState) -> dict:
    zones = state.get("zones", [])
    blocked_zones = [z for z in zones if not z.get('road_accessible')]
    
    drone_assignments = []
    for i, z in enumerate(blocked_zones):
        drone_assignments.append({
            "zone_id": z['zone_id'],
            "drone_id": f"D-00{i%9 + 1}"
        })
        
    timestamp = datetime.utcnow().isoformat() + "Z"
    decision: AgentDecision = {
        "agent": "drone",
        "action": "Deployed drones to blocked zones",
        "target_zone": None,
        "reasoning": f"Assigned {len(drone_assignments)} drones to inaccessible areas.",
        "timestamp": timestamp
    }
    
    event: TimelineEvent = {
        "event_id": f"EVT-{uuid.uuid4().hex[:8]}",
        "timestamp": timestamp,
        "agent": "drone",
        "event_type": "drone_deploy",
        "description": f"Drones deployed to {len(blocked_zones)} blocked zones",
        "zone_id": None
    }
    
    return {
        "drone_assignments": drone_assignments,
        "agent_decisions": [decision],
        "timeline_events": [event]
    }
