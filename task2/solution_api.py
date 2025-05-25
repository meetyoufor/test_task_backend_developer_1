import requests
import csv
from collections import Counter
from collections.abc import Sequence
from datetime import datetime

from requests.exceptions import RequestException, JSONDecodeError

from constants import (
    API,
    BASE_URL,
    RU_ALPHABET,
    SCRIPT_PATH,
    START_PARAMS,
    TIMEOUT,

    EXTRACTING_DATA_TEXT,
    JSON_ERROR_TEXT,
    REQUEST_ERROR_TEXT,
    WRONG_ARG_TYPE_TEXT,
    WRONG_PARAM_TYPE_TEXT
)


def build_url(url: str, script_path: str, api: str, params: dict[str, str]) -> str:
    """Constructs a full URL by combining the components.

    :param url: The base URL of the target resource.
    :type url: `str`
    :param script_path: script path of the target resource.
    :type script_path: `str`
    :param api: The API version.
    :type api: `str`
    :param params: Dictionary containing key-value pairs representing query parameters appended to the URL.
    :type params: `dict`
    :return: A fully constructed URL ready for use in a web request.
    :rtype: `str`
    :raises TypeError: If at least one of args (or its contents) is of an invalid type or was not passed.
    """
    for name, arg in [('url', url), ('script_path', script_path), ('api', api)]:
        if not isinstance(arg, str):
            raise TypeError(WRONG_ARG_TYPE_TEXT.format(
                name=name, expected=str.__name__, type_=type(arg).__name__
                ))
    for key, value in params.items():
        if not isinstance(value, str):
            raise TypeError(WRONG_PARAM_TYPE_TEXT.format(
                key=key, expected=str.__name__, found=type(value).__name__
                ))

    base_url = '/'.join((url, script_path, api))
    query_string = '&'.join(f'{k}={v}' for k, v in params.items())
    return '?'.join((base_url, query_string))

def get_content(url: str) -> dict | None:
    """"Sends a GET request and returns the JSON-decoded content of a response, if any.

    Expected structure:
    {
        "batchcomplete": str,
        "continue": {
            "cmcontinue": str,  # next page token
            "continue": str
        },
        "query": {
            "categorymembers": [
                {
                    "pageid": int,
                    "ns": int,
                    "title": str  # animal name
                },
            ]
        }
    }

    :param url: The URL where the GET request will be sent.
    :type url: `str`
    :return: In a good case a parsed JSON object, represented as a dict. Otherwise, None.
    :rtype: `dict`, `None`
    :raises TypeError: If `url` is of the wrong type.
    """
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        response.encoding = 'utf-8'

        try:
            return response.json()
        except JSONDecodeError as e:
            print(JSON_ERROR_TEXT.format(exception=e))
            return None

    except RequestException as e:
        print(REQUEST_ERROR_TEXT.format(exception=e))
        return None

def collect_data(start_url: str) -> list[str]:
    """Collects Russian animal names from Wikipedia API.
    Performs paginated requests to extract all animal names 
    that start with Cyrillic.

    :param start_url: Initial URL with query parameters for category members.
    :type start_url: `str`
    :return: List of animal names in Cyrillic alphabet.
    :rvalue: `list`
    """
    ru_names = []
    current_url = start_url

    while True:
        if content := get_content(current_url):
            add_ru_names(ru_names, content)
            next_page = get_next_page_token(content)
            if next_page:
                current_url = '&'.join((start_url, next_page))
            else:
                break
        else:
            break

    return ru_names

def add_ru_names(data: list[str], content: dict) -> None:
    """Extracts and adds Russian animal names to the provided list.
    Filters names starting with Russian letters and appends them to the target list.

    :param data: Target list.
    :ptype data: `list`
    :param content: A dictionary containing key-value pairs, including names as values.
    :type content: `dict`
    """
    try:
        category_members = content.get('query', {}).get('categorymembers')
        if category_members:
            for member in category_members:
                name = member['title']
                if name[0].upper() in RU_ALPHABET:
                    data.append(name.upper())
                    print(name)
    except (TypeError) as e:
        print(EXTRACTING_DATA_TEXT.format(exception=e))

def get_next_page_token(content: dict[str, str | int]) -> str | None:
    """Extracts next page token from the wiki content, if any.

    :param content: A dictionary containing key-value pairs, including next page token.
    :type content: `dict`
    :return: In a good case next page token as `str`. Otherwise, None.
    :rtype: `str`, `None`
    """
    try:
        next_page_token = content.get('continue', {}).get('cmcontinue', None)
        if next_page_token:
            return f'cmcontinue={next_page_token}'
        return None
    except (TypeError) as e:
        print(EXTRACTING_DATA_TEXT.format(exception=e))

def get_first_chars(names: Sequence[str]) -> list[str] | None:
        """Returns list of first characters from names.

        :param data: Sequence of names.
        :type data: `Sequence`
        :return: In a good case list of first characters from names. If empty, returns `None`.
        :rtype: `list`, `None
        """
        return [n[0] for n in names] if names else None

def count_by_chars(chars: list[str, int]) -> Counter | None:
    """Counts occurrences of each character in the input list.
    
    :param chars: List of characters to count. If empty, returns None.
    :param type: `list`
    :return: Counter object where keys are unique characters and values are their counts. Returns None if input list is empty.
    :rtype: `Counter`, None
    """
    return Counter(chars) if chars else None

def save_to_csv(data: Counter[str, int], filename: str = 'result.csv') -> None:
    """Saves data in alphabetical order to CSV file.

    :param data: Counter object where keys are unique characters and values are their counts.
    :type data: `Counter
    """
    curr_datetime = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    file = '_'.join((curr_datetime, filename))

    with open(file, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n')
        for char in RU_ALPHABET:
            if data.get(char):
                writer.writerow((char, data.get(char)))

def main():
    """Entry point for the script.
    
    Performs the following steps:
    1. Collects Russian animal names from Wikipedia API
    2. Extracts first letters of each name
    3. Calculates letter frequencies
    4. Saves results to a timestamped CSV file
    """
    start_url = build_url(BASE_URL, SCRIPT_PATH, API, START_PARAMS)
    names = collect_data(start_url)
    if names:
        first_chars = get_first_chars(names)
        result = count_by_chars(first_chars)
        save_to_csv(result)

if __name__ == '__main__':
    main()
