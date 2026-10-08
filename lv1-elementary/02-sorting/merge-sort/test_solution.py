"""solution.py 검증: README 예제 + 내장 sorted() 와의 랜덤 비교 + 안정성 + 역전 수 세기"""
import io
import random

from tools.loader import load_solution
from tools.sorting_testing import check_is_stable, check_sorts_correctly, random_arrays

solution = load_solution(__file__)


def brute_force_inversions(arr: list) -> int:
    return sum(arr[i] > arr[j] for i in range(len(arr)) for j in range(i + 1, len(arr)))


def test_readme_example():
    assert solution.merge_sort([5, 2, 4, 6, 1, 3]) == [1, 2, 3, 4, 5, 6]


def test_merge_of_two_sorted_lists():
    assert solution.merge([1, 4, 6], [2, 3, 9, 10]) == [1, 2, 3, 4, 6, 9, 10]
    assert solution.merge([], [1]) == [1]
    assert solution.merge([1], []) == [1]


def test_sorts_random_arrays():
    check_sorts_correctly(solution.merge_sort, in_place=False)


def test_is_stable():
    check_is_stable(solution.merge_sort, in_place=False)


def test_returns_a_new_list_even_for_tiny_inputs():
    arr = [7]
    assert solution.merge_sort(arr) is not arr


def test_count_inversions_matches_brute_force():
    for arr in random_arrays():
        before = list(arr)
        assert solution.count_inversions(arr) == brute_force_inversions(arr), arr
        assert arr == before


def test_count_inversions_readme_example():
    assert solution.count_inversions([5, 2, 4, 6, 1, 3]) == 9


def test_large_input_is_fast_enough_and_deep_recursion_is_not_needed():
    rng = random.Random(0)
    arr = [rng.randint(0, 10**9) for _ in range(100_000)]
    assert solution.merge_sort(arr) == sorted(arr)
    assert solution.count_inversions(list(range(2000, 0, -1))) == 2000 * 1999 // 2


def test_main_reads_stdin_and_prints_sorted(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("4\n3\n-1\n3\n0\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["-1", "0", "3", "3"]
