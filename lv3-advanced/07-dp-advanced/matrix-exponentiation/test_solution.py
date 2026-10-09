"""solution.py 검증: 점화식을 하나씩 계산하는 순진한 방법, 반복 곱셈, 경로를 직접 세는 DP 와 비교"""
import io
import random
import time

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)

MOD = 1_000_000_007


def fib_list(n):
    values = [0, 1]
    while len(values) <= n:
        values.append(values[-1] + values[-2])
    return values


def naive_matmul(a, b, mod=None):
    n = len(a)
    result = [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    return [[v % mod for v in row] for row in result] if mod else result


def test_mat_mul_matches_the_definition_and_is_associative():
    rng = random.Random(0)
    for _ in range(200):
        n = rng.randint(1, 5)
        a, b, c = ([[rng.randint(-5, 5) for _ in range(n)] for _ in range(n)] for _ in range(3))
        assert solution.mat_mul(a, b) == naive_matmul(a, b)
        assert solution.mat_mul(solution.mat_mul(a, b), c) == solution.mat_mul(a, solution.mat_mul(b, c))
        assert solution.mat_mul(a, b, 7) == naive_matmul(a, b, 7)


def test_mat_pow_matches_repeated_multiplication():
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(1, 4)
        a = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(n)]
        e = rng.randint(0, 12)
        expected = solution.mat_identity(n)
        for _ in range(e):
            expected = naive_matmul(expected, a)
        assert solution.mat_pow(a, e) == expected, (a, e)
        mod = rng.choice([2, 7, 1000])
        assert solution.mat_pow(a, e, mod) == [[v % mod for v in row] for row in expected]


def test_mat_pow_edge_cases_and_errors():
    assert solution.mat_pow([[2, 3], [4, 5]], 0) == [[1, 0], [0, 1]]
    assert solution.mat_pow([[2, 3], [4, 5]], 1) == [[2, 3], [4, 5]]
    assert solution.mat_pow([[2, 3], [4, 5]], 5, 1) == [[0, 0], [0, 0]]  # 모든 수의 나머지가 0
    assert solution.mat_pow([[2, 3], [4, 5]], 0, 1) == [[0, 0], [0, 0]]  # 나머지가 1 이면 단위 행렬도 0
    assert solution.mat_pow([[2]], 10) == [[1024]]
    assert solution.mat_pow([[-3]], 3, 7) == [[(-27) % 7]]
    with pytest.raises(ValueError, match="지수"):
        solution.mat_pow([[1]], -1)
    with pytest.raises(ValueError, match="정사각"):
        solution.mat_pow([[1, 2]], 2)
    with pytest.raises(ValueError, match="크기"):
        solution.mat_mul([[1]], [[1, 0], [0, 1]])


def test_fibonacci_both_ways_match_the_list():
    values = fib_list(300)
    for n in range(300):
        assert solution.fibonacci_matrix(n) == values[n], n
        assert solution.fibonacci_doubling(n) == values[n], n
        assert solution.fibonacci_matrix(n, MOD) == values[n] % MOD
        assert solution.fibonacci_doubling(n, MOD) == values[n] % MOD
    assert solution.fibonacci_matrix(90) == 2880067194370816120
    with pytest.raises(ValueError):
        solution.fibonacci_matrix(-1)
    with pytest.raises(ValueError):
        solution.fibonacci_doubling(-1)


def test_huge_fibonacci_agree_and_match_a_known_value():
    assert solution.fibonacci_matrix(1000, MOD) == 517691607  # F(1000)의 알려진 나머지
    for n in [10**9, 10**18, 2**60 - 1, 10**18 + 7]:
        assert solution.fibonacci_matrix(n, MOD) == solution.fibonacci_doubling(n, MOD)
    # F(n) mod p 는 주기(피사노 주기)가 있다: F(n + period) 가 같다.  mod 10 의 주기는 60
    assert all(solution.fibonacci_matrix(n, 10) == solution.fibonacci_matrix(n + 60, 10) for n in range(0, 100, 7))


def test_linear_recurrence_nth_matches_iteration():
    rng = random.Random(2)
    for _ in range(300):
        k = rng.randint(1, 5)
        coeffs = [rng.randint(-3, 3) for _ in range(k)]
        initial = [rng.randint(-4, 4) for _ in range(k)]
        sequence = list(initial)
        for m in range(k, 40):
            sequence.append(sum(coeffs[i] * sequence[m - 1 - i] for i in range(k)))
        for n in range(40):
            assert solution.linear_recurrence_nth(coeffs, initial, n) == sequence[n], (coeffs, initial, n)
            assert solution.linear_recurrence_nth(coeffs, initial, n, 1000) == sequence[n] % 1000
    # 피보나치와 트리보나치
    assert solution.linear_recurrence_nth([1, 1], [0, 1], 50) == fib_list(50)[50]
    assert solution.linear_recurrence_nth([1, 1, 1], [0, 0, 1], 10) == 81
    assert solution.linear_recurrence_nth([2], [3], 10) == 3 * 2**10
    with pytest.raises(ValueError, match="초기값"):
        solution.linear_recurrence_nth([1, 1], [0], 5)
    with pytest.raises(ValueError, match="초기값"):
        solution.linear_recurrence_nth([], [], 5)
    with pytest.raises(ValueError, match="0 이상"):
        solution.linear_recurrence_nth([1], [1], -1)


def test_recurrence_prefix_sum_matches_iteration():
    rng = random.Random(3)
    for _ in range(300):
        k = rng.randint(1, 4)
        coeffs = [rng.randint(-2, 3) for _ in range(k)]
        initial = [rng.randint(-3, 3) for _ in range(k)]
        sequence = list(initial)
        for m in range(k, 30):
            sequence.append(sum(coeffs[i] * sequence[m - 1 - i] for i in range(k)))
        for n in range(30):
            assert solution.recurrence_prefix_sum(coeffs, initial, n) == sum(sequence[: n + 1]), (coeffs, initial, n)
            assert solution.recurrence_prefix_sum(coeffs, initial, n, 97) == sum(sequence[: n + 1]) % 97
    assert solution.recurrence_prefix_sum([1, 1], [0, 1], 10) == fib_list(12)[12] - 1  # Σ F(0..n) = F(n+2) - 1
    with pytest.raises(ValueError):
        solution.recurrence_prefix_sum([1], [1, 2], 3)
    with pytest.raises(ValueError, match="0 이상"):
        solution.recurrence_prefix_sum([1], [1], -1)


def test_count_walks_matches_dynamic_programming():
    rng = random.Random(4)
    for _ in range(200):
        n = rng.randint(1, 6)
        adj = [[rng.randint(0, 2) for _ in range(n)] for _ in range(n)]
        length = rng.randint(0, 8)
        # 시작 정점마다 길이를 하나씩 늘려 가며 센다
        for start in range(n):
            ways = [1 if v == start else 0 for v in range(n)]
            for _ in range(length):
                ways = [sum(ways[u] * adj[u][v] for u in range(n)) for v in range(n)]
            assert solution.count_walks(adj, length)[start] == ways, (adj, length, start)
    # 완전 그래프 K3 의 닫힌 경로: 길이 3 이면 대각선 2
    triangle = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
    assert [solution.count_walks(triangle, 3)[i][i] for i in range(3)] == [2, 2, 2]
    assert solution.count_walks(triangle, 0) == solution.mat_identity(3)


def test_longest_walks_matches_dynamic_programming():
    rng = random.Random(5)
    for _ in range(300):
        n = rng.randint(1, 5)
        weights = [[rng.choice([None, None, rng.randint(-3, 9)]) for _ in range(n)] for _ in range(n)]
        length = rng.randint(0, 7)
        result = solution.longest_walks(weights, length)
        for start in range(n):
            best = [0 if v == start else None for v in range(n)]
            for _ in range(length):
                nxt = [None] * n
                for u in range(n):
                    if best[u] is None:
                        continue
                    for v in range(n):
                        if weights[u][v] is not None and (nxt[v] is None or best[u] + weights[u][v] > nxt[v]):
                            nxt[v] = best[u] + weights[u][v]
                best = nxt
            assert result[start] == best, (weights, length, start)
    assert solution.longest_walks([[5]], 4) == [[20]]
    assert solution.longest_walks([[None]], 3) == [[None]]
    assert solution.longest_walks([[None]], 0) == [[0]]
    with pytest.raises(ValueError, match="0 이상"):
        solution.longest_walks([[1]], -1)


def test_large_exponents_are_fast():
    started = time.perf_counter()
    k = 20
    rng = random.Random(6)
    coeffs = [rng.randint(0, 5) for _ in range(k)]
    initial = [rng.randint(0, 5) for _ in range(k)]
    solution.linear_recurrence_nth(coeffs, initial, 10**18, MOD)
    solution.fibonacci_matrix(10**18, MOD)
    assert time.perf_counter() - started < 15


def test_main_prints_fibonacci_mod(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("1000\n"))
    solution.main()
    assert capsys.readouterr().out == "517691607\n"
    monkeypatch.setattr("sys.stdin", io.StringIO("0\n"))
    solution.main()
    assert capsys.readouterr().out == "0\n"
