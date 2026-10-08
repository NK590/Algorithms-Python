"""solution.py 검증: 모든 쌍/모든 구간을 보는 O(n²) 풀이와 비교"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def test_pair_with_sum_sorted_matches_brute_force():
    rng = random.Random(0)
    for _ in range(600):
        arr = sorted(rng.randint(-6, 6) for _ in range(rng.randint(0, 9)))
        target = rng.randint(-10, 10)
        result = solution.pair_with_sum_sorted(arr, target)
        exists = any(arr[i] + arr[j] == target for i in range(len(arr)) for j in range(i + 1, len(arr)))
        if exists:
            i, j = result
            assert i < j and arr[i] + arr[j] == target
        else:
            assert result is None, (arr, target)


def test_readme_example_pair():
    assert solution.pair_with_sum_sorted([1, 2, 4, 7, 11, 15], 15) == (2, 4)
    assert solution.pair_with_sum_sorted([1, 2, 4], 100) is None


def test_count_subarrays_with_sum_matches_brute_force():
    rng = random.Random(1)
    for _ in range(600):
        arr = [rng.randint(1, 5) for _ in range(rng.randint(0, 12))]
        target = rng.randint(1, 15)
        expected = sum(sum(arr[i:j]) == target for i in range(len(arr)) for j in range(i + 1, len(arr) + 1))
        assert solution.count_subarrays_with_sum(arr, target) == expected, (arr, target)


def test_shortest_subarray_at_least_matches_brute_force():
    rng = random.Random(2)
    for _ in range(600):
        arr = [rng.randint(1, 5) for _ in range(rng.randint(0, 12))]
        s = rng.randint(1, 20)
        lengths = [j - i for i in range(len(arr)) for j in range(i + 1, len(arr) + 1) if sum(arr[i:j]) >= s]
        assert solution.shortest_subarray_at_least(arr, s) == (min(lengths) if lengths else 0), (arr, s)


def test_readme_example_shortest_subarray():
    assert solution.shortest_subarray_at_least([2, 3, 1, 2, 4, 3], 7) == 2  # [4, 3]
    assert solution.shortest_subarray_at_least([1, 1, 1], 10) == 0


def test_merge_sorted_matches_sorted():
    rng = random.Random(3)
    for _ in range(300):
        a = sorted(rng.randint(0, 9) for _ in range(rng.randint(0, 8)))
        b = sorted(rng.randint(0, 9) for _ in range(rng.randint(0, 8)))
        assert solution.merge_sorted(a, b) == sorted(a + b)


def test_linear_time_on_large_input():
    n = 200_000
    arr = [1] * n
    assert solution.count_subarrays_with_sum(arr, 5) == n - 4
    assert solution.shortest_subarray_at_least(arr, n) == n
    assert solution.pair_with_sum_sorted(list(range(n)), 2 * n - 3) == (n - 2, n - 1)


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("5 5\n1 2 3 2 3\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "3"
