from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, Boolean, Text
from typing import Optional
from ..database import Base


class CitizenReport(Base):
    __tablename__ = "citizen_reports"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)

    # Location
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)

    # Optional link to active disaster
    disaster_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Report type flags
    road_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    building_collapsed: Mapped[bool] = mapped_column(Boolean, default=False)
    people_injured: Mapped[bool] = mapped_column(Boolean, default=False)
    people_dead: Mapped[bool] = mapped_column(Boolean, default=False)
    request_help: Mapped[bool] = mapped_column(Boolean, default=False)
    safe_area: Mapped[bool] = mapped_column(Boolean, default=False)
    safe_road: Mapped[bool] = mapped_column(Boolean, default=False)

    # Metadata
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.5)
    status: Mapped[str] = mapped_column(String, default="pending")

    # Timestamps (ISO 8601)
    created_at: Mapped[str] = mapped_column(String)
    updated_at: Mapped[str] = mapped_column(String)
