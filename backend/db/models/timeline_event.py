from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from typing import Optional
from ..database import Base

class TimelineEvent(Base):
    __tablename__ = "timeline_events"

    event_id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    disaster_id: Mapped[str] = mapped_column(String, ForeignKey("disasters.disaster_id"))
    timestamp: Mapped[str] = mapped_column(String)
    agent: Mapped[str] = mapped_column(String)
    event_type: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    zone_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    disaster: Mapped["Disaster"] = relationship(back_populates="timeline_events")
