from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.dbModels.BaseModel import Base
from src.security.oneway import generate_secure_hash


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )
    firstName: Mapped[str] = mapped_column(String, nullable=True)
    lastName: Mapped[str] = mapped_column(String, nullable=True)
    role: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(
        String, nullable=True, unique=True
    )  # Change to String for phone numbers
    password: Mapped[str] = mapped_column(String, nullable=True, unique=True)
    create_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )

    # Constructor to initialize fields
    def __init__(
        self,
        firstName: str,
        lastName: str,
        role: str,
        email: str,
        phone: str,
        password: str,
    ):
        self.firstName = firstName
        self.lastName = lastName
        self.role = role
        self.email = email
        self.phone = phone
        self.password = generate_secure_hash(password)

    # Below properties are requeired for flask-login to validate and can be adjusted as needed
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_role(self):
        return self.role

    def get_id(self):
        return str(self.id)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, firstName={self.firstName!r}, lastName={self.lastName!r}, email={self.email!r}, phone={self.phone!r})"

    def as_dict(self) -> dict:
        data = super().as_dict()
        data.pop("password")
        data.pop("id")
        return data
