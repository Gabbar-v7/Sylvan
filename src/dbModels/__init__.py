from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.dbModels.BaseModel import Base
from src.dbModels.UserModel import User
from src.utils.pre_loader import config

# Corrected SQLite URL for a relative path
_engine = create_engine(
    environ.get("SQLALCHEMY_DATABASE_URI"),
    echo=(config.getboolean("database", "echo")),
)

# Create tables
Base.metadata.create_all(_engine)

dbSession = sessionmaker(bind=_engine)
