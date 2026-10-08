"""solution.py 검증: 정의대로 소인수분해한 μ, 모든 쌍을 gcd 로 확인하는 완전 탐색, 체와 비교"""
import io
import math
import random
import time

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def mu_by_definition(n):
    if n == 1:
        return 1
    count = 0
    p = 2
    while p * p <= n:
        if n % p == 0:
            n //= p
            if n % p == 0:
                return 0
            count += 1
        p += 1
    if n > 1:
        count += 1
    return -1 if count % 2 else 1


def test_mobius_sieve_matches_the_definition():
    mu = solution.mobius_sieve(3000)
    assert mu[0] == 0 and mu[1] == 1
    for n in range(1, 3001):
        assert mu[n] == mu_by_definition(n) == solution.mobius(n), n
    assert solution.mobius_sieve(0) == [0] and solution.mobius_sieve(1) == [0, 1]
    assert solution.mobius_sieve(10) == [0, 1, -1, -1, 0, -1, 1, -1, 0, 0, 1]
    with pytest.raises(ValueError, match="1 이상"):
        solution.mobius(0)


def test_sum_of_mu_over_divisors_is_one_only_for_n_equal_one():
    mu = solution.mobius_sieve(2000)
    for n in range(1, 2001):
        assert sum(mu[d] for d in range(1, n + 1) if n % d == 0) == (1 if n == 1 else 0), n


def test_divisor_sum_transform_and_its_inverse():
    rng = random.Random(0)
    for _ in range(100):
        size = rng.randint(2, 120)
        f = [0] + [rng.randint(-20, 20) for _ in range(size - 1)]
        big_f = solution.divisor_sum_transform(f)
        for n in range(1, size):
            assert big_f[n] == sum(f[d] for d in range(1, n + 1) if n % d == 0), n
        assert solution.inverse_divisor_sum_transform(big_f) == f
        mu = solution.mobius_sieve(size - 1)
        for n in range(1, size):  # 반전 공식을 정의대로
            assert f[n] == sum(mu[n // d] * big_f[d] for d in range(1, n + 1) if n % d == 0), n


def test_the_index_zero_slot_of_the_transforms_is_ignored_and_returned_as_zero():
    assert solution.divisor_sum_transform([99, 1, 1, 1]) == [0, 1, 2, 2]
    assert solution.inverse_divisor_sum_transform([99, 1, 2, 2]) == [0, 1, 1, 1]


def test_euler_phi_table_matches_counting_coprimes():
    phi = solution.euler_phi_table(400)
    for n in range(1, 401):
        assert phi[n] == sum(1 for k in range(1, n + 1) if math.gcd(k, n) == 1), n
    assert phi[0] == 0


def test_coprime_pair_counts_match_brute_force_and_each_other():
    for n in range(0, 61):
        expected = sum(1 for a in range(1, n + 1) for b in range(1, n + 1) if math.gcd(a, b) == 1)
        assert solution.count_coprime_pairs(n) == expected, n
        assert solution.count_coprime_pairs_fast(n) == expected, n
    assert solution.count_coprime_pairs(10) == 63
    for n in (100, 997, 1000, 2000):
        assert solution.count_coprime_pairs_fast(n) == solution.count_coprime_pairs(n), n
    mu_prefix = solution.mertens_prefix(solution.mobius_sieve(500))
    assert solution.count_coprime_pairs_fast(500, mu_prefix) == solution.count_coprime_pairs(500)
    assert solution.count_coprime_pairs_fast(37, mu_prefix) == solution.count_coprime_pairs(37)  # 더 큰 표를 받아도 된다


def test_mertens_prefix():
    prefix = solution.mertens_prefix(solution.mobius_sieve(12))
    assert prefix == [0, 1, 0, -1, -1, -2, -1, -2, -2, -2, -1, -2, -2]


def test_pairs_with_a_given_gcd():
    for n in range(0, 25):
        for m in range(0, 25):
            for g in (1, 2, 3, 5):
                expected = sum(1 for a in range(1, n + 1) for b in range(1, m + 1) if math.gcd(a, b) == g)
                assert solution.count_pairs_with_gcd(n, m, g) == expected, (n, m, g)
    with pytest.raises(ValueError, match="g 는"):
        solution.count_pairs_with_gcd(5, 5, 0)


def test_count_coprime_to_matches_counting():
    for m in range(1, 150):
        for n in (0, 1, 7, 30, 101):
            expected = sum(1 for k in range(1, n + 1) if math.gcd(k, m) == 1)
            assert solution.count_coprime_to(n, m) == expected, (n, m)
    # 30 의 주기마다 서로소가 8 개 (1, 7, 11, 13, 17, 19, 23, 29). 10^12 = 30·33333333333 + 10 이고 나머지 1..10 중 서로소는 1, 7 두 개
    assert solution.count_coprime_to(10**12, 30) == 33333333333 * 8 + 2
    with pytest.raises(ValueError, match="m 은"):
        solution.count_coprime_to(10, 0)


def test_count_squarefree_matches_a_sieve():
    def sieve_count(n):
        flags = bytearray([1]) * (n + 1)
        for d in range(2, math.isqrt(n) + 1):
            flags[d * d :: d * d] = bytearray(len(flags[d * d :: d * d]))
        return sum(flags[1:])

    for n in list(range(0, 400)) + [10**4, 99999, 10**6]:
        assert solution.count_squarefree(n) == (sieve_count(n) if n >= 1 else 0), n
    assert solution.count_squarefree(-5) == 0 and solution.count_squarefree(0) == 0
    assert solution.count_squarefree(10**6) == 607926
    assert solution.count_squarefree(10**14) / 10**14 == pytest.approx(6 / math.pi**2, abs=1e-6)  # 밀도 6/π²


def test_gcd_sums():
    for n in range(1, 120):
        assert solution.sum_of_gcds(n) == sum(math.gcd(i, n) for i in range(1, n + 1)), n
        assert solution.sum_gcd_all_pairs(n) == sum(math.gcd(a, b) for a in range(1, n + 1) for b in range(1, n + 1)), n
    assert solution.sum_of_gcds(12) == 1 + 2 + 3 + 4 + 1 + 6 + 1 + 4 + 3 + 2 + 1 + 12


def test_large_n_uses_the_block_decomposition_quickly():
    started = time.perf_counter()
    big = solution.count_coprime_pairs_fast(10**6)
    assert time.perf_counter() - started < 20
    assert big / 10**12 == pytest.approx(6 / math.pi**2, abs=1e-5)  # 서로소일 확률 6/π²
    phi = solution.euler_phi_table(1000)
    assert solution.count_coprime_pairs_fast(1000) == 2 * sum(phi[1:]) - 1  # 순서쌍 = 2·Σφ - 1


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("10\n"))
    solution.main()
    assert capsys.readouterr().out == "63\n"
