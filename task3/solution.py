from .constants import TESTS

def get_person_events(
        person_intervals: list[int],
        tag: str,
        lesson_start: int,
        lesson_end: int
        ) -> list[tuple[int, int, str]]:
    events = []
    for i in range(0, len(person_intervals), 2):
        start = max(person_intervals[i], lesson_start)
        end = min(person_intervals[i+1], lesson_end)
        if start < end:
            events.append((start, 1, tag))
            events.append((end, -1, tag))
    return events

def appearance(intervals: dict[str, list[int]]) -> int:
    start_lesson, end_lesson = intervals['lesson']

    pupil = get_person_events(intervals['pupil'], 'P', start_lesson, end_lesson)
    tutor = get_person_events(intervals['tutor'], 'T', start_lesson, end_lesson)

    events = []
    events.extend(pupil)
    events.extend(tutor)
    events.sort()

    total = 0
    p_count = 0
    t_count = 0
    prev_time = None

    for time, event, person in events:
        if p_count > 0 and t_count > 0 and prev_time is not None:
            total += time - prev_time

        if person == 'P':
            p_count += event
        if person == 'T':
            t_count += event

        prev_time = time

    return total

if __name__ == '__main__':
    for i, test in enumerate(TESTS):
        appearance(test['intervals'])
        test_answer = appearance(test['intervals'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
