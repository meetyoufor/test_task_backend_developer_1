import csv
import requests

from collections import Counter
from collections.abc import Sequence
from datetime import datetime

from bs4 import BeautifulSoup
from requests.exceptions import RequestException

from constants import (
    BASE_URL,
    START_URL,
    TIMEOUT,
    RU_ALPHABET,

    REQUEST_ERROR_TEXT
)

def get_content(url: str) -> str | None:
    """"Sends a GET request and returns the HTML content of a response as text, if any.

    :param url: The URL where the GET request will be sent.
    :type url: `str`
    :return: In a good case a markup content, represented as text. Otherwise, None.
    :rtype: `dict`, `None`
    :raises TypeError: If `url` is of the wrong type.
    """
    try:
        if url:
            response = requests.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response.text
    except RequestException as e:
        print(REQUEST_ERROR_TEXT.format(exception=e))
        return None

def add_ru_names(data: list[str], soup: BeautifulSoup) -> None:
    """Extracts and adds Russian animal names to the provided list.
    Filters names starting with Russian letters and appends them to the target list.

    :param data: An names list.
    :ptype data: `list`
    :param content: Data structure representing a parsed HTML.
    :type content: `BeautifulSoup`
    """
    category_div = soup.find('div', class_='mw-category mw-category-columns')
    if category_div:
        for link in category_div.find_all('a'):
            if title := link.get('title'):
                name = title.upper()
                if name[0] in RU_ALPHABET:
                    data.append(name)
                    print(name)

def get_next_page_url(soup: BeautifulSoup) -> str | None:
    """Extracts link of the next page from parsed HTML if found and constructs URL.

    :param content: Data structure representing a parsed HTML.
    :type content: `BeautifulSoup`
    :return: Next page URL if found. Otherwise, None.
    :rtype: `str`, `None`
    """
    link = soup.find('a', string='Следующая страница')
    return BASE_URL + link['href'] if link else None

def collect_data(start_url: str) -> list[str] | None:
    """Collects Russian animal names from Wikipedia.
    Performs paginated requests to extract all animal names 
    that start with Cyrillic.

    :param start_url: Initial URL with query parameters.
    :type start_url: `str`
    :return: List of animal names in Cyrillic alphabet.
    :rvalue: `list`
    """
    ru_names = []
    current_url = start_url

    while True:
        if content := get_content(current_url):
            soup = BeautifulSoup(content, 'html.parser')
            add_ru_names(ru_names, soup)
            current_url = get_next_page_url(soup)
        else:
            break

    return ru_names

def get_first_chars(names: Sequence[str]) -> list[str] | None:
        """Returns list of first characters from animal names.

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
    1. Collects Russian animal names from Wikipedia
    2. Extracts first letters of each name
    3. Calculates letter frequencies
    4. Saves results to a timestamped CSV file
    """
    start_url = START_URL
    names = collect_data(start_url)  # Сначала получаем 'список всех животных' в соответствии с заданием
    if names:
        first_chars = get_first_chars(names)  # Потом получаем список первых букв (можно было сразу получить список букв, отработало бы быстрее)
        result = count_by_chars(first_chars)
        save_to_csv(result)

if __name__ == '__main__':
    main()
