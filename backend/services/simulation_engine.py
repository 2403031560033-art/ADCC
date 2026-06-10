import json
import os
from sqlalchemy.orm import Session
from backend.db.models import Disaster, Zone, Hospital, Warehouse

async def load_scenario(scenario_name: str, db: Session) -> dict:
    """Load a disaster scenario from seed JSON. Deletes existing data first for re-runs."""
    # Path to the seed file
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    seed_file_path = os.path.join(base_dir, "seed_data", f"{scenario_name}.json")
    
    with open(seed_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    disaster_data = data["disaster"]
    disaster_id = disaster_data["disaster_id"]
    
    # ── Wipe EVERYTHING before seeding fresh data ──
    # This ensures zones from previous scenarios never linger in the DB.
    db.query(Zone).delete()
    db.query(Hospital).delete()
    db.query(Warehouse).delete()
    db.query(Disaster).delete()
    db.commit()

    # 1. Create Disaster
    disaster = Disaster(
        disaster_id=disaster_id,
        disaster_type=disaster_data["disaster_type"],
        region=disaster_data["region"],
        triggered_at=disaster_data["triggered_at"],
        status=disaster_data["status"]
    )
    db.add(disaster)
    db.flush()
    
    # 2. Insert Zones
    for z in data["zones"]:
        zone = Zone(
            zone_id=z["zone_id"],
            disaster_id=disaster_id,
            name=z["name"],
            lat=z["lat"],
            lon=z["lon"],
            severity=z["severity"],
            population=z["population"],
            status=z["status"],
            road_accessible=z["road_accessible"],
            assigned_agent=z.get("assigned_agent")
        )
        db.add(zone)
        
    # 3. Insert Hospitals
    for h in data["hospitals"]:
        hospital = Hospital(
            hospital_id=h["hospital_id"],
            name=h["name"],
            lat=h["lat"],
            lon=h["lon"],
            capacity=h["capacity"],
            available_beds=h["available_beds"]
        )
        db.add(hospital)
        
    # 4. Insert Warehouses
    for w in data["warehouses"]:
        warehouse = Warehouse(
            warehouse_id=w["warehouse_id"],
            name=w["name"],
            lat=w["lat"],
            lon=w["lon"],
            food_units=w["food_units"],
            medicine_units=w["medicine_units"],
            rescue_kits=w["rescue_kits"]
        )
        db.add(warehouse)
        
    db.commit()
    
    summary = data.get("summary", {})
    return {
        "disaster_id": disaster_id,
        "disaster_type": disaster_data["disaster_type"],
        "region": disaster_data["region"],
        "scenario_name": scenario_name,
        "total_zones": summary.get("total_zones", len(data["zones"])),
        "total_population_at_risk": summary.get("total_population_at_risk", 0),
    }
