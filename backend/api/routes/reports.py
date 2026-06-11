from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session
from typing import Optional

from backend.db.database import get_db
from backend.services.report_service import create_report, get_reports, get_report_by_id

router = APIRouter(prefix="/api/reports", tags=["reports"])


# ── Request / Response models ──────────────────────────────

class CreateReportRequest(BaseModel):
    latitude: float
    longitude: float
    road_blocked: bool = False
    building_collapsed: bool = False
    people_injured: bool = False
    people_dead: bool = False
    request_help: bool = False
    safe_area: bool = False
    safe_road: bool = False
    description: Optional[str] = None
    disaster_id: Optional[str] = None

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, v):
        if not -90 <= v <= 90:
            raise ValueError("latitude must be between -90 and 90")
        return v

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, v):
        if not -180 <= v <= 180:
            raise ValueError("longitude must be between -180 and 180")
        return v

    @field_validator("description")
    @classmethod
    def validate_description(cls, v):
        if v is not None and len(v) > 1000:
            raise ValueError("description must be 1000 characters or fewer")
        return v

    def has_at_least_one_flag(self) -> bool:
        return any([
            self.road_blocked,
            self.building_collapsed,
            self.people_injured,
            self.people_dead,
            self.request_help,
            self.safe_area,
            self.safe_road,
        ])


# ── Endpoints ──────────────────────────────────────────────

@router.post("", status_code=201)
async def submit_report(
    request: CreateReportRequest,
    db: Session = Depends(get_db),
):
    """Submit a new citizen report."""
    if not request.has_at_least_one_flag():
        raise HTTPException(
            status_code=422,
            detail="At least one report type must be selected"
        )

    report = await create_report(
        db=db,
        latitude=request.latitude,
        longitude=request.longitude,
        road_blocked=request.road_blocked,
        building_collapsed=request.building_collapsed,
        people_injured=request.people_injured,
        people_dead=request.people_dead,
        request_help=request.request_help,
        safe_area=request.safe_area,
        safe_road=request.safe_road,
        description=request.description,
        disaster_id=request.disaster_id,
    )
    return report


@router.get("")
async def list_reports(
    disaster_id: Optional[str] = None,
    limit: int = 200,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """Fetch all citizen reports, with optional disaster_id filter."""
    return get_reports(db, disaster_id=disaster_id, limit=limit, offset=offset)


@router.get("/{report_id}")
async def get_single_report(
    report_id: str,
    db: Session = Depends(get_db),
):
    """Fetch a single citizen report by ID."""
    result = get_report_by_id(db, report_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return result
