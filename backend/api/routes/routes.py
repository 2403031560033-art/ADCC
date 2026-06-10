from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from backend.services.route_optimizer import optimize_routes

router = APIRouter(prefix="/api/route", tags=["routes"])

class OptimizeRouteRequest(BaseModel):
    disaster_id: str
    blocked_zone_ids: List[str]

@router.post("/optimize")
async def optimize_routes_api(request: OptimizeRouteRequest):
    from backend.db.database import SessionLocal
    from backend.db.models import Warehouse, Zone
    
    db = SessionLocal()
    try:
        warehouses_db = db.query(Warehouse).all()
        warehouses = [{"warehouse_id": w.warehouse_id, "lat": w.lat, "lon": w.lon} for w in warehouses_db]
        
        zones_db = db.query(Zone).filter(Zone.disaster_id == request.disaster_id).all()
        priority_zones = [{"zone_id": z.zone_id, "lat": z.lat, "lon": z.lon, "road_accessible": z.road_accessible} for z in zones_db]
        
        # Vehicles from seed mock
        vehicles = [
            {"vehicle_id": "V-001", "base": "WH-001"},
            {"vehicle_id": "V-004", "base": "WH-002"},
            {"vehicle_id": "V-007", "base": "WH-003"}
        ]
        
        routes = optimize_routes(warehouses, vehicles, priority_zones, request.blocked_zone_ids)
        return {"routes": routes}
    finally:
        db.close()

