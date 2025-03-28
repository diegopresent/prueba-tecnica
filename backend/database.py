import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

db_username = os.getenv("USER_DB")
db_password = os.getenv("PASSWORD_DB")
db_host = os.getenv("HOST_DB")
db_port = os.getenv("PORT_DB")
db_name = os.getenv("DATABASE_NAME")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()