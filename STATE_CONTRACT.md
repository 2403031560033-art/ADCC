# ADCC — State Contract
# ADCCState is defined ONCE here. Do not redefine it anywhere else.
# All LangGraph nodes read from and write to this exact structure.

---

## ADCCState (Python TypedDict)

```python
from typing import TypedDict, List, Optional
from datetime import datetime

class ZoneState(TypedDict):
    zone_id: str          # e.g. "Z-001"
    name: str             # e.g. "Dibrugarh North"
    lat: float
    lon: float
    severity: int         # 1–10 (computed by severity_engine.py)
    population: int
    status: str           # "critical" | "moderate" | "stable"
    road_accessible: bool
    assigned_agent: Optional[str]

class ResourceState(TypedDict):
    resource_id: str
    type: str             # "food" | "medicine" | "rescue_equipment"
    quantity: int
    warehouse_id: str
    allocated_to: Optional[str]  # zone_id

class RouteState(TypedDict):
    route_id: str
    from_id: str          # warehouse_id or hospital_id
    to_id: str            # zone_id
    waypoints: List[dict] # [{"lat": float, "lon": float}]
    distance_km: float
    eta_minutes: int
    blocked: bool
    via_drone: bool

class AgentDecision(TypedDict):
    agent: str            # "coordinator" | "route" | "resource" | "medical" | "drone"
    action: str           # human-readable action taken
    target_zone: Optional[str]
    reasoning: str        # shown in Agent Activity Panel
    timestamp: str        # ISO 8601

class TimelineEvent(TypedDict):
    event_id: str
    timestamp: str
    agent: str
    event_type: str       # "dispatch" | "reroute" | "allocate" | "drone_deploy" | "priority_change"
    description: str
    zone_id: Optional[str]

class ADCCState(TypedDict):
    # Disaster context
    disaster_id: str
    disaster_type: str    # "flood" | "earthquake" | "cyclone"
    region: str
    triggered_at: str     # ISO 8601

    # Core data
    zones: List[ZoneState]
    resources: List[ResourceState]
    routes: List[RouteState]

    # Agent outputs
    priority_queue: List[str]       # zone_ids sorted by severity desc
    drone_assignments: List[dict]   # [{zone_id, drone_id}]
    medical_actions: List[dict]     # [{zone_id, hospital_id, supplies}]
    agent_decisions: List[AgentDecision]

    # Timeline
    timeline_events: List[TimelineEvent]

    # Final output
    final_plan: dict                # summary sent to frontend via Socket.IO

    # Computed metrics (populated by impact_engine.py)
    response_time_reduction: float  # percentage
    delivery_efficiency: float      # percentage
    supplies_delivered: float       # percentage
    lives_impacted: int
```

---

## Field Name Rules (FROZEN — do not rename)

| Concept | Field Name | Type |
|---|---|---|
| Zone identifier | `zone_id` | str |
| Severity score | `severity` | int (1–10) |
| Road blocked | `road_accessible` | bool (False = blocked) |
| Agent name | `agent` | str (lowercase) |
| Agent reasoning | `reasoning` | str |
| Event description | `description` | str |
| Drone assigned | `via_drone` | bool |

**CRITICAL:** The frontend reads `agent_decisions[].reasoning` for the Agent Panel.
The frontend reads `timeline_events[].description` for the Timeline.
Do NOT rename these fields.

---

## LangGraph Node Order

```
START
  ↓
severity_node          → populates: zones[].severity, priority_queue
  ↓
route_node             → populates: routes[], priority_queue zones with road_accessible=False
  ↓
resource_node          → populates: resources[].allocated_to
  ↓
medical_node           → populates: medical_actions[]
  ↓
drone_node             → populates: drone_assignments[], routes[].via_drone
  ↓
coordinator_node       → populates: final_plan, timeline_events
  ↓
END → emit via Socket.IO
```

---

## Socket.IO Events (frontend listens to these)

| Event | Payload |
|---|---|
| `agent_update` | `{ agent: str, action: str, reasoning: str }` |
| `timeline_event` | `TimelineEvent` object |
| `state_update` | Full `ADCCState` snapshot |
| `metrics_update` | `{ response_time_reduction, delivery_efficiency, supplies_delivered, lives_impacted }` |
