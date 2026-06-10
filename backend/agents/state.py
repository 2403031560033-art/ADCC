from typing import TypedDict, List, Optional
from datetime import datetime

class ZoneState(TypedDict):
    zone_id: str
    name: str
    lat: float
    lon: float
    severity: int
    population: int
    status: str
    road_accessible: bool
    assigned_agent: Optional[str]

class ResourceState(TypedDict):
    resource_id: str
    type: str
    quantity: int
    warehouse_id: str
    allocated_to: Optional[str]

class RouteState(TypedDict):
    route_id: str
    from_id: str
    to_id: str
    waypoints: List[dict]
    distance_km: float
    eta_minutes: int
    blocked: bool
    via_drone: bool

class AgentDecision(TypedDict):
    agent: str
    action: str
    target_zone: Optional[str]
    reasoning: str
    timestamp: str

class TimelineEvent(TypedDict):
    event_id: str
    timestamp: str
    agent: str
    event_type: str
    description: str
    zone_id: Optional[str]

class ADCCState(TypedDict):
    # Disaster context
    disaster_id: str
    disaster_type: str
    region: str
    triggered_at: str

    # Core data
    zones: List[ZoneState]
    resources: List[ResourceState]
    routes: List[RouteState]

    # Agent outputs
    priority_queue: List[str]
    drone_assignments: List[dict]
    medical_actions: List[dict]
    agent_decisions: List[AgentDecision]

    # Timeline
    timeline_events: List[TimelineEvent]

    # Final output
    final_plan: dict

    # Computed metrics
    response_time_reduction: float
    delivery_efficiency: float
    supplies_delivered: float
    lives_impacted: int
