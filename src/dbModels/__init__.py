from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from src.dbModels.BaseModel import Base
from src.dbModels.UserModels import User,UserPreference
from src.utils.pre_loader import config

# Corrected SQLite URL for a relative path
_engine = create_engine(
    environ.get("SQLALCHEMY_DATABASE_URI"),
    echo=(config.getboolean("database", "echo")),
    poolclass=QueuePool,  # Use QueuePool for connection pooling
    pool_size=config.getint(
        "database", "pool_size", fallback=5
    ),  # Number of connections in the pool
    max_overflow=config.getint(
        "database", "max_overflow", fallback=10
    ),  # Overflow connections beyond pool_size
    pool_timeout=config.getint(
        "database", "pool_timeout", fallback=30
    ),  # Timeout for acquiring a connection
)

# Create tables
Base.metadata.create_all(_engine)

dbSession = sessionmaker(bind=_engine)
