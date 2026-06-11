import uuid
from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy.orm import Session

from backend.db.models.citizen_report import CitizenReport
from backend.services.socket_manager import emit_citizen_report
from backend.services import verification_engine


def _generate_report_id() -> str:
    """Generate a short unique report ID like RPT-a1b2c3d4."""
    return f"RPT-{uuid.uuid4().hex[:8]}"


def _now_iso() -> str:
    """Current UTC time in ISO 8601 format."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _report_to_dict(report: CitizenReport) -> dict:
    """Convert a CitizenReport ORM instance to a plain dict."""
    return {
        "report_id": report.id,
        "disaster_id": report.disaster_id,
        "latitude": report.latitude,
        "longitude": report.longitude,
        "road_blocked": report.road_blocked,
        "building_collapsed": report.building_collapsed,
        "people_injured": report.people_injured,
        "people_dead": report.people_dead,
        "request_help": report.request_help,
        "safe_area": report.safe_area,
        "safe_road": report.safe_road,
        "description": report.description,
        "confidence_score": report.confidence_score,
        "status": report.status,
        "created_at": report.created_at,
        "updated_at": report.updated_at,
    }


async def create_report(
    db: Session,
    latitude: float,
    longitude: float,
    road_blocked: bool = False,
    building_collapsed: bool = False,
    people_injured: bool = False,
    people_dead: bool = False,
    request_help: bool = False,
    safe_area: bool = False,
    safe_road: bool = False,
    description: Optional[str] = None,
    disaster_id: Optional[str] = None,
) -> dict:
    """Create a new citizen report, persist it, and broadcast via Socket.IO."""
    now = _now_iso()
    report = CitizenReport(
        id=_generate_report_id(),
        disaster_id=disaster_id,
        latitude=latitude,
        longitude=longitude,
        road_blocked=road_blocked,
        building_collapsed=building_collapsed,
        people_injured=people_injured,
        people_dead=people_dead,
        request_help=request_help,
        safe_area=safe_area,
        safe_road=safe_road,
        description=description,
        confidence_score=0.5,
        status="pending",
        created_at=now,
        updated_at=now,
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    report_dict = _report_to_dict(report)

    # Broadcast to all connected clients in real-time
    await emit_citizen_report(report_dict)

    # Phase 2: Recalculate confidence for nearby reports
    updated = verification_engine.recalculate_area(db, latitude, longitude)
    for u in updated:
        # Re-broadcast any reports whose confidence changed
        updated_report = get_report_by_id(db, u["report_id"])
        if updated_report:
            await emit_citizen_report(updated_report)

    return report_dict


def get_reports(
    db: Session,
    disaster_id: Optional[str] = None,
    limit: int = 200,
    offset: int = 0,
) -> dict:
    """Fetch citizen reports with optional filtering."""
    query = db.query(CitizenReport)
    if disaster_id:
        query = query.filter(CitizenReport.disaster_id == disaster_id)

    total = query.count()
    reports = (
        query
        .order_by(CitizenReport.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "reports": [_report_to_dict(r) for r in reports],
        "total": total,
    }


def get_report_by_id(db: Session, report_id: str) -> Optional[dict]:
    """Fetch a single report by its ID. Returns None if not found."""
    report = db.query(CitizenReport).filter(CitizenReport.id == report_id).first()
    if report is None:
        return None
    return _report_to_dict(report)
