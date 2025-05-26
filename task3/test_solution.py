import pytest

from ..task3.solution import get_person_events, appearance

class TestGetPersonEvents:
    def test_get_person_events_basic(self):
        intervals = [10, 20, 30, 40]
        result = get_person_events(intervals, 'P', 0, 50)
        assert result == [(10, 1, 'P'), (20, -1, 'P'), (30, 1, 'P'), (40, -1, 'P')]

    def test_get_person_events_outside(self):
        intervals = [5, 15, 25, 35]
        result = get_person_events(intervals, 'T', 10, 30)
        assert result == [(10, 1, 'T'), (15, -1, 'T'), (25, 1, 'T'), (30, -1, 'T')]

    def test_get_person_events_partial_overlap(self):
        intervals = [5, 25, 35, 45]
        result = get_person_events(intervals, 'T', 10, 40)
        assert result == [(10, 1, 'T'), (25, -1, 'T'), (35, 1, 'T'), (40, -1, 'T')]

class TestAppearance:
    def test_appearance_simple_overlap(self):
        intervals = {
            'lesson': [10, 30],
            'pupil':  [5, 25],
            'tutor':  [20, 25]
        }
        assert appearance(intervals) == 5

    def test_appearance_flush(self):
        intervals = {
            'lesson': [10, 20],
            'pupil':  [10, 20],
            'tutor':  [10, 20]
        }
        assert appearance(intervals) == 10

    def test_appearance_empty_intervals(self):
        intervals = {
            'lesson': [10, 20],
            'pupil':  [15, 18],
            'tutor':  []
        }
        assert appearance(intervals) == 0

    def test_appearance_offset(self):
        intervals = {
            'lesson': [0, 100],
            'pupil':  [10, 20, 30, 40, 50, 60],
            'tutor':  [15, 25, 35, 45, 55, 65]
        }
        assert appearance(intervals) == 15

    def test_appearance_difficult_case(self):
        intervals = {
            'lesson': [10, 50],
            'pupil':  [5,  15, 20, 30, 35, 45],
            'tutor':  [12, 18, 25, 40]
        }
        assert appearance(intervals) == 13

if __name__ == '__main__':
    pytest.main()
