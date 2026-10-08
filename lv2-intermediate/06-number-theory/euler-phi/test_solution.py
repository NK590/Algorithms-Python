"""solution.py 검증: 정의(서로소인 수를 직접 센다)와 비교 + 성질(곱셈성, 약수 합) + 오일러 정리"""
import io
import math
import random

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def phi_by_definition(n):
    return sum(1 for k in range(1, n + 1) if math.gcd(k, n) == 1)


def test_phi_matches_definition():
    for n in range(1, 600):
        assert solution.phi(n) == phi_by_definition(n), n
    assert solution.phi(1) == 1 and solution.phi(2) == 1 and solution.phi(97) == 96 and solution.phi(36) == 12
    with pytest.raises(ValueError):
        solution.phi(0)


def test_table_matches_phi():
    table = solution.phi_table(3000)
    assert table == [0] + [solution.phi(n) for n in range(1, 3001)]
    assert solution.phi_table(0) == [0] and solution.phi_table(1) == [0, 1]


def test_phi_of_prime_powers_and_multiplicativity():
    for p in (2, 3, 5, 7, 11, 13):
        for k in range(1, 6):
            assert solution.phi(p**k) == p**k - p ** (k - 1)
    rng = random.Random(0)
    for _ in range(300):
        m, n = rng.randint(1, 500), rng.randint(1, 500)
        if math.gcd(m, n) == 1:
            assert solution.phi(m * n) == solution.phi(m) * solution.phi(n)
        else:  # φ(mn) = φ(m)φ(n) · g / φ(g) 이고 g > 1 이면 g / φ(g) > 1 이다
            g = math.gcd(m, n)
            assert solution.phi(m * n) * solution.phi(g) == solution.phi(m) * solution.phi(n) * g


def test_sum_over_divisors_of_phi_is_n():
    for n in range(1, 400):
        assert sum(solution.phi(d) for d in range(1, n + 1) if n % d == 0) == n


def test_euler_theorem():
    for n in range(2, 200):
        ph = solution.phi(n)
        for a in range(1, n):
            if math.gcd(a, n) == 1:
                assert pow(a, ph, n) == 1, (a, n)


def test_pow_mod_large_exponent_matches_builtin_even_when_not_coprime():
    rng = random.Random(1)
    for _ in range(2000):
        m = rng.randint(1, 200)
        a = rng.randint(0, 300)
        e = rng.randint(0, 10**6)
        assert solution.pow_mod_large_exponent(a, e, m) == pow(a, e, m), (a, e, m)
    # 지수 자체가 매우 큰 수여도 된다
    big = 10**200 + 12345
    assert solution.pow_mod_large_exponent(6, big, 36) == pow(6, big, 36)
    assert solution.pow_mod_large_exponent(7, 5, 1) == 0


def test_count_proper_reduced_fractions():
    for n in range(1, 40):
        brute = sum(1 for q in range(2, n + 1) for p in range(1, q) if math.gcd(p, q) == 1)
        assert solution.count_proper_reduced_fractions(n) == brute, n
    assert solution.count_proper_reduced_fractions(5) == 9  # 1/2 1/3 2/3 1/4 3/4 1/5 2/5 3/5 4/5


def test_large_input_uses_square_root_time():
    assert solution.phi(10**12) == 4 * 10**11
    assert solution.phi(999_999_999_989) == 999_999_999_988  # 소수
    assert solution.phi(2**40) == 2**39


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("36\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "12"
