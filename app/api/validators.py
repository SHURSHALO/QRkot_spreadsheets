from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.api.constants import (
    THE_PROJECT_EXISTS,
    PROJECT_NOT_FOUND,
    PROJECT_NOT_UPDATE,
    NOT_SET_AMOUNT,
    DELETE_A_CLOSED_PROJECT,
    PROJECT_HAS_FUNDS,
)


async def check_name_duplicate(
    charity_project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        charity_project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=THE_PROJECT_EXISTS,
        )


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PROJECT_NOT_FOUND,
        )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_NOT_UPDATE,
        )
    return charity_project


async def check_full_amount_invested_amount(
    charity_project_id,
    obj_in,
    session: AsyncSession,
):
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if (
        obj_in.full_amount is not None and
        obj_in.full_amount < charity_project.invested_amount
    ):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=NOT_SET_AMOUNT,
        )


async def check_delete(charity_project):
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=DELETE_A_CLOSED_PROJECT,
        )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_HAS_FUNDS,
        )
