from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id=Column(Integer, primary_key=True, index=True, autoincrement=True)
    description=Column(String(500), unique=False, nullable=False)
    amount=Column(DECIMAL, index=True, nullable=False, server_default="0.0")
    timestamp = Column(DATETIME, index=True, nullable=True, server_default=str(datetime.now()))
    promo=Column(String(500), unique=True, nullable=True)

