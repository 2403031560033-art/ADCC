def compute_severity(zone: dict, disaster_type: str) -> int:
    """
    Compute severity for a given zone using deterministic rules.
    """
    base_score = (zone["population"] / 1000) * 1.5
    road_multiplier = 3.0 if not zone["road_accessible"] else 1.0
    disaster_multiplier = 1.5 if disaster_type == "flood" else 1.2
    
    raw_score = base_score * road_multiplier * disaster_multiplier
    severity = min(10, round(raw_score))
    return severity

def rank_zones(zones: list, disaster_type: str) -> list:
    """
    Computes severity for all zones, sorts them descending, and returns sorted zone_ids.
    """
    scored_zones = []
    for zone in zones:
        sev = compute_severity(zone, disaster_type)
        scored_zones.append((zone["zone_id"], sev))
    
    # Sort by severity descending
    scored_zones.sort(key=lambda x: x[1], reverse=True)
    
    return [z[0] for z in scored_zones]
