from datetime import datetime, timedelta

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.api.constants import (
    FORMAT,
    SHEETS_SERVICE_NAME,
    SHEETS_SERVICE_VERSION,
    SHEET_PROPERTIES,
    DRIVE_SERVICE_NAME,
    DRIVE_SERVICE_VERSION,
)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:

    now_date_time = datetime.now().strftime(FORMAT)

    service = await wrapper_services.discover(
        SHEETS_SERVICE_NAME, SHEETS_SERVICE_VERSION
    )

    spreadsheet_body = {
        'properties': {
            'title': f'Отчёт от {now_date_time}',
            'locale': 'ru_RU',
        },
        SHEETS_SERVICE_NAME: [{'properties': SHEET_PROPERTIES}],
    }

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
    spreadsheetid: str, wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email,
    }
    service = await wrapper_services.discover(
        DRIVE_SERVICE_NAME, DRIVE_SERVICE_VERSION
    )
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid, json=permissions_body, fields='id'
        )
    )


async def spreadsheets_update_value(
    spreadsheetid: str, charity_project: list, wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover(
        SHEETS_SERVICE_NAME, SHEETS_SERVICE_VERSION
    )

    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание'],
    ]

    for project in charity_project:
        new_row = [
            project['name'],
            str(timedelta(project['collection_time'])),
            project['description'],
        ]
        table_values.append(new_row)

    end_row = len(table_values)
    range_end = f'E{end_row}'

    update_body = {'majorDimension': 'ROWS', 'values': table_values}
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=f'A1:{range_end}',
            valueInputOption='USER_ENTERED',
            json=update_body,
        )
    )
