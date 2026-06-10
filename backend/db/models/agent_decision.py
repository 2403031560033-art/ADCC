from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from typing import Optional
from ..database import Base

class AgentDecision(Base):
    __tablename__ = "agent_decisions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    disaster_id: Mapped[str] = mapped_column(String, ForeignKey("disasters.disaster_id"))
    agent: Mapped[str] = mapped_column(String)
    action: Mapped[str] = mapped_column(String)
    target_zone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    reasoning: Mapped[str] = mapped_column(String)
    timestamp: Mapped[str] = mapped_column(String)

    disaster: Mapped["Disaster"] = relationship(back_populates="agent_decisions")
