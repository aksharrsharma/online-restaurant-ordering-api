from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Promos(Base):
    __tablename__ = "promos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(25), unique=True, nullable=False, index=True)
    percent_off = Column(DECIMAL, nullable=False)
    expiration = Column(DATETIME, nullable=False, server_default=str(datetime.now()))

