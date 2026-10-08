"""solution.py 검증: 구간을 직접 잘라 정렬하고 세는 순진한 방법과 무작위 배열(음수·중복 포함)·구간으로 비교"""
import io
import random
import time

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def random_range(rng, n):
    left = rng.randint(0, n)
    return left, rng.randint(left, n)


def test_access_and_kth_match_sorting():
    rng = random.Random(0)
    for _ in range(200):
        n = rng.randint(1, 40)
        spread = rng.choice([1, 2, 5, 40])
        values = [rng.randint(-spread, spread) for _ in range(n)]
        matrix = solution.WaveletMatrix(values)
        assert [matrix.access(i) for i in range(n)] == values
        for _ in range(30):
            left = rng.randrange(n)
            right = rng.randint(left + 1, n)
            k = rng.randint(1, right - left)
            assert matrix.kth_smallest(left, right, k) == sorted(values[left:right])[k - 1], (values, left, right, k)
            assert matrix.median(left, right) == sorted(values[left:right])[(right - left + 1) // 2 - 1]


def test_counts_sums_predecessor_successor_match_brute_force():
    rng = random.Random(1)
    for _ in range(200):
        n = rng.randint(0, 35)
        spread = rng.choice([1, 3, 10, 40])
        values = [rng.randint(-spread, spread) for _ in range(n)]
        matrix = solution.WaveletMatrix(values)
        for _ in range(40):
            left, right = random_range(rng, n)
            piece = values[left:right]
            x = rng.randint(-spread - 2, spread + 2)
            low, high = sorted((rng.randint(-spread - 2, spread + 2), rng.randint(-spread - 2, spread + 2)))
            assert matrix.count_less(left, right, x) == sum(1 for v in piece if v < x)
            assert matrix.count_at_most(left, right, x) == sum(1 for v in piece if v <= x)
            assert matrix.count_equal(left, right, x) == piece.count(x)
            assert matrix.count_in_range(left, right, low, high) == sum(1 for v in piece if low <= v <= high)
            assert matrix.count_in_range(left, right, high + 1, low) == 0  # low > high 인 범위는 비어 있다
            assert matrix.sum_less(left, right, x) == sum(v for v in piece if v < x)
            assert matrix.predecessor(left, right, x) == max((v for v in piece if v < x), default=None)
            assert matrix.successor(left, right, x) == min((v for v in piece if v > x), default=None)
            k = rng.randint(0, len(piece))
            assert matrix.sum_smallest(left, right, k) == sum(sorted(piece)[:k]), (values, left, right, k)


def test_a_threshold_beyond_every_value_counts_everything():
    # 값이 하나뿐이거나 순위 비트 수의 한계(2의 거듭제곱)에 딱 맞는 경우
    for distinct in (1, 2, 3, 4, 5, 8, 9):
        values = list(range(distinct)) * 2
        matrix = solution.WaveletMatrix(values)
        n = len(values)
        assert matrix.count_less(0, n, 10**9) == n and matrix.count_less(0, n, -10**9) == 0
        assert matrix.sum_less(0, n, 10**9) == sum(values)
        assert matrix.count_at_most(0, n, distinct - 1) == n
        assert matrix.kth_smallest(0, n, n) == distinct - 1 and matrix.kth_smallest(0, n, 1) == 0


def test_bounds_and_empty_input():
    matrix = solution.WaveletMatrix([3, 1, 2])
    assert matrix.count_less(1, 1, 100) == 0 and matrix.sum_less(2, 2, 100) == 0 and matrix.sum_smallest(0, 0, 0) == 0
    with pytest.raises(IndexError, match="구간"):
        matrix.count_less(0, 4, 1)
    with pytest.raises(IndexError, match="구간"):
        matrix.count_less(2, 1, 1)
    with pytest.raises(IndexError, match="index 가"):
        matrix.access(3)
    with pytest.raises(IndexError, match="index 가"):
        matrix.access(-1)
    with pytest.raises(ValueError, match="k 가"):
        matrix.kth_smallest(0, 3, 0)
    with pytest.raises(ValueError, match="k 가"):
        matrix.kth_smallest(0, 3, 4)
    with pytest.raises(ValueError, match="k 가"):
        matrix.sum_smallest(0, 3, 4)
    empty = solution.WaveletMatrix([])
    assert empty.count_less(0, 0, 5) == 0 and empty.predecessor(0, 0, 5) is None and empty.successor(0, 0, 5) is None


def test_layer_structure_is_a_stable_partition_by_bit():
    rng = random.Random(2)
    values = [rng.randint(0, 30) for _ in range(50)]
    matrix = solution.WaveletMatrix(values)
    assert len(matrix.zeros) == matrix.height == (len(matrix.values) - 1).bit_length()
    for t in range(matrix.height):
        assert len(matrix.zeros[t]) == len(values) + 1 and matrix.zeros[t][0] == 0
        assert matrix.zero_total[t] == matrix.zeros[t][-1]
    assert matrix.prefix_sums[-1][-1] == sum(values)


def test_large_input_is_fast_and_correct():
    rng = random.Random(3)
    n = 200000
    values = [rng.randint(-10**9, 10**9) for _ in range(n)]
    started = time.perf_counter()
    matrix = solution.WaveletMatrix(values)
    answers = []
    queries = []
    for _ in range(20000):
        left = rng.randrange(n)
        right = rng.randint(left + 1, n)
        k = rng.randint(1, right - left)
        queries.append((left, right, k))
        answers.append(matrix.kth_smallest(left, right, k))
    assert time.perf_counter() - started < 30
    for (left, right, k), answer in list(zip(queries, answers))[:5]:
        assert answer == sorted(values[left:right])[k - 1]


def test_main_range_kth_smallest_format(monkeypatch, capsys):
    text = "5 3\n5 1 4 2 3\n0 5 0\n1 4 1\n2 3 0\n"
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(text.encode())))
    solution.main()
    assert capsys.readouterr().out == "1\n2\n4\n"
