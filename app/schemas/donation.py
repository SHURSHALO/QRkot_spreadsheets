from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, Extra


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationUpgrade(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]
    invested_amount: int = Field(
        0,
    )
    fully_invested: bool = Field(
        False,
    )
    close_date: Optional[datetime]


class DonationDB(DonationCreate):
    id: int
    create_date: datetime
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
