"""solution.py 검증: 모든 순열을 시도하는 느린 방법, 안정성 성질, 내장 sorted 와 비교"""
import io
import itertools
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def test_sort_words_by_length_then_alphabet_without_duplicates():
    words = ["but", "i", "wont", "hesitate", "no", "more", "no", "more", "it", "cannot", "wait", "im", "yours"]
    assert solution.sort_words(words) == ["i", "im", "it", "no", "but", "more", "wait", "wont", "yours", "cannot", "hesitate"]
    assert solution.sort_words([]) == []


def test_sort_words_matches_a_manual_two_step_sort():
    rng = random.Random(0)
    for _ in range(300):
        words = ["".join(rng.choice("abc") for _ in range(rng.randint(1, 4))) for _ in range(rng.randint(0, 10))]
        manual = sorted(set(words))                    # 먼저 사전순
        manual = sorted(manual, key=len)               # 그다음 길이순 (안정 정렬이라 사전순이 유지된다)
        assert solution.sort_words(words) == manual


def test_sort_points():
    assert solution.sort_points([(3, 4), (1, -1), (1, 1), (2, 2), (3, 3)]) == [(1, -1), (1, 1), (2, 2), (3, 3), (3, 4)]


def test_sort_by_age_keeps_join_order_for_equal_ages():
    members = [(21, "Junkyu"), (21, "Dohyun"), (20, "Sunyoung")]
    assert solution.sort_by_age(members) == [(20, "Sunyoung"), (21, "Junkyu"), (21, "Dohyun")]
    rng = random.Random(1)
    for _ in range(300):
        members = [(rng.randint(1, 4), f"m{i}") for i in range(rng.randint(0, 12))]
        result = solution.sort_by_age(members)
        assert [m[0] for m in result] == sorted(m[0] for m in members)
        for age in {m[0] for m in members}:
            assert [m for m in result if m[0] == age] == [m for m in members if m[0] == age]


def test_sort_digits_descending():
    assert solution.sort_digits_descending(2143) == 4321
    assert solution.sort_digits_descending(999000) == 999000
    assert solution.sort_digits_descending(0) == 0


def test_largest_number_matches_trying_every_order():
    rng = random.Random(2)
    for _ in range(400):
        numbers = [rng.choice([0, 1, 3, 5, 9, 10, 12, 30, 34, 121, 128, 999]) for _ in range(rng.randint(1, 5))]
        expected = max(int("".join(map(str, p))) for p in itertools.permutations(numbers))
        assert int(solution.largest_number(numbers)) == expected, numbers
    assert solution.largest_number([3, 30, 34, 5, 9]) == "9534330"
    assert solution.largest_number([0, 0, 0]) == "0"
    assert solution.largest_number([10, 2]) == "210"


def test_counting_sort_matches_sorted():
    rng = random.Random(3)
    for _ in range(300):
        max_value = rng.randint(0, 20)
        values = [rng.randint(0, max_value) for _ in range(rng.randint(0, 30))]
        assert solution.counting_sort(values, max_value) == sorted(values)
    assert solution.counting_sort([], 5) == []


def test_counting_sort_handles_large_input_with_small_range():
    rng = random.Random(4)
    values = [rng.randint(0, 10_000) for _ in range(300_000)]
    assert solution.counting_sort(values, 10_000) == sorted(values)


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("6\nbanana\nfig\napple\nfig\nkiwi\nplum\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["fig", "kiwi", "plum", "apple", "banana"]
