from backend.services.severity_engine import compute_severity, rank_zones

def test_tc1_majuli_island():
    # TC1: Majuli Island (pop 8000, road blocked, flood) → severity 10
    zone = {
        "zone_id": "Z-011",
        "name": "Majuli Island",
        "population": 8000,
        "road_accessible": False
    }
    
    severity = compute_severity(zone, "flood")
    assert severity == 10, f"Expected severity 10, got {severity}"

def test_rank_zones():
    zones = [
        {"zone_id": "Z-001", "population": 2000, "road_accessible": True},
        {"zone_id": "Z-011", "population": 8000, "road_accessible": False},
        {"zone_id": "Z-002", "population": 4000, "road_accessible": True}
    ]
    
    ranked = rank_zones(zones, "flood")
    assert ranked == ["Z-011", "Z-002", "Z-001"]
