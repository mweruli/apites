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

SQLALCHEMY_DATABASE_URL = DATABASE_URL

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