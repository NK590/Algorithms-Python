"""solution.py 검증: 체, 시행 나눗셈, 알려진 소수·카마이클 수·강한 의사소수와 비교"""
import io
import math
import random

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def sieve(limit):
    flags = bytearray([1]) * (limit + 1)
    flags[0:2] = b"\x00\x00"
    for i in range(2, int(limit**0.5) + 1):
        if flags[i]:
            flags[i * i :: i] = bytearray(len(flags[i * i :: i]))
    return flags


def trial_division_is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    for p in range(3, math.isqrt(n) + 1, 2):
        if n % p == 0:
            return False
    return True


def test_matches_a_sieve_for_every_number_up_to_200000():
    flags = sieve(200000)
    for n in range(200001):
        assert solution.is_prime(n) == bool(flags[n]), n
    assert not solution.is_prime(-7) and not solution.is_prime(0) and not solution.is_prime(1)


def test_matches_trial_division_for_random_numbers_around_10_to_the_12():
    rng = random.Random(0)
    for _ in range(80):
        n = rng.randint(10**12, 2 * 10**12)
        assert solution.is_prime(n) == trial_division_is_prime(n), n


def test_mersenne_numbers_and_their_neighbours():
    mersenne_exponents = {2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521}
    for p in range(2, 140):
        assert solution.is_prime(2**p - 1, rng=random.Random(1)) == (p in mersenne_exponents), p
    assert solution.is_prime(2**521 - 1, rng=random.Random(2))
    assert not solution.is_prime(2**521 + 1, rng=random.Random(2))  # 3 으로 나누어떨어진다


def test_carmichael_numbers_fool_fermat_but_not_miller_rabin():
    carmichael = [561, 1105, 1729, 2465, 2821, 6601, 8911, 41041, 825265, 321197185]
    for n in carmichael:
        coprime_bases = [a for a in range(2, min(n - 1, 60)) if math.gcd(a, n) == 1]
        assert all(solution.is_fermat_probable_prime(n, a) for a in coprime_bases), n  # 서로소인 모든 밑에서 속는다
        assert not solution.is_prime(n), n
        assert any(not solution.is_strong_probable_prime(n, a) for a in coprime_bases), n


def test_strong_pseudoprimes_to_small_bases_are_caught_by_the_full_base_set():
    table = {
        2047: [2],
        1373653: [2, 3],
        25326001: [2, 3, 5],
        3215031751: [2, 3, 5, 7],
        2152302898747: [2, 3, 5, 7, 11],
        3474749660383: [2, 3, 5, 7, 11, 13],
        341550071728321: [2, 3, 5, 7, 11, 13, 17],
        3825123056546413051: [2, 3, 5, 7, 11, 13, 17, 19, 23],
        318665857834031151167461: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37],
    }
    for n, bases in table.items():
        assert all(solution.is_strong_probable_prime(n, a) for a in bases), n  # 이 밑들에는 소수처럼 보인다
        assert not solution.is_prime(n), n  # 그러나 13 개의 밑 전체로는 걸러진다


def test_strong_probable_prime_is_true_for_every_base_when_n_is_prime():
    for n in (5, 7, 13, 101, 7919, 104729):
        assert all(solution.is_strong_probable_prime(n, a) for a in range(2, n - 1)), n


def test_at_most_a_quarter_of_bases_are_liars_for_an_odd_composite():
    for n in range(9, 3000, 2):
        if solution.is_prime(n):
            continue
        liars = sum(1 for a in range(1, n) if solution.is_strong_probable_prime(n, a))
        assert liars <= (n - 1) / 4, (n, liars)


def test_primes_squares_and_products_of_big_primes():
    p, q = 2**61 - 1, 2**89 - 1
    assert solution.is_prime(p) and solution.is_prime(q)
    assert not solution.is_prime(p * q) and not solution.is_prime(p * p) and not solution.is_prime(q * q)
    for prime in (41, 43, 47):
        assert not solution.is_prime(prime * prime)
    assert solution.is_prime(2**127 - 1, rng=random.Random(3))  # 결정적 한계(3.3·10^24) 를 넘는 크기: 무작위 밑
    assert not solution.is_prime((2**127 - 1) * (2**107 - 1), rng=random.Random(3))
    assert not solution.is_prime(2**128, rng=random.Random(3))


def test_the_number_of_random_bases_follows_rounds_above_the_deterministic_limit():
    class CountingRng:
        def __init__(self):
            self.calls = 0

        def randrange(self, low, high):
            self.calls += 1
            return random.Random(self.calls).randrange(low, high)

    for rounds in (1, 7, 40):
        rng = CountingRng()
        assert solution.is_prime(2**127 - 1, rounds=rounds, rng=rng)  # 소수는 모든 밑을 통과하므로 rounds 번 모두 뽑는다
        assert rng.calls == rounds
    rng = CountingRng()
    assert solution.is_prime(1000003, rng=rng) and rng.calls == 0  # 결정적 범위에서는 난수를 쓰지 않는다


def test_small_primes_are_recognised_and_their_multiples_are_not():
    for p in solution.SMALL_PRIMES:
        assert solution.is_prime(p)
        assert not solution.is_prime(p * 101) and not solution.is_prime(p * p)


def test_next_prime():
    flags = sieve(5000)
    for n in range(-3, 4000):
        expected = next(m for m in range(max(n + 1, 2), 5000) if flags[m])
        assert solution.next_prime(n) == expected, n
    assert solution.next_prime(10**18) == 10**18 + 3
    assert solution.next_prime(2**61 - 2) == 2**61 - 1


def test_known_values_of_the_decomposition_helper():
    assert solution._decompose(13) == (2, 3)  # 12 = 2² · 3
    assert solution._decompose(17) == (4, 1)  # 16 = 2⁴ · 1
    assert solution._decompose(3) == (1, 1)


def test_main_counts_areas_with_prime_two_s_plus_one(monkeypatch, capsys):
    # 2S+1: 3 (소수), 5 (소수), 7 (소수), 9 (합성수), 11 (소수), 13 (소수), 15 (합성수)
    monkeypatch.setattr("sys.stdin", io.StringIO("7\n1 2 3 4 5 6 7\n"))
    solution.main()
    assert capsys.readouterr().out == "5\n"
    # N 이 S 의 하나와 같지 않은 입력: 2S+1 = 21 (합성수), 23 (소수), 27 (합성수) -> 1 개
    monkeypatch.setattr("sys.stdin", io.StringIO("3\n10 11 13\n"))
    solution.main()
    assert capsys.readouterr().out == "1\n"
