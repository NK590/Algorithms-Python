"""solution.py 검증: 점화식을 한 항씩 계산하는 순진한 방법, 행렬 거듭제곱, 알려진 수열(피보나치·펠·타일링)과 무작위 점화식으로 비교"""
import io
import random
import time

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)
MOD = 10**9 + 7


def naive(coeffs, initial, n):
    seq = list(initial)
    while len(seq) <= n:
        seq.append(sum(c * seq[-1 - j] for j, c in enumerate(coeffs)))
    return seq[n]


def test_exact_integers_match_iteration():
    rng = random.Random(0)
    for _ in range(400):
        k = rng.randint(1, 6)
        coeffs = [rng.randint(-3, 4) for _ in range(k)]
        initial = [rng.randint(-5, 5) for _ in range(k)]
        n = rng.randint(0, 40)
        expected = naive(coeffs, initial, n)
        assert solution.kitamasa(coeffs, initial, n) == expected, (coeffs, initial, n)
        assert solution.bostan_mori(coeffs, initial, n) == expected, (coeffs, initial, n)
        assert solution.matrix_power_term(coeffs, initial, n) == expected, (coeffs, initial, n)


def test_modular_results_match_iteration_and_each_other():
    rng = random.Random(1)
    for _ in range(300):
        k = rng.randint(1, 7)
        mod = rng.choice([2, 3, 10, 97, 998244353, MOD])
        coeffs = [rng.randint(0, mod - 1) for _ in range(k)]
        initial = [rng.randint(0, mod - 1) for _ in range(k)]
        n = rng.randint(0, 60)
        expected = naive(coeffs, initial, n) % mod
        for function in (solution.kitamasa, solution.bostan_mori, solution.matrix_power_term):
            assert function(coeffs, initial, n, mod) == expected, (function.__name__, coeffs, initial, n, mod)


def test_huge_index_agrees_between_the_three_methods():
    rng = random.Random(2)
    for _ in range(30):
        k = rng.randint(1, 8)
        coeffs = [rng.randint(0, MOD - 1) for _ in range(k)]
        initial = [rng.randint(0, MOD - 1) for _ in range(k)]
        n = rng.randint(10**15, 10**18)
        a = solution.kitamasa(coeffs, initial, n, MOD)
        assert a == solution.bostan_mori(coeffs, initial, n, MOD) == solution.matrix_power_term(coeffs, initial, n, MOD)


def test_known_sequences():
    fib = [0, 1]
    for _ in range(100):
        fib.append(fib[-1] + fib[-2])
    assert [solution.fibonacci(i) for i in range(20)] == fib[:20]
    assert solution.fibonacci(100) == fib[100] and solution.fibonacci(90, MOD) == fib[90] % MOD
    assert solution.fibonacci(10**18, MOD) == 209783453  # F(10^18) mod 1e9+7
    pell = [0, 1]
    for _ in range(30):
        pell.append(2 * pell[-1] + pell[-2])
    assert [solution.kitamasa([2, 1], [0, 1], i) for i in range(30)] == pell[:30]
    assert solution.kitamasa([2], [1], 100) == 2**100  # k = 1
    assert solution.kitamasa([1, 1, 1], [0, 0, 1], 12) == [0, 0, 1, 1, 2, 4, 7, 13, 24, 44, 81, 149, 274][12]  # 트리보나치
    # 3 × 2k 판 타일링: f_k = 4 f_{k-1} - f_{k-2}
    assert [solution.kitamasa([4, -1], [1, 3], k) for k in range(6)] == [1, 3, 11, 41, 153, 571]


def test_sum_of_prefix_matches_summing_terms():
    rng = random.Random(3)
    for _ in range(300):
        k = rng.randint(1, 6)
        coeffs = [rng.randint(-3, 4) for _ in range(k)]
        initial = [rng.randint(-5, 5) for _ in range(k)]
        n = rng.randint(0, 40)
        expected = sum(naive(coeffs, initial, i) for i in range(n + 1))
        assert solution.sum_of_prefix(coeffs, initial, n) == expected, (coeffs, initial, n)
        mod = rng.choice([7, 1000])
        assert solution.sum_of_prefix(coeffs, initial, n, mod) == expected % mod
    assert solution.sum_of_prefix([], [], 5) == 0


def test_edge_cases_and_errors():
    assert solution.kitamasa([], [], 5) == 0 and solution.bostan_mori([], [], 5) == 0
    assert solution.kitamasa([3, 4], [7, 9], 0) == 7 and solution.kitamasa([3, 4], [7, 9], 1) == 9
    assert solution.kitamasa([3, 4], [7, 9], 1, 5) == 4  # n < k 에서도 mod 를 적용한다
    with pytest.raises(ValueError, match="initial"):
        solution.kitamasa([1, 1], [1], 5)
    with pytest.raises(ValueError, match="initial"):
        solution.bostan_mori([1, 1], [1], 5)
    with pytest.raises(ValueError, match="n 은"):
        solution.kitamasa([1, 1], [0, 1], -1)
    with pytest.raises(ValueError, match="n 은"):
        solution.bostan_mori([1, 1], [0, 1], -1)


def test_large_order_is_fast():
    rng = random.Random(4)
    k = 60
    coeffs = [rng.randint(0, MOD - 1) for _ in range(k)]
    initial = [rng.randint(0, MOD - 1) for _ in range(k)]
    started = time.perf_counter()
    a = solution.kitamasa(coeffs, initial, 10**18, MOD)
    b = solution.bostan_mori(coeffs, initial, 10**18, MOD)
    assert time.perf_counter() - started < 60
    assert a == b


def test_main_tiling_format(monkeypatch, capsys):
    for text, expected in [("2\n", 3), ("4\n", 11), ("7\n", 0), ("1000000000000000000\n", None)]:
        monkeypatch.setattr("sys.stdin", io.StringIO(text))
        solution.main()
        out = int(capsys.readouterr().out)
        if expected is not None:
            assert out == expected
        else:
            assert out == solution.kitamasa([4, -1], [1, 3], 5 * 10**17, MOD)
