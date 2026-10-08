"""solution.py 검증: 곱하면 원래 수, 각 인수는 소수, 약수 개수·합은 직접 센 값과 비교"""
import io
import math

from tools.loader import load_solution

solution = load_solution(__file__)


def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def test_readme_example():
    assert solution.factorize(360) == [2, 2, 2, 3, 3, 5]
    assert solution.prime_exponents(360) == {2: 3, 3: 2, 5: 1}
    assert solution.factorize(1) == []
    assert solution.factorize(97) == [97]
    assert solution.factorize(2 * 3 * 5 * 7 * 11 * 13) == [2, 3, 5, 7, 11, 13]


def test_factors_multiply_back_and_are_prime_and_sorted():
    for n in range(1, 3000):
        factors = solution.factorize(n)
        assert math.prod(factors) == n
        assert all(is_prime(p) for p in factors)
        assert factors == sorted(factors)


def test_large_semiprime_and_prime():
    p, q = 1_000_003, 999_983
    assert solution.factorize(p * q) == sorted([p, q])
    assert solution.factorize(1_000_000_007) == [1_000_000_007]
    assert solution.factorize(2**40) == [2] * 40


def test_count_and_sum_of_divisors_match_direct_enumeration():
    for n in range(1, 1500):
        assert solution.count_divisors(n) == len(divisors(n)), n
        assert solution.sum_of_divisors(n) == sum(divisors(n)), n


def test_factorize_with_spf_matches_trial_division():
    limit = 3000
    spf = list(range(limit + 1))
    for i in range(2, limit + 1):
        if spf[i] == i:
            for j in range(i * i, limit + 1, i):
                if spf[j] == j:
                    spf[j] = i
    for n in range(1, limit + 1):
        assert solution.factorize_with_spf(n, spf) == solution.factorize(n)


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("72\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["2", "2", "2", "3", "3"]
