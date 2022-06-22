from sqlalchemy.sql import func
from core.database import Base

from sqlalchemy import Column, Integer, String, DATETIME
from sqlalchemy.orm import relationship



class CategoriesModel(Base):
    __tablename__ = "Categories"

    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(200), unique=True, index=True)
    vehicles = relationship("VehiclesModel", backref="category")
    updated_on = Column(DATETIME(), onupdate=func.now())
    created_on = Column(DATETIME(), default=func.now())


