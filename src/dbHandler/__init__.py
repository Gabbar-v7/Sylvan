from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.dbHandler.dbUsers import User, UserBase

# Corrected SQLite URL for a relative path
_engine = create_engine("sqlite:///database.db", echo=True)

# Create tables
UserBase.metadata.create_all(_engine)

dbSession = sessionmaker(bind=_engine)
