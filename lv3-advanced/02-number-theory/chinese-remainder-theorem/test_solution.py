"""solution.py 검증: 한 주기 안의 모든 x 를 하나씩 대입해 본 결과와 비교"""
import io
import math
import random

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def brute_force(remainders, moduli):
    lcm = math.lcm(*moduli)
    return [x for x in range(lcm) if all(x % m == r % m for r, m in zip(remainders, moduli))], lcm


def test_crt_pair_matches_brute_force_for_every_small_case():
    for m1 in range(1, 13):
        for m2 in range(1, 13):
            for r1 in range(m1):
                for r2 in range(m2):
                    solutions, lcm = brute_force([r1, r2], [m1, m2])
                    result = solution.crt_pair(r1, m1, r2, m2)
                    if not solutions:
                        assert result is None, (r1, m1, r2, m2)
                    else:
                        assert solutions == [result[0]] and result[1] == lcm, (r1, m1, r2, m2)


def test_crt_pair_accepts_remainders_outside_the_modulus_range():
    for m1 in range(1, 9):
        for m2 in range(1, 9):
            for r1 in range(-2 * m1, 3 * m1):
                for r2 in range(-m2, 2 * m2):
                    solutions, lcm = brute_force([r1, r2], [m1, m2])
                    result = solution.crt_pair(r1, m1, r2, m2)
                    assert result == ((solutions[0], lcm) if solutions else None), (r1, m1, r2, m2)


def test_solvable_exactly_when_remainders_agree_modulo_gcd():
    for m1 in range(1, 30):
        for m2 in range(1, 30):
            g = math.gcd(m1, m2)
            for r1 in range(0, m1, 3):
                for r2 in range(0, m2, 3):
                    assert (solution.crt_pair(r1, m1, r2, m2) is not None) == ((r1 - r2) % g == 0)


def test_general_crt_matches_brute_force_with_many_equations():
    rng = random.Random(0)
    for _ in range(400):
        k = rng.randint(1, 4)
        moduli = [rng.randint(1, 12) for _ in range(k)]
        remainders = [rng.randint(-20, 20) for _ in range(k)]  # 음수나 모듈러보다 큰 값도 받는다
        solutions, lcm = brute_force(remainders, moduli)
        result = solution.crt(remainders, moduli)
        if not solutions:
            assert result is None, (remainders, moduli)
        else:
            assert result == (solutions[0], lcm) and solutions == [solutions[0]], (remainders, moduli)


def test_sunzi_problem():
    assert solution.crt([2, 3, 2], [3, 5, 7]) == (23, 105)  # 孫子算經의 '물불의 수'
    assert solution.crt_coprime([2, 3, 2], [3, 5, 7]) == (23, 105)
    assert solution.crt([], []) == (0, 1)  # 식이 없으면 모든 수가 해


def test_crt_coprime_matches_general_crt():
    rng = random.Random(1)
    pools = [3, 4, 5, 7, 9, 11, 13, 16, 17, 19, 23]
    for _ in range(200):
        moduli = rng.sample(pools, rng.randint(1, 4))
        if any(math.gcd(a, b) != 1 for i, a in enumerate(moduli) for b in moduli[i + 1 :]):
            continue
        remainders = [rng.randrange(m) for m in moduli]
        assert solution.crt_coprime(remainders, moduli) == solution.crt(remainders, moduli), (remainders, moduli)
    with pytest.raises(ValueError):
        solution.crt_coprime([1, 2], [4, 6])


def test_garner_equals_reconstructing_the_big_number():
    rng = random.Random(2)
    primes = [998244353, 1000000007, 1000000009]
    product = math.prod(primes)
    for _ in range(200):
        x = rng.randrange(product)
        remainders = [x % p for p in primes]
        for mod in (10**9 + 7, 1, 2, 12345, (1 << 61) - 1, 998244353):
            assert solution.garner(remainders, primes, mod) == x % mod, (x, mod)
        assert solution.crt_coprime(remainders, primes) == (x, product)
    with pytest.raises(ValueError):
        solution.garner([1, 1], [6, 9], 100)


def test_garner_with_small_moduli_matches_brute_force():
    moduli = [3, 5, 7, 11]
    for x in range(3 * 5 * 7 * 11):
        assert solution.garner([x % m for m in moduli], moduli, 1000) == x % 1000


def test_calendar_year_matches_simulation():
    for m in range(1, 9):
        for n in range(1, 9):
            lcm = math.lcm(m, n)
            first_seen = {}
            for year in range(1, lcm + 1):
                first_seen.setdefault(((year - 1) % m + 1, (year - 1) % n + 1), year)
            for x in range(1, m + 1):
                for y in range(1, n + 1):
                    assert solution.calendar_year(m, n, x, y) == first_seen.get((x, y), -1), (m, n, x, y)
    assert solution.calendar_year(40000, 40000 - 1, 40000, 40000 - 1) == 40000 * 39999  # 마지막 해


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("3\n10 12 3 9\n10 12 7 2\n13 11 5 6\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["33", "-1", "83"]
