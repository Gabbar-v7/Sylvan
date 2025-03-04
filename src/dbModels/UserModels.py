from sqlalchemy import DateTime, Integer, String, Enum, Boolean, ForeignKey, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from typing import Optional

from src.dbModels.BaseModel import Base
from src.security.oneway import generate_secure_hash


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False)
    firstName: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    lastName: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[str] = mapped_column(
        Enum("patient", "doctor", "anonymous-doctor",
             name="role_enum", create_constraint=True),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    phone: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, unique=True)
    password: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    preferences = relationship(
        "UserPreference", back_populates="user", uselist=False, cascade="all, delete")

    def __init__(self, firstName: str, lastName: str, role: str, email: str, phone: Optional[str], password: Optional[str]):
        self.firstName = firstName
        self.lastName = lastName
        self.role = role
        self.email = email
        self.phone = phone if phone else None
        self.password = generate_secure_hash(password) if password else None

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def get_role(self):
        return self.role

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"User(id={self.id!r}, firstName={self.firstName!r}, lastName={self.lastName!r}, email={self.email!r})"

    def as_dict(self):
        data = {column.name: getattr(self, column.name)
                for column in self.__table__.columns}
        data.pop("password", None)  # Exclude password from the dictionary
        return data


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    email_notification: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False)
    sms_notification: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False)

    # Relationships
    user = relationship("User", back_populates="preferences")

    def __init__(self, user_id: int, email_notification: bool = True, sms_notification: bool = True):
        self.user_id = user_id
        self.email_notification = email_notification
        self.sms_notification = sms_notification
