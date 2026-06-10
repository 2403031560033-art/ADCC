from fastapi import APIRouter

router = APIRouter(prefix="/api/zones", tags=["zones"])

@router.get("")
async def get_zones():
    return {
        "zones": [
            {
                "zone_id": "Z-001",
                "name": "Dibrugarh North",
                "lat": 27.47,
                "lon": 94.91,
                "severity": 9,
                "population": 4200,
                "status": "critical",
                "road_accessible": False,
                "assigned_agent": "drone"
            }
        ]
    }
