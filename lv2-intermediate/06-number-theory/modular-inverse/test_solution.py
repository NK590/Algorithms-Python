"""solution.py 검증: 정의(모든 후보를 시도)와 비교, 존재 조건 gcd = 1, 파이썬 내장 pow(a, -1, m) 과 비교"""
import io
import math
import random

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))


def test_inverse_exists_exactly_when_gcd_is_one():
    for m in range(1, 60):
        for a in range(0, 3 * m):
            brute = solution.inverse_brute_force(a, m)
            assert solution.has_inverse(a, m) == (brute != -1), (a, m)
            assert (math.gcd(a, m) == 1) == (brute != -1)


def test_euler_inverse_matches_brute_force_for_any_modulus():
    for m in range(1, 80):
        for a in range(1, 2 * m):
            if solution.has_inverse(a, m):
                x = solution.inverse_euler(a, m)
                assert x == solution.inverse_brute_force(a, m), (a, m)
                assert 0 <= x < m
                if m > 1:
                    assert x == pow(a, -1, m), (a, m)  # 파이썬 3.8+ 내장 모듈러 역원
            else:
                with pytest.raises(ValueError):
                    solution.inverse_euler(a, m)


def test_fermat_inverse_matches_builtin_for_primes():
    for p in (2, 3, 5, 7, 11, 13, 97, 10**9 + 7, 998244353):
        rng = random.Random(p)
        for a in [1, 2, p - 1] + [rng.randint(1, p - 1) for _ in range(20)]:
            if a % p:
                assert solution.inverse_fermat(a, p) == pow(a, -1, p), (a, p)
    with pytest.raises(ValueError):
        solution.inverse_fermat(0, 7)
    with pytest.raises(ValueError):
        solution.inverse_fermat(21, 7)


def test_fermat_inverse_is_wrong_for_composite_modulus_but_euler_is_right():
    # m = 15 는 소수가 아니므로 a^(m-2) 는 역원이 아니다. 오일러 정리는 맞다.
    assert pow(2, 15 - 2, 15) != pow(2, -1, 15)
    assert solution.inverse_euler(2, 15) == pow(2, -1, 15) == 8


def test_inverse_table_matches_individual_inverses():
    for p in (2, 3, 5, 7, 101, 10**9 + 7):
        n = min(p - 1, 2000)
        table = solution.inverse_table(n, p)
        assert len(table) == n + 1
        for i in range(1, n + 1):
            assert i * table[i] % p == 1, (i, p)
    assert solution.inverse_table(0, 7) == [0]


def test_divide_mod():
    p = 10**9 + 7
    rng = random.Random(0)
    for _ in range(200):
        a, b = rng.randint(0, 10**12), rng.randint(1, p - 1)
        q = solution.divide_mod(a, b, p)
        assert q * b % p == a % p
    # 정수 나눗셈이 정확히 떨어질 때는 같은 값
    assert solution.divide_mod(100, 4, p) == 25


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("3 7\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "5"
    monkeypatch.setattr("sys.stdin", io.StringIO("6 9\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "-1"
    monkeypatch.setattr("sys.stdin", io.StringIO("2 15\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "8"
