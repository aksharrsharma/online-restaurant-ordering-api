from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class UserType(str, Enum):
    customer = "customer"
    staff = "staff"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(30), unique=True, nullable=False, index=True)
    password = Column(String(25), nullable=False)
    user_type = Column(Enum(UserType()), nullable=False)

