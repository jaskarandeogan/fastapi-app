# Description: This file contains the database configuration and connection details.

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

load_dotenv(".env")

DATABASE_URL = os.getenv("DATABASE_URL")

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_URL}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
