from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PaymentBase(BaseModel):
    description: str
    amount: float
    promo: str
    timestamp: datetime


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    id: int
    amount: float = 0.0


class Payment(PaymentBase):
    id: int

    class ConfigDict:
        from_attributes = True