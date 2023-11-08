from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from db.config_db import PostgresConfig
from db.exceptions.connect_exception import DBConnectException

url = PostgresConfig.url
engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def check_db_connect():
    try:
        session = SessionLocal()
        session.execute(text("SELECT 1"))
        session.close()
    except:
        raise DBConnectException()
