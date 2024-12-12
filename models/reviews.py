from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Reviews(Base):
    __tablename__ = "reviews"

    id=Column(Integer, primary_key=True, index=True, autoincrement=True)
    description=Column(String(500), unique=False, nullable=False)
    rating=Column(Integer, index=True, nullable=False, server_default="0")

