from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

# Initialize Base
UserBase = declarative_base()


class User(UserBase):
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
        self.password = password

    def __repr__(self):
        return f"User(id={self.id!r}, firstName={self.firstName!r}, lastName={self.lastName!r})"

    def as_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }
