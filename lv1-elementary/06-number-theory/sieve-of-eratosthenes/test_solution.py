"""solution.py 검증: 하나씩 나눠 보는 판별과 비교 + 알려진 소수의 개수"""
import io
from math import isqrt

from tools.loader import load_solution

solution = load_solution(__file__)


def is_prime_by_trial(n):
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


def test_readme_example():
    assert solution.sieve(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


def test_matches_trial_division():
    table = solution.prime_table(3000)
    assert table == [is_prime_by_trial(i) for i in range(3001)]


def test_every_limit_including_prime_squares():
    # n 이 소수의 제곱(4, 9, 25, 49 …)일 때도 √n 까지 지워야 한다
    for n in range(0, 400):
        assert solution.prime_table(n) == [is_prime_by_trial(i) for i in range(n + 1)], n
        spf = solution.smallest_prime_factor_table(n)
        for i in range(2, n + 1):
            assert spf[i] == next(d for d in range(2, i + 1) if i % d == 0), (n, i)


def test_small_limits():
    assert solution.sieve(0) == [] and solution.sieve(1) == []
    assert solution.sieve(2) == [2] and solution.sieve(3) == [2, 3]
    assert solution.prime_table(0) == [False] and solution.prime_table(1) == [False, False]


def test_known_prime_counts():
    assert solution.count_primes(100) == 25
    assert solution.count_primes(1000) == 168
    assert solution.count_primes(10**6) == 78498


def test_smallest_prime_factor_table():
    spf = solution.smallest_prime_factor_table(3000)
    for i in range(2, 3001):
        expected = next(d for d in range(2, i + 1) if i % d == 0)
        assert spf[i] == expected, i
    # spf 로 소인수분해: 360 = 2^3 × 3^2 × 5
    n, factors = 360, []
    while n > 1:
        factors.append(spf[n])
        n //= spf[n]
    assert factors == [2, 2, 2, 3, 3, 5]


def test_large_limit_runs_fast():
    assert solution.count_primes(2 * 10**6) == 148933


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("10 30\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["11", "13", "17", "19", "23", "29"]


def test_main_range_is_inclusive_on_both_ends(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("11 29\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["11", "13", "17", "19", "23", "29"]
