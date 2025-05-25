from urllib.parse import quote

# common
BASE_URL = 'https://ru.wikipedia.org'
TITLE = quote('Категория:Животные_по_алфавиту')
RU_ALPHABET = ('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')
TIMEOUT = 5

# API
SCRIPT_PATH = 'w'
API = 'api.php'
START_PARAMS = {
    'action': 'query',
    'list': 'categorymembers',
    'cmtitle': TITLE,
    'cmtype': 'page',
    'cmlimit': '500',
    'format': 'json'
}

REQUEST_ERROR_TEXT = 'There was an error that occurred while handling request: {exception}'
JSON_ERROR_TEXT = 'Response data is not JSON: {exception}'
WRONG_ARG_TYPE_TEXT = 'Argument \'{arg_name}\': expected {expected} instance, \'{found}\' found'
WRONG_PARAM_TYPE_TEXT = 'Param key \'{key}\': expected {expected} instance as value, \'{found}\' found'
EXTRACTING_DATA_TEXT = 'There was an error occurred while extracting data: {exception}'

# HTML parse
REQUEST_PART = '/wiki/' + TITLE
START_URL = BASE_URL + REQUEST_PART
