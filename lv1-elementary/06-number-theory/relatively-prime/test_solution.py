"""solution.py 검증: "1 보다 큰 공약수가 없다"는 정의와 fractions.Fraction 과 비교"""
import io
import itertools
import math
import random
from fractions import Fraction

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def share_a_divisor(a, b):
    return any(a % d == 0 and b % d == 0 for d in range(2, max(a, b) + 1))


def test_is_coprime_matches_definition():
    for a in range(1, 40):
        for b in range(1, 40):
            assert solution.is_coprime(a, b) == (not share_a_divisor(a, b)), (a, b)
    assert solution.is_coprime(1, 99) and solution.is_coprime(8, 15) and not solution.is_coprime(6, 9)


def test_coprime_iff_lcm_is_the_product():
    for a in range(1, 30):
        for b in range(1, 30):
            assert solution.is_coprime(a, b) == (math.lcm(a, b) == a * b)


def test_coprimes_up_to():
    assert solution.coprimes_up_to(12, 12) == [1, 5, 7, 11]
    assert solution.coprimes_up_to(10, 1) == list(range(1, 11))


def test_reduce_fraction_matches_fractions_module():
    rng = random.Random(0)
    for _ in range(500):
        n, d = rng.randint(-50, 50), rng.randint(-50, 50)
        if d == 0:
            continue
        expected = Fraction(n, d)
        assert solution.reduce_fraction(n, d) == (expected.numerator, expected.denominator)
    with pytest.raises(ZeroDivisionError):
        solution.reduce_fraction(1, 0)


def test_add_fractions_matches_fractions_module():
    rng = random.Random(1)
    for _ in range(500):
        a = (rng.randint(-20, 20), rng.randint(1, 20))
        b = (rng.randint(-20, 20), rng.randint(1, 20))
        total = Fraction(*a) + Fraction(*b)
        assert solution.add_fractions(a, b) == (total.numerator, total.denominator)
    assert solution.add_fractions((2, 7), (3, 5)) == (31, 35)
    assert solution.add_fractions((1, 6), (1, 3)) == (1, 2)


def test_pairwise_coprime_is_stronger_than_overall_gcd_one():
    assert math.gcd(6, 10, 15) == 1
    assert not solution.pairwise_coprime([6, 10, 15])
    assert solution.pairwise_coprime([2, 3, 5, 7]) and solution.pairwise_coprime([8]) and solution.pairwise_coprime([])


def test_pairwise_coprime_checks_every_pair():
    assert not solution.pairwise_coprime([2, 4, 3])  # 맨 앞 두 수(인접한 쌍)만 서로소가 아닌 경우
    assert not solution.pairwise_coprime([3, 5, 7, 14])  # 맨 처음과 맨 끝만 걸리는 경우
    rng = random.Random(2)
    for _ in range(300):
        numbers = [rng.randint(1, 30) for _ in range(rng.randint(0, 5))]
        expected = all(math.gcd(x, y) == 1 for x, y in itertools.combinations(numbers, 2))
        assert solution.pairwise_coprime(numbers) == expected, numbers


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("2 7\n3 5\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["31", "35"]
