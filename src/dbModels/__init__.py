from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from keys import SQLALCHEMY_DATABASE_URI

from src.dbModels.UserModel import Base, User

# Corrected SQLite URL for a relative path
_engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

# Create tables
Base.metadata.create_all(_engine)

dbSession = sessionmaker(bind=_engine)
