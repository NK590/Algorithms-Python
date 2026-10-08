"""solution.py 검증: 소수 전체에서 정리가 성립하는지, 역원이 정의대로인지, 유사 소수·카마이클 수가 정의와 일치하는지"""
import io
import math
import random

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))


def test_power_mod_matches_builtin():
    rng = random.Random(0)
    for _ in range(1000):
        a, b, m = rng.randint(0, 10**9), rng.randint(0, 10**9), rng.randint(1, 10**9)
        assert solution.power_mod(a, b, m) == pow(a, b, m)
    assert solution.power_mod(7, 5, 1) == 0


def test_theorem_holds_for_every_prime_and_every_a_not_divisible_by_p():
    for p in range(2, 200):
        if is_prime(p):
            assert all(solution.fermat_holds(a, p) for a in range(1, p))
            assert solution.power_mod(5, p, p) == 5 % p  # a^p ≡ a 도 모든 a 에서 성립한다
            assert all(solution.power_mod(a, p, p) == a % p for a in range(0, 3 * p))


def test_the_converse_is_false():
    # 합성수 n 도 어떤 a 에서는 a^(n-1) ≡ 1 일 수 있다
    assert solution.fermat_holds(2, 341) and not is_prime(341)
    assert not solution.fermat_holds(2, 15)  # 하지만 대부분의 합성수는 걸린다


def test_inverse_mod_prime_is_a_real_inverse():
    for p in (2, 3, 5, 7, 11, 13, 101):
        for a in list(range(1, 50)) + [p - 1, 2 * p - 1]:
            if a % p:
                inv = solution.inverse_mod_prime(a, p)
                assert 0 < inv < p and a * inv % p == 1, (a, p)
    big = 10**9 + 7
    for a in (1, 2, 3, 12345, big - 1):
        inv = solution.inverse_mod_prime(a, big)
        assert 0 < inv < big and a * inv % big == 1
    with pytest.raises(ValueError):
        solution.inverse_mod_prime(14, 7)


def test_fermat_test_accepts_all_primes_and_rejects_most_composites():
    for n in range(2, 2000):
        if is_prime(n):
            assert solution.fermat_test(n), n
    assert not solution.fermat_test(0) and not solution.fermat_test(1)
    rejected = sum(1 for n in range(4, 2000) if not is_prime(n) and not solution.fermat_test(n))
    composites = sum(1 for n in range(4, 2000) if not is_prime(n))
    assert rejected / composites > 0.98


def test_pseudoprimes_base_2():
    assert solution.fermat_pseudoprimes(2000) == [341, 561, 645, 1105, 1387, 1729, 1905]
    for n in solution.fermat_pseudoprimes(5000, base=3):
        assert not is_prime(n) and pow(3, n - 1, n) == 1


def carmichael_by_definition(limit):
    result = []
    for n in range(3, limit + 1):
        if is_prime(n):
            continue
        if all(pow(a, n - 1, n) == 1 for a in range(1, n) if math.gcd(a, n) == 1):
            result.append(n)
    return result


def test_carmichael_numbers_match_the_definition():
    assert solution.carmichael_numbers(3000) == carmichael_by_definition(3000) == [561, 1105, 1729, 2465, 2821]
    assert solution.carmichael_numbers(10000) == [561, 1105, 1729, 2465, 2821, 6601, 8911]


def test_carmichael_numbers_fool_every_coprime_base():
    # 561 = 3 · 11 · 17 은 소수가 아니지만, 561 과 서로소인 밑(2, 5, 7, 13)의 검사를 모두 통과해 소수처럼 보인다
    assert not is_prime(561)
    assert solution.fermat_test(561, bases=(2, 5, 7, 13))
    assert all(solution.fermat_holds(a, 561) for a in range(1, 561) if math.gcd(a, 561) == 1)
    # 서로소가 아닌 밑(3 은 561 의 약수)은 합성수임을 드러낸다
    assert not solution.fermat_test(561, bases=(3,))
    assert not solution.fermat_test(561)  # 기본 밑 (2, 3, 5, 7) 에는 3 이 들어 있다


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("3 7\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "5"  # 3 · 5 = 15 ≡ 1 (mod 7)
