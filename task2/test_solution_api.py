import pytest

from ..task2.solution_api import (
    Counter,
    add_ru_names,
    build_url,
    count_by_chars,
    get_first_chars,
    get_next_page_token
)

class TestBuildURL:
    def test_build_url(self):
        result = build_url('http://test.url', 'w', 'apiv1', {'query': 'test', 'limit': '10'})
        assert result == 'http://test.url/w/apiv1?query=test&limit=10'

    def test_build_url_type_error(slef):
        with pytest.raises(TypeError):
            build_url(123, 'w', 'apiv1', {'query': 'test'})

# class TestGetContent: не смог написать тесты

# class TestCollectData: не смог написать тесты

class TestAddRuNames:
    def test_add_ru_names_filter_ru_letters(self):
        result = []
        expected = ["ЛЕВ", "МЕДВЕДЬ"]
        content = {'query': {'categorymembers': [{'title': 'Лев'}, {'title': 'Dog'}, {'title': 'Медведь'}]}}
        
        add_ru_names(result, content)
        assert sorted(result) == sorted(expected)

    def test_add_ru_names_empty_collection(self):
        result = []
        expected = []
        content = {'query': {'categorymembers': []}}

        add_ru_names(result, content)
        assert result == expected

class GetNextPageToken:
    def test_get_next_page_token_with_token():
        content = {
            'batchcomplete': 'text',
            'continue': {
                'cmcontinue': 'next-page-token',  # here
                'continue': 'text'
            },
            'query': {
                'categorymembers': [
                    {
                        'pageid': 1111,
                        'ns': 0,
                        'title': 'text'
                    },
                ]
            }
        }
        result = get_next_page_token(content)
        assert result == 'cmcontinue=next-page-token'

    def test_get_next_page_token_without_token():
        content = {}
        result = get_next_page_token(content)
        assert result is None

    def test_get_next_page_token_empty_response():
        content = None
        result = get_next_page_token(content)
        assert result is None

class TestGetFirstChars:
    def test_get_first_chars_with_names(self):
        assert get_first_chars(["Лев", "Крот", "Волк"]) == ["Л", "К", "В"]

    def test_get_first_chars_empty_input(self):
        assert get_first_chars([]) is None

class TestCountByChars:
    def test_count_by_chars_normal_case(self):
        assert count_by_chars(["А", "Б", "А", "В"]) == Counter({"А": 2, "Б": 1, "В": 1})

    def test_count_by_chars_empty_input(self):
        assert count_by_chars([]) is None

# class SaveToCSV: не смог написать тесты

if __name__ == '__main__':
    pytest.main()
