from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float
from typing import List
from ..database import Base

class Warehouse(Base):
    __tablename__ = "warehouses"

    warehouse_id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    lat: Mapped[float] = mapped_column(Float)
    lon: Mapped[float] = mapped_column(Float)
    food_units: Mapped[int] = mapped_column(Integer)
    medicine_units: Mapped[int] = mapped_column(Integer)
    rescue_kits: Mapped[int] = mapped_column(Integer)

    resources: Mapped[List["Resource"]] = relationship(back_populates="warehouse")
