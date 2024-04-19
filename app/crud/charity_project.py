from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpgrade,
)
from app.models import Donation
from app.api.services.Invest import investing


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(self.model.id).where(self.model.name == project_name)
        )
        return db_project_id.scalars().first()

    async def create_project(
        self,
        project: CharityProjectCreate,
        session: AsyncSession,
    ):

        charity_project = await investing(project, session, Donation)

        new_charity_project = await self.create(
            CharityProjectUpgrade(**charity_project), session
        )
        return new_charity_project

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> list[dict[str, str]]:
        """Получение и сортировка закрытых проектов и генерация отчета."""
        closed_projects = await session.execute(
            select(
                [
                    self.model.name,
                    (
                        func.julianday(self.model.close_date) -
                        func.julianday(self.model.create_date)
                    ).label('collection_time'),
                    self.model.description,
                ]
            )
            .where(self.model.fully_invested)
            .order_by('collection_time')
        )
        projects = closed_projects.all()
        return projects


charity_project_crud = CRUDCharityProject(CharityProject)
