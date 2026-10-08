"""solution.py 검증: README 예제 + 내장 sorted() 와의 랜덤 비교 + 중복값·정렬된 입력 + quick_select"""
import io
import random

import pytest

from tools.loader import load_solution
from tools.sorting_testing import check_sorts_correctly, random_arrays

solution = load_solution(__file__)


def test_readme_example():
    assert solution.quick_sort([5, 2, 4, 6, 1, 3]) == [1, 2, 3, 4, 5, 6]
    arr = [5, 2, 4, 6, 1, 3]
    solution.quick_sort_inplace(arr)
    assert arr == [1, 2, 3, 4, 5, 6]


def test_quick_sort_sorts_random_arrays():
    check_sorts_correctly(solution.quick_sort, in_place=False)


def test_quick_sort_inplace_sorts_random_arrays():
    check_sorts_correctly(solution.quick_sort_inplace, in_place=True)


@pytest.mark.parametrize("sort_fn, in_place", [(solution.quick_sort, False), (solution.quick_sort_inplace, True)])
def test_duplicates_and_already_sorted_inputs_do_not_blow_up(sort_fn, in_place):
    # 값이 모두 같은 입력, 이미 정렬된(또는 역순인) 입력은 기준값 선택이 나쁘면 O(n²) 이나 재귀 폭주가 일어나는 대표 사례다.
    n = 20_000
    for arr in ([7] * n, list(range(n)), list(range(n, 0, -1)), [1, 2] * (n // 2)):
        expected = sorted(arr)
        result = list(arr)
        if in_place:
            sort_fn(result)
        else:
            result = sort_fn(arr)
        assert result == expected


def test_partition_splits_into_smaller_equal_larger():
    rng = random.Random(0)
    for _ in range(300):
        arr = [rng.randint(0, 5) for _ in range(rng.randint(1, 12))]
        before = sorted(arr)
        lt, gt = solution._partition(arr, 0, len(arr) - 1)
        pivot = arr[lt]
        assert sorted(arr) == before  # 원소를 잃거나 늘리지 않는다
        assert all(x < pivot for x in arr[:lt])
        assert all(x == pivot for x in arr[lt:gt + 1])
        assert all(x > pivot for x in arr[gt + 1:])


def test_quick_select_matches_sorted():
    rng = random.Random(1)
    for arr in random_arrays():
        for k in range(len(arr)):
            before = list(arr)
            assert solution.quick_select(arr, k) == sorted(arr)[k], (arr, k)
            assert arr == before
    big = [rng.randint(0, 10**6) for _ in range(5000)]
    assert solution.quick_select(big, 2500) == sorted(big)[2500]


def test_quick_select_rejects_out_of_range_k():
    with pytest.raises(IndexError):
        solution.quick_select([1, 2, 3], 3)
    with pytest.raises(IndexError):
        solution.quick_select([], 0)


def test_main_reads_stdin_and_prints_sorted(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("4\n3\n-1\n3\n0\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["-1", "0", "3", "3"]
