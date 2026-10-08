"""solution.py 검증: 최소 소인수 체로 모든 m 의 f(m) 을 직접 계산한 접두사 합, 소수 체와 비교"""
import io
import random
import time
from math import isqrt

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)
LIMIT = 200000


def smallest_prime_factors(limit):
    spf = list(range(limit + 1))
    for i in range(2, isqrt(limit) + 1):
        if spf[i] == i:
            for j in range(i * i, limit + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf


SPF = smallest_prime_factors(LIMIT)


def factorize(m):
    result = []
    while m > 1:
        p = SPF[m]
        e = 0
        while m % p == 0:
            m //= p
            e += 1
        result.append((p, e))
    return result


def prefix_sums(f_prime_power, limit=LIMIT):
    """f(1) = 1, f(m) = Π f(p^e) 로 모든 m ≤ limit 의 접두사 합 (접두사 합 리스트 반환)."""
    prefix = [0, 1]
    for m in range(2, limit + 1):
        value = 1
        for p, e in factorize(m):
            value *= f_prime_power(p, e)
        prefix.append(prefix[-1] + value)
    return prefix


def totient_pp(p, e):
    return p ** (e - 1) * (p - 1)


def sigma_pp(p, e):
    return sum(p ** i for i in range(e + 1))


def mobius_pp(p, e):
    return -1 if e == 1 else 0


TOTIENT, SIGMA, MOBIUS = prefix_sums(totient_pp), prefix_sums(sigma_pp), prefix_sums(mobius_pp)


def sieve_primes(limit):
    flags = bytearray([1]) * (limit + 1)
    flags[0:2] = b"\x00\x00"[:min(2, limit + 1)]
    for i in range(2, isqrt(limit) + 1):
        if flags[i]:
            flags[i * i::i] = bytearray(len(flags[i * i::i]))
    return flags


def interesting_values(rng):
    values = list(range(0, 130))
    for p in (2, 3, 5, 7, 11, 13, 97, 101, 211, 353):  # 소수의 제곱 근처 (재귀의 경계)
        values += [p * p - 1, p * p, p * p + 1, p ** 3 - 1, p ** 3, p * (p + 1)]
    values += [rng.randrange(130, LIMIT) for _ in range(40)]
    return [v for v in values if v <= LIMIT]


def test_prime_count_and_sum_match_a_sieve():
    rng = random.Random(0)
    flags = sieve_primes(LIMIT)
    count_prefix, sum_prefix = [0], [0]
    for v in range(1, LIMIT + 1):
        count_prefix.append(count_prefix[-1] + flags[v])
        sum_prefix.append(sum_prefix[-1] + (v if flags[v] else 0))
    for n in interesting_values(rng):
        assert solution.prime_count(n) == count_prefix[n], n
        assert solution.prime_sum(n) == sum_prefix[n], n
    assert solution.prime_count(-5) == 0 and solution.prime_sum(1) == 0


def test_larger_prime_tables_match_a_sieve():
    flags = sieve_primes(5 * 10**6)
    assert solution.prime_count(5 * 10**6) == sum(flags)
    assert solution.prime_sum(5 * 10**6) == sum(i for i, f in enumerate(flags) if f)
    assert solution.prime_count(10**6) == 78498


def test_totient_sigma_mobius_sums_match_direct_computation():
    rng = random.Random(1)
    for n in interesting_values(rng):
        assert solution.sum_totient(n) == TOTIENT[n], n
        assert solution.sum_sigma(n) == SIGMA[n], n
        assert solution.sum_mobius(n) == MOBIUS[n], n
    assert solution.sum_totient(10**6) == 303963552392
    assert solution.sum_mobius(10**6) == 212


def test_n_of_zero_one_and_negative():
    assert solution.sum_totient(0) == 0 and solution.sum_totient(-3) == 0
    assert solution.sum_totient(1) == 1 and solution.sum_sigma(1) == 1 and solution.sum_mobius(1) == 1
    assert solution.min25_sum(1, [5], lambda p, e: 5, mod=1) == 0
    assert solution.min25_sum(1, [5], lambda p, e: 5, mod=7) == 1


def test_generic_multiplicative_functions_with_random_prime_values():
    """f(p) 는 p 의 0~2 차 다항식, f(p^e) 는 e 에 따라 달라지는 임의의 식. 정의대로 모든 m 의 f(m) 을 곱해 더한 것과 비교."""
    rng = random.Random(2)
    for _ in range(25):
        degree = rng.randint(0, 2)
        coefficients = [rng.randint(-4, 5) for _ in range(degree + 1)]

        def poly(p):
            return sum(c * p ** k for k, c in enumerate(coefficients))

        style = rng.randrange(3)

        def prime_power(p, e):
            if style == 0:
                return poly(p) ** e
            if style == 1:
                return poly(p) * e * e
            return poly(p) if e == 1 else (p * e - 3)  # e ≥ 2 에서는 아무 식이나 (e = 1 만 다항식과 맞으면 된다)

        prefix = prefix_sums(prime_power, 3000)
        for n in rng.sample(range(1, 3000), 15) + [2999, 3000]:
            assert solution.min25_sum(n, coefficients, prime_power) == prefix[n], (coefficients, style, n)


def test_modular_results_equal_exact_results_reduced():
    rng = random.Random(3)
    for mod in (10**9 + 7, 998244353, 7):
        for n in rng.sample(range(2, 50000), 15):
            assert solution.sum_totient(n, mod) == TOTIENT[n] % mod
            assert solution.sum_sigma(n, mod) == SIGMA[n] % mod
            assert solution.sum_mobius(n, mod) == MOBIUS[n] % mod
    big = 10**7
    assert solution.sum_sigma(big, 998244353) == solution.sum_sigma(big) % 998244353


def test_prime_poly_length_is_validated():
    with pytest.raises(ValueError, match="길이"):
        solution.min25_sum(10, [], lambda p, e: 1)
    with pytest.raises(ValueError, match="길이"):
        solution.min25_sum(10, [1, 2, 3, 4], lambda p, e: 1)


def test_tables_have_square_root_many_entries():
    small, large, primes = solution._tables(10**6, 1)
    assert len(small[0]) == 1001 and len(large[0]) == 1001
    assert primes == [p for p in range(2, 1001) if all(p % q for q in range(2, isqrt(p) + 1))]
    assert large[0][1] == 78498 and small[0][1000] == 168 and large[0][1000] == solution.prime_count(1000)


def test_speed_ten_million():
    start = time.perf_counter()
    assert solution.prime_count(10**7) == 664579
    assert solution.sum_totient(10**7) == 30396356427242
    assert time.perf_counter() - start < 60


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("1000\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["168", "76127", "304192"]
