from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, Boolean, ForeignKey, JSON
from typing import Any
from ..database import Base

class Route(Base):
    __tablename__ = "routes"

    route_id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    disaster_id: Mapped[str] = mapped_column(String, ForeignKey("disasters.disaster_id"))
    from_id: Mapped[str] = mapped_column(String)
    to_id: Mapped[str] = mapped_column(String)
    waypoints: Mapped[Any] = mapped_column(JSON)
    distance_km: Mapped[float] = mapped_column(Float)
    eta_minutes: Mapped[int] = mapped_column(Integer)
    blocked: Mapped[bool] = mapped_column(Boolean)
    via_drone: Mapped[bool] = mapped_column(Boolean)

    disaster: Mapped["Disaster"] = relationship(back_populates="routes")
