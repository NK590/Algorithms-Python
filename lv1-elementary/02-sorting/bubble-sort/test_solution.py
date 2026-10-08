"""solution.py 검증: README 예제 + 내장 sorted() 와의 랜덤 비교 + 안정성 + 교환 횟수(역전 수)"""
import io
import random

from tools.loader import load_solution
from tools.sorting_testing import check_is_stable, check_sorts_correctly, random_arrays

solution = load_solution(__file__)


def brute_force_inversions(arr: list) -> int:
    return sum(arr[i] > arr[j] for i in range(len(arr)) for j in range(i + 1, len(arr)))


def test_readme_example():
    arr = [5, 2, 4, 6, 1, 3]
    swaps = solution.bubble_sort(arr)
    assert arr == [1, 2, 3, 4, 5, 6]
    assert swaps == 9


def test_sorts_random_arrays():
    check_sorts_correctly(solution.bubble_sort, in_place=True)


def test_is_stable():
    check_is_stable(solution.bubble_sort, in_place=True)


def test_swap_count_equals_number_of_inversions():
    for arr in random_arrays():
        assert solution.bubble_sort(list(arr)) == brute_force_inversions(arr), arr


def test_sorted_input_needs_no_swaps_and_stops_after_one_pass():
    class Counting(list):
        reads = 0

        def __getitem__(self, i):
            Counting.reads += 1
            return super().__getitem__(i)

    arr = Counting(range(1000))
    assert solution.bubble_sort(arr) == 0
    assert list(arr) == list(range(1000))
    # 조기 종료가 없다면 약 1000 * 999 번 비교하느라 원소를 100만 번 가까이 읽는다. 한 바퀴만 돌면 2000 번 안팎이다.
    assert Counting.reads < 5000


def test_reversed_input():
    arr = list(range(50, 0, -1))
    assert solution.bubble_sort(arr) == 50 * 49 // 2
    assert arr == list(range(1, 51))


def test_main_reads_stdin_and_prints_sorted(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("4\n3\n-1\n3\n0\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["-1", "0", "3", "3"]
