from fastapi import APIRouter

router = APIRouter(prefix="/api/agents", tags=["agents"])

@router.get("/decisions")
async def get_agent_decisions():
    return {
        "decisions": [
            {
                "agent": "coordinator",
                "action": "Prioritized Zone Z-001 as critical",
                "target_zone": "Z-001",
                "reasoning": "Zone Z-001 has severity 9, population 4200, road blocked. Dispatching Drone Agent.",
                "timestamp": "2025-01-01T10:01:00Z"
            }
        ]
    }
