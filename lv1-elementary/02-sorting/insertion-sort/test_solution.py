"""solution.py 검증: README 예제 + 내장 sorted() 와의 랜덤 비교 + 안정성"""
import io

from tools.loader import load_solution
from tools.sorting_testing import check_is_stable, check_sorts_correctly

solution = load_solution(__file__)


def test_readme_example():
    arr = [5, 2, 4, 6, 1, 3]
    solution.insertion_sort(arr)
    assert arr == [1, 2, 3, 4, 5, 6]


def test_sorts_random_arrays():
    check_sorts_correctly(solution.insertion_sort, in_place=True)


def test_is_stable():
    check_is_stable(solution.insertion_sort, in_place=True)


def test_nearly_sorted_input_needs_few_shifts():
    class Counting(list):
        writes = 0

        def __setitem__(self, i, v):
            Counting.writes += 1
            super().__setitem__(i, v)

    arr = Counting(range(2000))
    arr[10], arr[11] = arr[11], arr[10]  # 이웃한 두 원소만 뒤집힌, 거의 정렬된 입력
    Counting.writes = 0
    solution.insertion_sort(arr)
    assert list(arr) == list(range(2000))
    assert Counting.writes < 2000 * 2  # 전체를 O(n²) 으로 훑었다면 훨씬 많았을 것이다


def test_main_reads_stdin_and_prints_sorted(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("4\n3\n-1\n3\n0\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["-1", "0", "3", "3"]
