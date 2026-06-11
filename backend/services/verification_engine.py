"""
Verification Engine for Community Intelligence Network.

Rule-based confidence scoring using report density within a geographic radius.
Uses Haversine formula for distance calculation — no external dependencies.
"""

import math
from typing import List, Optional
from sqlalchemy.orm import Session
from backend.db.models.citizen_report import CitizenReport


# ── Constants ──────────────────────────────────────────────

RADIUS_METERS = 500       # Proximity radius for report clustering
TIME_WINDOW_HOURS = 2     # Only consider reports within this window
EARTH_RADIUS_KM = 6371.0  # Mean radius of the Earth in kilometers


# ── Haversine distance ────────────────────────────────────

def haversine_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance (in meters) between two points
    on Earth using the Haversine formula.
    """
    lat1_r, lat2_r = math.radians(lat1), math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return EARTH_RADIUS_KM * c * 1000  # convert km → meters


# ── Confidence scoring rules ──────────────────────────────

def compute_confidence(nearby_count: int) -> float:
    """
    Rule-based confidence score based on report density.

    3 reports in same area  → confidence 0.65
    5 reports in same area  → confidence 0.80
    10 reports in same area → confidence 1.0 (verified)
    """
    if nearby_count >= 10:
        return 1.0
    elif nearby_count >= 5:
        return 0.8
    elif nearby_count >= 3:
        return 0.65
    else:
        return 0.5  # default for isolated reports


def compute_status(confidence: float) -> str:
    """Determine status from confidence score."""
    if confidence >= 1.0:
        return "verified"
    return "pending"


# ── Main recalculation logic ─────────────────────────────

def recalculate_area(
    db: Session,
    center_lat: float,
    center_lon: float,
    radius_meters: float = RADIUS_METERS,
) -> List[dict]:
    """
    Recalculate confidence scores for all reports near (center_lat, center_lon).

    Returns a list of updated report dicts (report_id, confidence_score, status)
    so the caller can broadcast updates via Socket.IO.
    """
    # Rough bounding box to pre-filter with SQL (avoid scanning entire table)
    # 1 degree latitude ≈ 111,320 meters
    lat_delta = radius_meters / 111_320
    # 1 degree longitude ≈ 111,320 * cos(latitude)
    lon_delta = radius_meters / (111_320 * max(math.cos(math.radians(center_lat)), 0.01))

    candidates = (
        db.query(CitizenReport)
        .filter(
            CitizenReport.latitude.between(center_lat - lat_delta, center_lat + lat_delta),
            CitizenReport.longitude.between(center_lon - lon_delta, center_lon + lon_delta),
        )
        .all()
    )

    # Precise distance filter using Haversine
    nearby_reports = [
        r for r in candidates
        if haversine_meters(center_lat, center_lon, r.latitude, r.longitude) <= radius_meters
    ]

    nearby_count = len(nearby_reports)
    new_confidence = compute_confidence(nearby_count)
    new_status = compute_status(new_confidence)

    updated = []
    for report in nearby_reports:
        if report.confidence_score != new_confidence or report.status != new_status:
            report.confidence_score = new_confidence
            report.status = new_status
            updated.append({
                "report_id": report.id,
                "confidence_score": new_confidence,
                "status": new_status,
            })

    if updated:
        db.commit()

    return updated
