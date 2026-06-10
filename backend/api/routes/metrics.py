from fastapi import APIRouter

router = APIRouter(prefix="/api/metrics", tags=["metrics"])

@router.get("/{disaster_id}")
async def get_metrics(disaster_id: str):
    return {
        "disaster_id": disaster_id,
        "response_time_reduction": 42.0,
        "delivery_efficiency": 67.0,
        "supplies_delivered": 91.0,
        "lives_impacted": 3200
    }
