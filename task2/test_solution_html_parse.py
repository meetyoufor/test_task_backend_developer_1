import pytest

from ..task2.solution_html_parse import (
    BeautifulSoup,
    Counter,
    add_ru_names,
    collect_data,
    count_by_chars,
    get_content,
    get_first_chars,
    get_next_page_url,
    RequestException,
    BASE_URL
)

@pytest.fixture
def mock_html_content_next_page():
    html = '''
        <html>
            <head><title>Test Page</title></head>
            <body>
                <div class="mw-category mw-category-columns">
                    <ul>
                        <li><a href="#" title="Амурский тигр"></a></li>
                        <li><a href="#" title="Белый медведь"></a></li>
                        <li><a href="#" title="African elephant"></a></li>
                        <li><a href="#" title="Lion"></a></li>
                        <li><a href="#" title="Шимпанзе"></a></li>
                    </ul>
                </div>
                <nav>
                    <a href="/next-page/" rel="next" title="Next page">Следующая страница</a>
                </nav>
            </body>
        </html>
        '''
    return BeautifulSoup(html, 'html.parser')

@pytest.fixture
def mock_html_no_content_no_next_page():
    html = '''
    <html>
        <head><title>Test Page</title></head>
        <body>
            <div class="another-class">
                <ul>
                    <li><a href="#" title="No animals here"></a></li>
                </ul>
            </div>
            <nav>
                <a href="/previous-page/" rel="prev" title="Previous page">Предыдущая страница</a>
            </nav>
        </body>
    </html>
    '''
    return BeautifulSoup(html, 'html.parser')

@pytest.fixture
def mock_html_no_ru_titels():
    html = '''
        <html>
            <head><title>Test Page</title></head>
            <body>
                <div class="mw-category mw-category-columns">
                    <ul>
                        <li><a href="#" title="Tiger"></a></li>
                        <li><a href="#" title="African elephant"></a></li>
                        <li><a href="#" title="Lion"></a></li>
                    </ul>
                </div>
            </body>
        </html>
        '''
    return BeautifulSoup(html, 'html.parser')

class TestGetContent:
    @pytest.mark.parametrize(
        'status_code,text,expected',
        [
            (200, 'Lorem ipsum', 'Lorem ipsum'),
            (404, 'Lorem ipsum',  None),
            (500, 'Lorem ipsum',  None)
        ]
    )
    def test_get_content_response(self, mocker, text, status_code, expected):
        mock_response = mocker.Mock()
        mock_response.text = text
        mock_response.status_code = status_code

        if status_code == 200:
            mock_response.raise_for_status.return_value = None
        else:
            mock_response.raise_for_status.side_effect = RequestException(
                f'Error: {status_code}'
            )

        mocker.patch('tetrika.task2.solution_html_parse.requests.get', return_value=mock_response)

        result = get_content('http://test.url')
        assert result == expected

    def test_empty_url(self):
        assert get_content('') is None

class TestAddRuNames:
    def test_add_ru_names(self, mock_html_content_next_page):
        result = []
        expected = ['АМУРСКИЙ ТИГР', 'БЕЛЫЙ МЕДВЕДЬ', 'ШИМПАНЗЕ']
        add_ru_names(result, mock_html_content_next_page)
        assert sorted(result) == sorted(expected)

    def test_add_ru_names_no_category(self, mock_html_no_content_no_next_page):
        result = []
        expected = []
        add_ru_names(result, mock_html_no_content_no_next_page)
        assert result == expected

    def test_add_ru_names_no_ru_titels(self, mock_html_no_ru_titels):
        result = []
        expected = []
        add_ru_names(result, mock_html_no_ru_titels)
        assert result == expected

class TestGetNextPageURL:
    def test_get_next_page_url_with_link(self, mock_html_content_next_page):
        result = get_next_page_url(mock_html_content_next_page)
        expected = BASE_URL + '/next-page/'
        assert result == expected

    def test_get_next_page_url_without_link(self, mock_html_no_content_no_next_page):
        result = get_next_page_url(mock_html_no_content_no_next_page)
        expected = None 
        assert result == expected

class TestCollectData:
    def test_collect_data_returns_list_on_success(self, mocker, mock_html_content_next_page):
        mocker.patch(
            'tetrika.task2.solution_html_parse.get_content',
            side_effect=[mock_html_content_next_page.prettify(), None]
            )
        
        mocker.patch(
            'tetrika.task2.solution_html_parse.get_next_page_url',
            side_effect=["/next-page/", None]
            )
        
        result = collect_data("http://test.com")
        
        assert isinstance(result, list)
        assert len(result) > 0
        assert "АМУРСКИЙ ТИГР" in result

    def test_collect_data_handles_no_content(self, mocker):
        mocker.patch('tetrika.task2.solution_html_parse.get_content', return_value=None)
        
        result = collect_data("http://test.com")
        assert len(result) == 0

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

if __name__ == '__main__':
    pytest.main()
