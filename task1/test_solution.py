import pytest
from task2.solution_html_parse import strict, TYPE_ERROR_TEXT

def test_strict_correct_types():
    @strict
    def sum_two(a: int, b: int) -> int:
        return a + b

    assert sum_two(1, 2) == 3
    assert sum_two(a=1, b=2) == 3

def test_strict_incorrect_args():
    @strict
    def concat_two(s1: str, s2: str) -> str:
        return f'{s1} {s2}' 

    with pytest.raises(TypeError) as e_message:
        concat_two('Hello', 1)

    assert e_message.value.args[0] == TYPE_ERROR_TEXT.format(
        argument='s2', correct_type='str', wrong_type='int'
    )

def test_strict_incorrect_kwargs():
    @strict
    def sum_two(a: float, b: float) -> float:
        return a + b

    with pytest.raises(TypeError) as exc_info:
        sum_two(a=1.0, b="2.0")

    assert exc_info.value.args[0] == TYPE_ERROR_TEXT.format(
        argument='b', correct_type='float', wrong_type='str'
    )

def test_strict_no_annotations():
    @strict
    def no_annotations(a, b):
        return a + b

    assert no_annotations(1, 2) == 3
    assert no_annotations(a='a', b='b') == 'ab'

def test_strict_partial_annotations():
    @strict
    def partial_annotations(a: int, b):
        return a + b

    assert partial_annotations(1, 2) == 3
    assert partial_annotations(1, 2.0) == 3.0

    with pytest.raises(TypeError):
        partial_annotations(1.0, 2)

if __name__ == '__main__':
    pytest.main([__file__])
