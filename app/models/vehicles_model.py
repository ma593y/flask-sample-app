from sqlalchemy.sql import func
from core.database import Base

from sqlalchemy import Column, Integer, String, DATETIME



class VehiclesModel(Base):
    __tablename__ = "Vehicles"

    vehicle_id = Column(Integer, primary_key=True, index=True)
    vehicle_make = Column(String(200))
    vehicle_model = Column(String(200))
    vehicle_color = Column(String(200))
    vehicle_year = Column(String(200))
    vehicle_price = Column(String(200))
    vehicle_mileage = Column(String(200))
    vehicle_fuel_type = Column(String(200))
    vehicle_transmission = Column(String(200))
    vehicle_tank_capacity = Column(String(200))
    vehicle_engine_capacity = Column(String(200))
    updated_on = Column(DATETIME(), onupdate=func.now())
    created_on = Column(DATETIME(), default=func.now())


