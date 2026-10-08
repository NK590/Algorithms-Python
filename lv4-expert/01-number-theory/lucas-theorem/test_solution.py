"""solution.py 검증: math.comb 로 정확히 계산한 값, 파스칼 항등식, 올림 세기와 비교"""
import io
import math
import random
import time

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23]


def test_lucas_matches_exact_binomials_for_small_primes():
    for p in PRIMES:
        for n in range(0, 160):
            for k in range(0, n + 1):
                assert solution.lucas(n, k, p) == math.comb(n, k) % p, (n, k, p)
    assert solution.lucas(5, 6, 7) == 0 and solution.lucas(5, -1, 7) == 0
    with pytest.raises(ValueError, match="소수"):
        solution.lucas(10, 3, 9)
    with pytest.raises(ValueError, match="소수"):
        solution.lucas(10, 3, 1)


def test_lucas_matches_exact_values_for_moderately_large_n():
    rng = random.Random(0)
    for _ in range(120):
        n = rng.randint(1000, 30000)
        k = rng.randint(0, n)
        p = rng.choice([2, 3, 7, 13, 101, 997])
        assert solution.lucas(n, k, p) == math.comb(n, k) % p, (n, k, p)


def test_known_identities_for_huge_arguments():
    for p in (2, 3, 5, 7, 101):
        for a in (1, 2, 5, 9, 20):
            top = p**a - 1
            for k in {0, 1, 2, top // 2, top - 1, top}:
                if k <= top:
                    assert solution.lucas(top, k, p) == (-1) ** k % p, (p, a, k)  # C(p^a - 1, k) ≡ (-1)^k
            for k in {1, 2, p**a // 2, p**a - 1}:
                if 0 < k < p**a:
                    assert solution.lucas(p**a, k, p) == 0, (p, a, k)  # 0 < k < p^a 이면 0
            assert solution.lucas(p**a, 0, p) == solution.lucas(p**a, p**a, p) == 1
    rng = random.Random(1)
    for _ in range(300):  # p = 2: C(n, k) 가 홀수 ⟺ k 의 켜진 비트가 n 의 켜진 비트의 부분집합
        n = rng.getrandbits(rng.randint(1, 62))
        k = rng.randint(0, n)
        assert solution.lucas(n, k, 2) == (1 if k & n == k else 0), (n, k)
    assert solution.lucas(10**18, 10**9, 998244353) == solution.lucas(10**18, 10**18 - 10**9, 998244353)


def test_pascals_rule_holds_for_huge_n_and_composite_moduli():
    rng = random.Random(2)
    for _ in range(80):
        n = rng.randint(10**15, 10**18)
        k = rng.randint(1, 10**9)
        m = rng.choice([6, 12, 30, 72, 1000, 360, 4, 8, 9, 27, 49, 1_000_000])
        left = solution.binomial_mod(n, k, m)
        right = (solution.binomial_mod(n - 1, k - 1, m) + solution.binomial_mod(n - 1, k, m)) % m
        assert left == right, (n, k, m)


def test_kummer_valuation_counts_carries():
    for p in (2, 3, 5, 7):
        for n in range(0, 120):
            for k in range(0, n + 1):
                value = math.comb(n, k)
                expected = 0
                while value % p == 0:
                    value //= p
                    expected += 1
                assert solution.kummer_valuation(n, k, p) == expected, (n, k, p)
    with pytest.raises(ValueError, match="0 ≤ k ≤ n"):
        solution.kummer_valuation(3, 5, 2)
    assert solution.digit_sum(255, 2) == 8 and solution.digit_sum(255, 16) == 30 and solution.digit_sum(0, 10) == 0


def test_prime_power_moduli_match_exact_values():
    for p, e in [(2, 1), (2, 2), (2, 3), (2, 5), (3, 2), (3, 3), (5, 2), (5, 3), (7, 2), (11, 2)]:
        pe = p**e
        for n in range(0, 90):
            for k in range(0, n + 1):
                assert solution.binomial_prime_power(n, k, p, e) == math.comb(n, k) % pe, (n, k, p, e)
    assert solution.binomial_prime_power(5, 7, 2, 3) == 0
    with pytest.raises(ValueError, match="소수"):
        solution.binomial_prime_power(5, 2, 4, 2)
    with pytest.raises(ValueError, match="e 는"):
        solution.binomial_prime_power(5, 2, 2, 0)


def test_general_moduli_match_exact_values():
    for m in list(range(1, 70)) + [100, 360, 1000, 4096, 2310, 9999]:
        for n in range(0, 70):
            for k in range(0, n + 1):
                assert solution.binomial_mod(n, k, m) == math.comb(n, k) % m, (n, k, m)
    assert solution.binomial_mod(5, 9, 10) == 0 and solution.binomial_mod(5, -1, 10) == 0
    with pytest.raises(ValueError, match="m 은"):
        solution.binomial_mod(5, 2, 0)


def test_general_moduli_on_big_n_against_exact_values():
    rng = random.Random(3)
    for _ in range(40):
        n = rng.randint(2000, 12000)
        k = rng.randint(0, n)
        m = rng.choice([360, 1000, 4096, 12345, 65536, 3**7, 5**4 * 7])
        assert solution.binomial_mod(n, k, m) == math.comb(n, k) % m, (n, k, m)


def test_catalan_numbers_mod_m():
    catalan = [1]
    for n in range(0, 60):
        catalan.append(catalan[-1] * 2 * (2 * n + 1) // (n + 2))
    for m in (2, 7, 10, 12, 1000, 998244353, 1_000_000_007):
        for n in range(0, 61):
            assert solution.catalan_mod(n, m) == catalan[n] % m, (n, m)
    with pytest.raises(ValueError, match="n 은"):
        solution.catalan_mod(-1, 7)
    assert solution.catalan_mod(10**15, 1) == 0


def test_a_huge_prime_modulus_works_when_the_digits_are_small():
    # p 가 TABLE_LIMIT 보다 크면 표를 만들지 않고 곱으로 계산한다: n 이 p 보다 작으면 한 자리
    p = 998244353
    for n, k in [(10, 3), (100, 50), (1000, 1), (1000, 999), (500, 250)]:
        assert solution.lucas(n, k, p) == math.comb(n, k) % p, (n, k)
    assert solution.lucas(10**9 + 100, 5, p) == math.comb(10**9 + 100, 5) % p  # 두 자리 (n = 1·p + 1755747)
    assert solution._small_binomial(30, 15, p) == math.comb(30, 15) % p


def test_speed_for_a_large_prime_and_for_a_prime_power():
    started = time.perf_counter()
    solution.lucas(4 * 10**18, 2 * 10**18, 1999)
    solution.binomial_mod(10**18, 10**9, 2**20)
    solution.binomial_mod(10**18, 10**17, 3**12)
    assert time.perf_counter() - started < 20


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("10 3 7\n"))
    solution.main()
    assert capsys.readouterr().out == f"{math.comb(10, 3) % 7}\n"
    monkeypatch.setattr("sys.stdin", io.StringIO("4000000000000000000 2000000000000000000 1999\n"))
    solution.main()
    assert capsys.readouterr().out == f"{solution.lucas(4 * 10**18, 2 * 10**18, 1999)}\n"
