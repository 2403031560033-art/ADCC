from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float
from ..database import Base

class Hospital(Base):
    __tablename__ = "hospitals"

    hospital_id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    lat: Mapped[float] = mapped_column(Float)
    lon: Mapped[float] = mapped_column(Float)
    capacity: Mapped[int] = mapped_column(Integer)
    available_beds: Mapped[int] = mapped_column(Integer)
