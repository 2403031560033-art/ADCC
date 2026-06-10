from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import List
from ..database import Base

class Disaster(Base):
    __tablename__ = "disasters"
    
    disaster_id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    disaster_type: Mapped[str] = mapped_column(String)
    region: Mapped[str] = mapped_column(String)
    triggered_at: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)

    zones: Mapped[List["Zone"]] = relationship(back_populates="disaster")
    routes: Mapped[List["Route"]] = relationship(back_populates="disaster")
    agent_decisions: Mapped[List["AgentDecision"]] = relationship(back_populates="disaster")
    timeline_events: Mapped[List["TimelineEvent"]] = relationship(back_populates="disaster")
