from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from typing import Optional
from ..database import Base

class Resource(Base):
    __tablename__ = "resources"

    resource_id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    type: Mapped[str] = mapped_column(String)
    quantity: Mapped[int] = mapped_column(Integer)
    warehouse_id: Mapped[str] = mapped_column(String, ForeignKey("warehouses.warehouse_id"))
    allocated_to: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    warehouse: Mapped["Warehouse"] = relationship(back_populates="resources")
