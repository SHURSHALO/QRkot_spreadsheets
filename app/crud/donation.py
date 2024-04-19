from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User, CharityProject
from app.api.services.Invest import investing
from app.schemas.donation import DonationUpgrade, DonationCreate


class CRUDDonation(CRUDBase):

    async def get_by_user(
        self,
        user: User,
        session: AsyncSession,
    ) -> list[Donation]:
        donation_user = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return donation_user.scalars().all()

    async def create_donation(
        self, donation: DonationCreate, session: AsyncSession, user: User
    ):

        donation_project = await investing(donation, session, CharityProject)

        new_donation = await self.create(
            DonationUpgrade(**donation_project), session, user
        )

        return new_donation


donation_crud = CRUDDonation(Donation)
