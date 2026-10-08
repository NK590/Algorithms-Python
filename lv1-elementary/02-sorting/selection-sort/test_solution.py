"""solution.py 검증: README 예제 + 내장 sorted() 와의 랜덤 비교 + 불안정 정렬 예시"""
import io

from tools.loader import load_solution
from tools.sorting_testing import Keyed, check_sorts_correctly

solution = load_solution(__file__)


def test_readme_example():
    arr = [5, 2, 4, 6, 1, 3]
    solution.selection_sort(arr)
    assert arr == [1, 2, 3, 4, 5, 6]


def test_sorts_random_arrays():
    check_sorts_correctly(solution.selection_sort, in_place=True)


def test_is_not_stable_example_from_readme():
    # 같은 값 2 두 개(2#0, 2#1)와 1 하나: 1 을 맨 앞으로 보내려고 2#0 과 맞바꾸면 2 들의 순서가 뒤집힌다.
    items = [Keyed(2, 0), Keyed(2, 1), Keyed(1, 2)]
    solution.selection_sort(items)
    assert [(x.key, x.id) for x in items] == [(1, 2), (2, 1), (2, 0)]


def test_makes_at_most_n_minus_1_swaps():
    class Counting(list):
        swaps = 0

        def __setitem__(self, i, v):
            Counting.swaps += 1
            super().__setitem__(i, v)

    arr = Counting(range(100, 0, -1))
    solution.selection_sort(arr)
    assert list(arr) == list(range(1, 101))
    assert Counting.swaps <= 2 * 99  # 교환 한 번에 대입 두 번


def test_main_reads_stdin_and_prints_sorted(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("4\n3\n-1\n3\n0\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["-1", "0", "3", "3"]
