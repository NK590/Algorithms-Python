"""solution.py 검증: README 예제 + 내장 sorted() 와의 랜덤 비교 + 힙 성질"""
import io
import random

from tools.loader import load_solution
from tools.sorting_testing import check_sorts_correctly

solution = load_solution(__file__)


def is_max_heap(arr: list, size: int) -> bool:
    return all(arr[(i - 1) // 2] >= arr[i] for i in range(1, size))


def test_readme_example():
    arr = [5, 2, 4, 6, 1, 3]
    solution.heap_sort(arr)
    assert arr == [1, 2, 3, 4, 5, 6]


def test_sorts_random_arrays():
    check_sorts_correctly(solution.heap_sort, in_place=True)


def test_regression_for_the_old_child_index_bug():
    # 이전 구현은 자식 인덱스를 2*i, 2*i+1 로 계산해서 이 입력이 [1, 2, 3, 4, 5, 7, 6] 으로 정렬됐다.
    arr = [1, 2, 3, 4, 5, 6, 7]
    solution.heap_sort(arr)
    assert arr == [1, 2, 3, 4, 5, 6, 7]


def test_sift_down_restores_the_heap_property():
    rng = random.Random(0)
    for _ in range(300):
        n = rng.randint(1, 15)
        arr = [rng.randint(0, 20) for _ in range(n)]
        for i in range(n // 2 - 1, -1, -1):  # 아래에서 위로 올라가며 정리하면 전체가 힙이 된다
            solution._sift_down(arr, i, n)
        assert is_max_heap(arr, n), arr


def test_large_input():
    rng = random.Random(0)
    arr = [rng.randint(0, 10**9) for _ in range(50_000)]
    expected = sorted(arr)
    solution.heap_sort(arr)
    assert arr == expected


def test_main_reads_stdin_and_prints_sorted(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("4\n3\n-1\n3\n0\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["-1", "0", "3", "3"]
