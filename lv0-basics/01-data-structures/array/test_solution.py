"""solution.py 검증: 내장 list 연산과의 랜덤 비교"""
import io
import random

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def random_list(rng):
    return [rng.randint(-5, 5) for _ in range(rng.randint(0, 10))]


def test_insert_at_matches_list_insert():
    rng = random.Random(0)
    for _ in range(300):
        arr = random_list(rng)
        index = rng.randint(0, len(arr))
        expected = list(arr)
        expected.insert(index, 99)
        solution.insert_at(arr, index, 99)
        assert arr == expected


def test_delete_at_matches_list_pop():
    rng = random.Random(1)
    for _ in range(300):
        arr = random_list(rng)
        if not arr:
            continue
        index = rng.randrange(len(arr))
        expected = list(arr)
        value = expected.pop(index)
        assert solution.delete_at(arr, index) == value
        assert arr == expected


def test_out_of_range_indices_raise():
    with pytest.raises(IndexError):
        solution.insert_at([1, 2], 3, 0)
    with pytest.raises(IndexError):
        solution.insert_at([1, 2], -1, 0)
    with pytest.raises(IndexError):
        solution.delete_at([1, 2], 2)
    with pytest.raises(IndexError):
        solution.delete_at([], 0)


def test_reverse_in_place_whole_and_range():
    arr = [1, 2, 3, 4, 5]
    solution.reverse_in_place(arr)
    assert arr == [5, 4, 3, 2, 1]
    arr = [1, 2, 3, 4, 5]
    solution.reverse_in_place(arr, 1, 3)
    assert arr == [1, 4, 3, 2, 5]
    arr = []
    solution.reverse_in_place(arr)
    assert arr == []


def test_rotate_left_matches_slicing():
    rng = random.Random(2)
    for _ in range(300):
        arr = random_list(rng)
        k = rng.randint(0, 25)
        expected = arr[k % len(arr):] + arr[:k % len(arr)] if arr else []
        solution.rotate_left(arr, k)
        assert arr == expected


def test_max_with_index_returns_first_maximum():
    assert solution.max_with_index([3, 9, 2, 9, 1]) == (9, 1)
    assert solution.max_with_index([-4]) == (-4, 0)
    with pytest.raises(ValueError):
        solution.max_with_index([])


def test_max_with_index_matches_builtin():
    rng = random.Random(3)
    for _ in range(300):
        arr = random_list(rng) or [0]
        value, index = solution.max_with_index(arr)
        assert value == max(arr) and arr.index(value) == index


def test_main_prints_min_and_max(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("5\n20 10 35 30 7\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["7", "35"]
