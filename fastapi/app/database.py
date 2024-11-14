from sqlalchemy import NullPool, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg
from psycopg.rows import dict_row, namedtuple_row
import time
from .config import settings

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#create a session for every request that we make to the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

while True:
    try:
        # conn = psycopg.connect(conninfo='localhost' port=5432 dbname='fastapi')
        conn = psycopg.connect(host='localhost',port = 5432,user = 'postgres',
                            dbname = 'fastapi', password='3July2024@', row_factory= dict_row)
        cursor = conn.cursor()
        print("Database connected successfully!!")
        break
    except Exception as error:
        print("Database connectivity failed!!")
        print("Error : ",error)
        time.sleep(2)