from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class PromoBase(BaseModel):
    code:str
    percent_off:float
    expiration: datetime


class PromoCreate(PromoBase):
    pass

class PromoUpdate(BaseModel):
    id:int
    code:str
    percent_off:float = 0.0


class Promo(PromoBase):
    id: int

    class ConfigDict:
        from_attributes = True