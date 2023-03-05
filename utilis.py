from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymssql


# DATABASE_URL = 'f'mssql+pymssql://{settings.DB_UID}:{settings.DB_PWD}@{settings.DB_SERVER}:{settings.DB_PORT}/{settings.DB_NAME}'


server = 'DESKTOP-UIGNTDP\SQLEXPRESS,9124'
database = 'invoices'
username = 'sa'
password = 'oracle1237494'

# Connect to the database
DATABASE_URL = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+11+for+SQL+Server"

# QLALCHEMY_DATABASE_URL = DATABASE_URL

DATABASE_URL_MYSQL = f"mysql+pymysql://root:@localhost:3306/hrmis"
engine_mysql = create_engine(DATABASE_URL_MYSQL)
engine_msssql = create_engine(DATABASE_URL)
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:oracle1234@localhost:3306/hrmis"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
) 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
server = '41.215.30.210,1433'
database = 'hrms'
username = 'sa'
password = 'oracle1234'

# Connect to the database
DATABASE_URL = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+11+for+SQL+Server"

SQLALCHEMY_DATABASE_URL = DATABASE_URL

DATABASE_URL_MYSQL = f"mysql+pymysql://root:@localhost:3306/hrmis"
engine_mysql = create_engine(DATABASE_URL_MYSQL)
engine_msssql = create_engine(DATABASE_URL)

"""
This file contains FastAPI app.
Modify the routes as you wish.
"""

import datetime
import time
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, validator
from redbird.oper import in_, between, greater_equal

from fastapi import APIRouter, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from scheduler import app as app_rocketry

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
