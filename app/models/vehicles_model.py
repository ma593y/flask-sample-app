from sqlalchemy.sql import func
from core.database_config import Base
from sqlalchemy import Column, Integer, String, DATETIME, ForeignKey



class VehiclesModel(Base):
    __tablename__ = "Vehicles"

    vehicle_id = Column(Integer, primary_key=True, index=True)
    vehicle_make = Column(String(200))
    vehicle_model = Column(String(200))
    vehicle_color = Column(String(200))
    vehicle_fuel_type = Column(String(200))
    vehicle_transmission = Column(String(200))

    vehicle_year = Column(Integer)
    vehicle_price = Column(Integer)
    vehicle_mileage = Column(Integer)
    vehicle_tank_capacity = Column(Integer)
    vehicle_engine_capacity = Column(Integer)

    category_id = Column(Integer, ForeignKey("Categories.category_id"))

    updated_on = Column(DATETIME(), onupdate=func.now())
    created_on = Column(DATETIME(), default=func.now())


