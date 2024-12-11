from sqlalchemy.orm import DeclarativeBase


# Initialize Base
class Base(DeclarativeBase):
    def as_dict(self) -> dict:
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }
