from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation
from app.schemas.charity_project import CharityProjectUpdate
from app.schemas.donation import DonationCreate


async def investing(
    obj: Union[DonationCreate, CharityProjectUpdate],
    session: AsyncSession,
    model: Union[Donation, CharityProject],
):

    active_objects = await session.execute(
        select(model).where(model.fully_invested == 0)
    )
    active_objects = active_objects.scalars().all()

    donation_amount = obj.full_amount
    donation_to_invested_amount = 0

    for active_object in active_objects:

        full_amount = active_object.full_amount

        obj_invested_amount = active_object.invested_amount + donation_amount

        def sum_with_limit(limit: int, value: int) -> tuple[int, int]:
            return (
                min(limit, value),
                max(0, value - limit),
            )

        result, remainder = sum_with_limit(full_amount, obj_invested_amount)

        amount_of_donation = donation_amount - remainder

        active_object.invested_amount += amount_of_donation
        donation_to_invested_amount += amount_of_donation

        if result == full_amount:
            active_object.fully_invested = True
            active_object.close_date = datetime.now()

        donation_amount = remainder

        if donation_amount == 0:
            break

    obj_in_data = obj.dict()
    obj_in_data['invested_amount'] = donation_to_invested_amount

    if obj_in_data['full_amount'] == obj_in_data['invested_amount']:
        obj_in_data.update(
            {'fully_invested': True, 'close_date': datetime.now()}
        )

    return obj_in_data
