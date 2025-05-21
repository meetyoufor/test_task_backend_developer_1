import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from collections import Counter

from constans import (
    BASE_URL,
    START_URL,
    TIMEOUT_VALUE,
    RU_ALPHABET
)

def get_content(url: str, timeout: int = TIMEOUT_VALUE) -> str | None:
    if not url:
        return None
    
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response.text
    except RequestException as e:
        print(f'Error: {e}')
        return None

def add_animal_name(animals: list[str], soup: BeautifulSoup) -> bool:
    category_div = soup.find('div', class_='mw-category mw-category-columns')
    if category_div:
        for link in category_div.find_all('a'):
            if title := link.get('title'):
                animal_name = title.upper()
                if animal_name[0] in RU_ALPHABET:
                    animals.append(animal_name)
                    print(animal_name)

def get_next_page_url(soup: BeautifulSoup) -> str | None:
    next_link = soup.find('a', string='Следующая страница')
    if next_link:
        return BASE_URL + next_link['href']
    return None

def collect_data(start_url: str) -> list[str] | None:
    animals = []
    current_url = start_url

    while True:
        if content := get_content(current_url):
            soup = BeautifulSoup(content, 'html.parser')
            add_animal_name(animals, soup)
            current_url = get_next_page_url(soup)
        else:
            break

    return animals

def get_first_chars(animal_names: list[str]) -> list[str]:
    first_chars = [i[0] for i in animal_names]
    return first_chars

def count_by_first_chars(first_chars: list[str]) -> Counter[str, int]:
    return Counter(first_chars)

def save_to_csv(data: Counter[str, int], filename: str = 'result.csv') -> None:
    with open(filename, 'w', encoding='utf-8') as file:
        for char in RU_ALPHABET:
            if data.get(char):
                file.write(f'{char},{data.get(char)}\n')

def main():
    url = START_URL
    data = collect_data(url)  # Сначала получаем 'список всех животных' в соответствии с заданием
    first_letters = get_first_chars(data)  # Потом получаем список первых букв (можно было сразу получить список букв, отработало бы быстрее)
    result = count_by_first_chars(first_letters)
    save_to_csv(result)

if __name__ == '__main__':
    main()
