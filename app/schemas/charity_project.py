from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, Extra, validator

from app.api.constants import MIN_LENGTH, MAX_LENGTH


class CharityProjectCreate(BaseModel):
    name: str = Field(..., min_length=MIN_LENGTH, max_length=MAX_LENGTH)
    description: str = Field(..., min_length=MIN_LENGTH)
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid
        orm_mode = True


class CharityProjectResponses(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpgrade(CharityProjectCreate):
    invested_amount: int = Field(
        0,
    )
    fully_invested: bool = Field(
        False,
    )
    close_date: Optional[datetime]


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(
        None, min_length=MIN_LENGTH, max_length=MAX_LENGTH
    )
    description: Optional[str] = Field(None, min_length=MIN_LENGTH)
    full_amount: Optional[PositiveInt]

    @validator('name', 'description', 'full_amount')
    def validate_fields(cls, value, field):
        if field.name == 'name' and value is None:
            raise ValueError('Укажите название проекта!')
        if field.name == 'description' and value is None:
            raise ValueError('Укажите описание проекта!')
        if field.name == 'full_amount' and value is None:
            raise ValueError('Укажите полную сумму!')
        return value

    class Config:
        extra = Extra.forbid
