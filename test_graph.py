from backend.agents.graph import app as adcc_graph
from backend.db.database import SessionLocal
from backend.db.models import Zone

db = SessionLocal()
try:
    zones = [{"zone_id": z.zone_id, "name": z.name, "lat": z.lat, "lon": z.lon, "severity": z.severity, "population": z.population, "status": z.status, "road_accessible": z.road_accessible} for z in db.query(Zone).all()]
finally:
    db.close()

initial_state = {
    "disaster_id": "test",
    "disaster_type": "flood",
    "region": "Assam",
    "triggered_at": "2025-01-01T10:00:00Z",
    "zones": zones,
    "resources": [],
    "routes": [],
    "priority_queue": [],
    "drone_assignments": [],
    "medical_actions": [],
    "agent_decisions": [],
    "timeline_events": [],
    "final_plan": {},
    "response_time_reduction": 0.0,
    "delivery_efficiency": 0.0,
    "supplies_delivered": 0.0,
    "lives_impacted": 0
}

print(f"Loaded {len(zones)} zones")
print("Invoking graph...")
result = adcc_graph.invoke(initial_state)
print("Keys returned:", result.keys())
print("Agent decisions:", len(result.get("agent_decisions", [])))
print("Timeline events:", len(result.get("timeline_events", [])))
