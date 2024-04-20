THE_PROJECT_EXISTS = 'Проект с таким именем уже существует!'
PROJECT_NOT_FOUND = 'Проект не найден!'

PROJECT_NOT_UPDATE = 'Проект проинвестирован обновить нельзя!'
NOT_SET_AMOUNT = 'Невозможно установить требуемую сумму меньше уже внесенной.'

DELETE_A_CLOSED_PROJECT = 'Нельзя удалить закрытый проект'
PROJECT_HAS_FUNDS = 'Нельзя удалить проект, в который уже внесены средства'

MIN_LENGTH = 1
MAX_LENGTH = 100

FORMAT = '%Y/%m/%d %H:%M:%S'

SHEETS_SERVICE_NAME = 'sheets'
SHEETS_SERVICE_VERSION = 'v4'
SHEET_PROPERTIES = {
    'sheetType': 'GRID',
    'sheetId': 0,
    'title': 'Лист1',
    'gridProperties': {'rowCount': 100, 'columnCount': 11},
}
DRIVE_SERVICE_NAME = 'drive'
DRIVE_SERVICE_VERSION = 'v3'
