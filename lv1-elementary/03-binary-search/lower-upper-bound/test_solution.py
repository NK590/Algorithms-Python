"""solution.py 검증: bisect 와 정의를 그대로 옮긴 선형 탐색 둘 다와 비교"""
import bisect
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def sorted_array(rng):
    return sorted(rng.randint(0, 8) for _ in range(rng.randint(0, 14)))


def test_readme_example():
    arr = [1, 2, 2, 2, 5, 7]
    assert solution.lower_bound(arr, 2) == 1
    assert solution.upper_bound(arr, 2) == 4
    assert solution.count_equal(arr, 2) == 3
    assert solution.lower_bound(arr, 3) == solution.upper_bound(arr, 3) == 4  # 없는 값이면 둘이 같다
    assert solution.lower_bound(arr, 0) == 0 and solution.upper_bound(arr, 9) == 6


def test_bounds_match_bisect_and_linear_definitions():
    rng = random.Random(0)
    for _ in range(400):
        arr = sorted_array(rng)
        for x in range(-1, 10):
            assert solution.lower_bound(arr, x) == bisect.bisect_left(arr, x)
            assert solution.upper_bound(arr, x) == bisect.bisect_right(arr, x)
            first_ge = next((i for i, v in enumerate(arr) if v >= x), len(arr))
            first_gt = next((i for i, v in enumerate(arr) if v > x), len(arr))
            assert solution.lower_bound(arr, x) == first_ge and solution.upper_bound(arr, x) == first_gt
            assert solution.count_equal(arr, x) == arr.count(x)


def test_count_in_range_floor_and_ceil():
    rng = random.Random(1)
    for _ in range(400):
        arr = sorted_array(rng)
        low, high = sorted((rng.randint(-1, 9), rng.randint(-1, 9)))
        assert solution.count_in_range(arr, low, high) == sum(low <= v <= high for v in arr)
        x = rng.randint(-1, 9)
        below = [v for v in arr if v <= x]
        above = [v for v in arr if v >= x]
        assert solution.floor_value(arr, x) == (max(below) if below else None)
        assert solution.ceil_value(arr, x) == (min(above) if above else None)


def test_partition_point_on_a_function_without_an_array():
    # "제곱이 50 이상이 되는 첫 정수" = 8
    assert solution.partition_point(0, 100, lambda i: i * i >= 50) == 8
    assert solution.partition_point(0, 10, lambda i: False) == 10  # 모두 False 이면 hi
    assert solution.partition_point(0, 10, lambda i: True) == 0
    assert solution.partition_point(5, 5, lambda i: True) == 5  # 빈 구간


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("6\n1 2 2 2 5 7\n4\n2 5 3 9\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["3", "1", "0", "0"]
