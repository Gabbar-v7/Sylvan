from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column
from src.security.oneway import hash


# Initialize Base
class Base(DeclarativeBase):
    def as_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )
    firstName: Mapped[str] = mapped_column(String, nullable=False)
    lastName: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(
        String, nullable=False, unique=True
    )  # Change to String for phone numbers
    password: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    create_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )

    # Constructor to initialize fields
    def __init__(
        self, firstName: str, lastName: str, email: str, phone: str, password: str
    ):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.phone = phone
        self.password = hash(password)

    def __repr__(self):
        return f"User(id={self.id!r}, firstName={self.firstName!r}, lastName={self.lastName!r}, email={self.email!r}, phone={self.phone!r}, password={self.password!r})"
