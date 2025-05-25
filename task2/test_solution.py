import pytest
from task2.solution_html_parse import (
    requests,
    get_content,
    RequestException
)

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

        if status_code != 200:
            mock_response.raise_for_status.side_effect = RequestException(
                f'Error: {status_code}'
            )
        else:
            mock_response.raise_for_status.return_value = None

        mock_requests_get = mocker.patch('solution.requests.get')
        mock_requests_get.return_value = mock_response

        result = get_content('http://test.url')
        assert result == expected

    def test_empty_url(self):
        assert get_content('') is None

if __name__ == '__main__':
    pytest.main([__file__])
