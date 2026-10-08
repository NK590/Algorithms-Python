"""solution.py 검증: 구간을 직접 더한 값과 비교"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def test_readme_example():
    arr = [5, 4, 3, 2, 1]
    prefix = solution.build_prefix(arr)
    assert prefix == [0, 5, 9, 12, 14, 15]
    assert solution.range_sum(prefix, 1, 3) == 9  # 4 + 3 + 2
    assert solution.range_sum(prefix, 0, 4) == 15
    assert solution.range_sum(prefix, 2, 2) == 3


def test_every_range_matches_direct_sum():
    rng = random.Random(0)
    for _ in range(200):
        arr = [rng.randint(-9, 9) for _ in range(rng.randint(1, 12))]
        prefix = solution.build_prefix(arr)
        for left in range(len(arr)):
            for right in range(left, len(arr)):
                assert solution.range_sum(prefix, left, right) == sum(arr[left:right + 1])


def test_empty_array():
    assert solution.build_prefix([]) == [0]


def test_count_subarrays_with_sum_matches_brute_force_including_negatives():
    rng = random.Random(1)
    for _ in range(500):
        arr = [rng.randint(-3, 3) for _ in range(rng.randint(0, 12))]
        k = rng.randint(-4, 4)
        expected = sum(sum(arr[i:j]) == k for i in range(len(arr)) for j in range(i + 1, len(arr) + 1))
        assert solution.count_subarrays_with_sum(arr, k) == expected, (arr, k)


def test_apply_range_adds_matches_naive_updates():
    rng = random.Random(2)
    for _ in range(300):
        n = rng.randint(1, 12)
        updates = []
        naive = [0] * n
        for _ in range(rng.randint(0, 8)):
            left = rng.randrange(n)
            right = rng.randrange(left, n)
            value = rng.randint(-5, 5)
            updates.append((left, right, value))
            for i in range(left, right + 1):
                naive[i] += value
        assert solution.apply_range_adds(n, updates) == naive


def test_large_input_is_fast():
    n = 500_000
    prefix = solution.build_prefix(list(range(n)))
    assert solution.range_sum(prefix, 0, n - 1) == n * (n - 1) // 2


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("5 3\n5 4 3 2 1\n1 3\n2 4\n5 5\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["12", "9", "1"]
