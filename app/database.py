from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

database = "fastapi"
hostname = "localhost"
username = "postgres"
password = "admin"

SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{password}@{hostname}/{database}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
