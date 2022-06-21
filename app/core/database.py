# Import Third-Party Libraries 

import os
import pymysql
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# DB Configs

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USERNAME}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


# SQLAlchemy Setup

engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_size=100, max_overflow=50, pool_recycle=3600)
session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = scoped_session(session_factory)

Base = declarative_base()
