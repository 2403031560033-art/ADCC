from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, Boolean, ForeignKey
from typing import Optional
from ..database import Base

class Zone(Base):
    __tablename__ = "zones"

    zone_id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    disaster_id: Mapped[str] = mapped_column(String, ForeignKey("disasters.disaster_id"))
    name: Mapped[str] = mapped_column(String)
    lat: Mapped[float] = mapped_column(Float)
    lon: Mapped[float] = mapped_column(Float)
    severity: Mapped[int] = mapped_column(Integer)
    population: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String)
    road_accessible: Mapped[bool] = mapped_column(Boolean)
    assigned_agent: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    disaster: Mapped["Disaster"] = relationship(back_populates="zones")
