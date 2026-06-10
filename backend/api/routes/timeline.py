from fastapi import APIRouter

router = APIRouter(prefix="/api/timeline", tags=["timeline"])

@router.get("/{disaster_id}")
async def get_timeline(disaster_id: str):
    return {
        "events": [
            {
                "event_id": "EVT-001",
                "timestamp": "2025-01-01T10:01:00Z",
                "agent": "coordinator",
                "event_type": "priority_change",
                "description": "Zone Z-001 elevated to CRITICAL — population 4200 at risk",
                "zone_id": "Z-001"
            }
        ]
    }
