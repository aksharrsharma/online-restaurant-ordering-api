from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ReviewBase(BaseModel):
    description: str
    rating: int


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    id: int
    description: Optional[str] = None
    rating: int = 0


class Review(ReviewBase):
    id: int

    class ConfigDict:
        from_attributes = True