from datetime import datetime
import uuid
from backend.agents.state import ADCCState, AgentDecision, TimelineEvent
from backend.services.severity_engine import compute_severity, rank_zones

def severity_node(state: ADCCState) -> dict:
    zones = state.get("zones", [])
    disaster_type = state.get("disaster_type", "flood")
    
    updated_zones = []
    for z in zones:
        sev = compute_severity(z, disaster_type)
        z_copy = dict(z)
        z_copy["severity"] = sev
        updated_zones.append(z_copy)
        
    pq = rank_zones(updated_zones, disaster_type)
    
    timestamp = datetime.utcnow().isoformat() + "Z"
    decision: AgentDecision = {
        "agent": "coordinator",
        "action": "Computed severity scores",
        "target_zone": None,
        "reasoning": "Evaluated population and road access across all zones to build priority queue.",
        "timestamp": timestamp
    }
    
    event: TimelineEvent = {
        "event_id": f"EVT-{uuid.uuid4().hex[:8]}",
        "timestamp": timestamp,
        "agent": "system",
        "event_type": "priority_change",
        "description": "Severity computed and priority queue initialized",
        "zone_id": None
    }
    
    return {
        "zones": updated_zones,
        "priority_queue": pq,
        "agent_decisions": [decision],
        "timeline_events": [event]
    }
