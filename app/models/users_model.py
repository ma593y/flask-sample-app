from sqlalchemy.sql import func
from core.database_config import Base
from sqlalchemy import Boolean, Column, Integer, String, DATETIME
from werkzeug.security import generate_password_hash, check_password_hash



class UsersModel(Base):
    __tablename__ = "Users"

    user_id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String(200), unique=True, index=True)
    user_full_name = Column(String(200))
    user_hashed_password = Column(String(200))
    user_is_active = Column(Boolean, default=True)
    
    updated_on = Column(DATETIME(), onupdate=func.now())
    created_on = Column(DATETIME(), default=func.now())


    def set_hashed_password(self, random_password):
        self.user_hashed_password = generate_password_hash(password=random_password)
        return True

    
    def check_hashed_password(self, password):
        return check_password_hash(self.user_hashed_password, password)


