"""solution.py 검증: 정의대로 완전탐색한 값과 비교하고, 반환한 계수를 식에 대입해 확인한다"""
import io
import math
import random

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def test_bezout_identity_holds_for_every_small_pair_including_negatives():
    for a in range(-30, 31):
        for b in range(-30, 31):
            g, x, y = solution.extended_gcd(a, b)
            assert g == math.gcd(a, b), (a, b)
            assert a * x + b * y == g, (a, b, x, y)


def test_bezout_identity_for_huge_numbers():
    rng = random.Random(0)
    for _ in range(300):
        a, b = rng.randint(1, 10**18), rng.randint(1, 10**18)
        g, x, y = solution.extended_gcd(a, b)
        assert g == math.gcd(a, b) and a * x + b * y == g
    a, b = 354224848179261931, 218922995834555169  # 인접한 피보나치 수: 단계가 가장 많은 경우
    g, x, y = solution.extended_gcd(a, b)
    assert g == 1 and a * x + b * y == 1


def test_coefficients_stay_small():
    rng = random.Random(1)
    for _ in range(500):
        a, b = rng.randint(1, 10**6), rng.randint(1, 10**6)
        g, x, y = solution.extended_gcd(a, b)
        assert abs(x) <= b // g and abs(y) <= a // g, (a, b, x, y)


def test_recursive_version_agrees():
    for a in range(0, 40):
        for b in range(0, 40):
            g, x, y = solution.extended_gcd_recursive(a, b)
            assert g == math.gcd(a, b) and a * x + b * y == g, (a, b)
    assert solution.extended_gcd(240, 46) == (2, -9, 47)  # 240·(-9) + 46·47 = 2
    assert solution.extended_gcd_recursive(240, 46) == (2, -9, 47)


def test_mod_inverse_matches_brute_force():
    for m in range(1, 40):
        for a in range(-50, 50):
            expected = next((x for x in range(m) if a * x % m == 1 % m), None)
            if expected is None:
                with pytest.raises(ValueError):
                    solution.mod_inverse(a, m)
            else:
                assert solution.mod_inverse(a, m) == expected, (a, m)
    assert solution.mod_inverse(3, 10**9 + 7) == 333333336
    assert solution.mod_inverse(3, 10) == 7  # 소수가 아닌 모듈러


def brute_solutions(a, b, c, bound=60):
    return [(x, y) for x in range(-bound, bound + 1) for y in range(-bound, bound + 1) if a * x + b * y == c]


def test_diophantine_existence_and_validity():
    rng = random.Random(2)
    for _ in range(600):
        a, b = rng.randint(-12, 12), rng.randint(-12, 12)
        c = rng.randint(-30, 30)
        found = solution.solve_diophantine(a, b, c)
        exists = bool(brute_solutions(a, b, c, bound=45))
        if found is None:
            assert not exists, (a, b, c)
        else:
            assert a * found[0] + b * found[1] == c, (a, b, c, found)
            assert exists or (a == 0 and b == 0)


def test_diophantine_family_covers_exactly_the_brute_force_solutions():
    rng = random.Random(3)
    for _ in range(300):
        a, b = rng.randint(-12, 12), rng.randint(-12, 12)
        if a == 0 and b == 0:
            continue
        c = rng.randint(-30, 30)
        family = solution.diophantine_family(a, b, c)
        if family is None:
            assert not brute_solutions(a, b, c)
            continue
        x0, y0, dx, dy = family
        for t in range(-4, 5):
            assert a * (x0 + dx * t) + b * (y0 + dy * t) == c
        for x, y in brute_solutions(a, b, c):
            # b = 0 이면 dx = 0 이라 x 는 고정이고 t 는 y 로 정해진다
            t, remainder = divmod(x - x0, dx) if dx else divmod(y - y0, dy)
            assert remainder == 0 and x == x0 + dx * t and y == y0 + dy * t, (a, b, c, x, y)
    with pytest.raises(ValueError):
        solution.diophantine_family(0, 0, 0)


def test_smallest_nonnegative_x_solution_matches_brute_force():
    rng = random.Random(4)
    for _ in range(500):
        a, b = rng.randint(-12, 12), rng.randint(-12, 12)
        if b == 0:
            continue
        c = rng.randint(-40, 40)
        result = solution.smallest_nonnegative_x_solution(a, b, c)
        expected = next(((x, (c - a * x) // b) for x in range(0, abs(b) + 1) if (c - a * x) % b == 0), None)
        assert result == expected, (a, b, c)
        if result is not None:
            assert a * result[0] + b * result[1] == c and result[0] >= 0


def test_count_nonnegative_solutions_matches_brute_force():
    for a in range(1, 13):
        for b in range(1, 13):
            for c in range(0, 70):
                expected = sum(1 for x in range(0, c // a + 1) if (c - a * x) % b == 0)
                assert solution.count_nonnegative_solutions(a, b, c) == expected, (a, b, c)
    assert solution.count_nonnegative_solutions(3, 5, 7) == 0  # 동전 3, 5 로 만들 수 없는 가장 큰 금액은 7
    assert solution.count_nonnegative_solutions(3, 5, 8) == 1


def test_linear_congruence_matches_brute_force():
    for m in range(1, 25):
        for a in range(0, 25):
            for b in range(0, 25):
                brute = [x for x in range(m) if (a * x - b) % m == 0]
                result = solution.solve_linear_congruence(a, b, m)
                if result is None:
                    assert not brute, (a, b, m)
                else:
                    x0, modulus = result
                    assert 0 <= x0 < modulus, (a, b, m)
                    assert sorted(x for x in range(m) if x % modulus == x0 % modulus) == brute, (a, b, m)


def test_main(monkeypatch, capsys):
    for text, expected in [("3 5 7\n", "4 -1"), ("4 6 7\n", "-1"), ("5 0 10\n", "2 0"), ("0 0 0\n", "0 0"), ("0 0 3\n", "-1")]:
        monkeypatch.setattr("sys.stdin", io.StringIO(text))
        solution.main()
        assert capsys.readouterr().out.strip() == expected, text
