"""solution.py 검증: 시행 나눗셈, 곱해서 다시 확인, 르장드르 공식, 알려진 소인수분해와 비교"""
import io
import math
import random
import time

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def trial_factorize(n):
    result = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            result[p] = result.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        result[n] = result.get(n, 0) + 1
    return result


def product(factors):
    value = 1
    for p, e in factors.items():
        value *= p**e
    return value


def next_prime_above(n):
    m = n + 1
    while not solution.is_prime(m):
        m += 1
    return m


def test_factorize_matches_trial_division_for_every_number_up_to_20000():
    for n in range(1, 20001):
        assert solution.factorize(n) == trial_factorize(n), n
    assert solution.factorize(1) == {}


def test_factors_are_prime_and_multiply_back_for_random_composites():
    rng = random.Random(0)
    for _ in range(100):
        primes = [next_prime_above(rng.randint(2, 10**6)) for _ in range(rng.randint(1, 5))]
        n = 1
        for p in primes:
            n *= p
        factors = solution.factorize(n)
        assert product(factors) == n
        assert all(trial_factorize(p) == {p: 1} for p in factors)
        assert sorted(factors) == sorted(set(primes))


def test_semiprimes_of_two_31_bit_primes_split_quickly():
    rng = random.Random(1)
    started = time.perf_counter()
    for _ in range(5):
        p = next_prime_above(rng.randint(2**30, 2**31))
        q = next_prime_above(rng.randint(2**30, 2**31))
        n = p * q
        assert solution.factorize(n) == dict(sorted({p: 1, q: 1}.items()) if p != q else {p: 2})
        assert solution.prime_factors(n) == sorted([p, q])
    assert time.perf_counter() - started < 20


def test_prime_powers_squares_and_cubes_of_big_primes():
    big = next_prime_above(10**9)
    assert solution.factorize(big**2) == {big: 2}
    assert solution.factorize(big**3) == {big: 3}
    assert solution.factorize(2**62) == {2: 62}
    assert solution.factorize(3**39) == {3: 39}
    assert solution.factorize((10**6 + 3) ** 3 * (10**6 + 33)) == {10**6 + 3: 3, 10**6 + 33: 1}
    assert solution.factorize(2**61 - 1) == {2**61 - 1: 1}


def test_known_factorisations():
    assert solution.factorize(600851475143) == {71: 1, 839: 1, 1471: 1, 6857: 1}
    assert solution.factorize(10**18) == {2: 18, 5: 18}
    assert solution.factorize(2**64 + 1) == {274177: 1, 67280421310721: 1}  # 페르마 수 F6
    assert solution.factorize(561) == {3: 1, 11: 1, 17: 1}  # 카마이클 수
    assert solution.factorize(341550071728321) == {10670053: 1, 32010157: 1}  # 시행 나눗셈으로도 확인한 값 (밑 2..17 의 강한 의사소수)


def test_legendre_formula_for_a_factorial_and_a_primorial_like_product():
    n = 60
    factorial = math.factorial(n)
    legendre = {}
    for p in range(2, n + 1):
        if all(p % q for q in range(2, int(p**0.5) + 1)):
            e, power = 0, p
            while power <= n:
                e += n // power
                power *= p
            legendre[p] = e
    assert solution.factorize(factorial) == legendre
    rng = random.Random(2)
    primes = [next_prime_above(rng.randint(2**39, 2**40)) for _ in range(6)]
    big = 1
    for p in primes:
        big *= p
    started = time.perf_counter()
    assert solution.factorize(big) == dict(sorted({p: 1 for p in primes}.items()))
    assert time.perf_counter() - started < 20


def test_pollard_rho_returns_a_proper_divisor():
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randint(4, 10**15)
        if solution.is_prime(n):
            with pytest.raises(ValueError, match="합성수"):
                solution.pollard_rho(n)
            continue
        d = solution.pollard_rho(n)
        assert 1 < d < n and n % d == 0, (n, d)
    assert solution.pollard_rho(10**6) == 2  # 짝수
    assert solution.pollard_rho(49) == 7  # 완전제곱
    for bad in (-5, 0, 1, 2, 3):
        with pytest.raises(ValueError, match="합성수"):
            solution.pollard_rho(bad)


def test_pollard_rho_retries_with_a_new_constant_when_brent_fails(monkeypatch):
    calls = []

    def fake_brent(n, c, rng, batch=128):
        calls.append(c)
        return n if c < 3 else 5  # 처음 두 번은 실패(약수가 n 자체), 세 번째에서 성공

    monkeypatch.setattr(solution, "_brent", fake_brent)
    assert solution.pollard_rho(15) == 5
    assert calls == [1, 2, 3]  # c 를 1 씩 늘려 가며 다시 시도한다


def test_squares_of_big_primes_are_split_without_a_special_case():
    for p in (10**9 + 7, 999999937, 2**31 - 1):
        d = solution.pollard_rho(p * p)
        assert d == p, p
        assert solution.factorize(p * p) == {p: 2}


def test_factorize_validation():
    for bad in (0, -1, -100):
        with pytest.raises(ValueError, match="1 이상"):
            solution.factorize(bad)


def test_divisors_count_sum_and_phi_match_brute_force():
    for n in range(1, 1500):
        expected = [d for d in range(1, n + 1) if n % d == 0]
        assert solution.divisors(n) == expected, n
        assert solution.count_divisors(n) == len(expected), n
        assert solution.sum_divisors(n) == sum(expected), n
        assert solution.euler_phi(n) == sum(1 for k in range(1, n + 1) if math.gcd(k, n) == 1), n
    p, q = 1000003, 998244353
    assert solution.euler_phi(p * q) == (p - 1) * (q - 1)
    assert solution.count_divisors(2**10 * 3**5 * 5**2) == 11 * 6 * 3
    assert solution.sum_divisors(10**12) == ((2**13 - 1) * (5**13 - 1) // 4)


def test_is_prime_is_the_miller_rabin_from_the_previous_concept():
    flags = [True] * 5001
    flags[0] = flags[1] = False
    for i in range(2, 71):
        if flags[i]:
            for j in range(i * i, 5001, i):
                flags[j] = False
    assert all(solution.is_prime(n) == flags[n] for n in range(5001))
    assert solution.is_prime(2**127 - 1, random.Random(0))
    assert not solution.is_prime(2**127 + 1, random.Random(0))


def test_main_prints_each_prime_factor_on_its_own_line(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("18\n"))
    solution.main()
    assert capsys.readouterr().out == "2\n3\n3\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(f"{2**62 - 57}\n"))
    solution.main()
    out = capsys.readouterr().out.split()
    assert math.prod(int(x) for x in out) == 2**62 - 57
