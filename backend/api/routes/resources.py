from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from backend.services.allocation_engine import allocate_resources

router = APIRouter(prefix="/api/resource", tags=["resources"])

class AllocateResourceRequest(BaseModel):
    disaster_id: str
    priority_zone_ids: List[str]

@router.post("/allocate")
async def allocate_resources_api(request: AllocateResourceRequest):
    from backend.db.database import SessionLocal
    from backend.db.models import Warehouse, Zone
    
    db = SessionLocal()
    try:
        warehouses_db = db.query(Warehouse).all()
        warehouses = [{"warehouse_id": w.warehouse_id, "lat": w.lat, "lon": w.lon, "food_units": w.food_units, "medicine_units": w.medicine_units, "rescue_kits": w.rescue_kits} for w in warehouses_db]
        
        zones_db = db.query(Zone).filter(Zone.disaster_id == request.disaster_id).all()
        zones = [{"zone_id": z.zone_id, "lat": z.lat, "lon": z.lon, "severity": z.severity} for z in zones_db]
        
        allocations = allocate_resources(request.priority_zone_ids, zones, warehouses)
        return {"allocations": allocations}
    finally:
        db.close()

