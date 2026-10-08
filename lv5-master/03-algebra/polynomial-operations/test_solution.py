"""solution.py 검증: 계수 점화식(O(n²)) 으로 구하는 순진한 구현, 이항 계수 같은 닫힌 식, 라그랑주 보간과 호너 평가와 비교"""
import io
import random
import time
from math import comb

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)
MODS = [998244353, 10**9 + 7, 10007]


def naive_multiply(a, b, mod):
    if not a or not b:
        return []
    result = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i + j] += x * y
    return [c % mod for c in result]


def naive_inverse(f, n, mod):
    inv0 = pow(f[0], mod - 2, mod)
    g = []
    for i in range(n):
        total = (1 if i == 0 else 0) - sum(f[j] * g[i - j] for j in range(1, min(i, len(f) - 1) + 1))
        g.append(total * inv0 % mod)
    return g


def naive_exp(f, n, mod):
    """n a_n = Σ k f_k a_{n-k}"""
    a = [1]
    for i in range(1, n):
        total = sum(k * (f[k] if k < len(f) else 0) % mod * a[i - k] for k in range(1, i + 1))
        a.append(total % mod * pow(i, mod - 2, mod) % mod)
    return a[:n]


def naive_log(f, n, mod):
    """g' = f'/f, 즉 n g_n = n f_n - Σ_{k=1}^{n-1} k g_k f_{n-k}  (f_0 = 1)"""
    fx = lambda i: f[i] if i < len(f) else 0
    g = [0]
    for i in range(1, n):
        total = i * fx(i) - sum(k * g[k] * fx(i - k) for k in range(1, i))
        g.append(total % mod * pow(i, mod - 2, mod) % mod)
    return g[:n]


def naive_sqrt_series(f, n, mod, root):
    """g_0 = root, g_n = (f_n - Σ_{i=1}^{n-1} g_i g_{n-i}) / (2 g_0)"""
    fx = lambda i: f[i] if i < len(f) else 0
    g = [root]
    for i in range(1, n):
        total = fx(i) - sum(g[j] * g[i - j] for j in range(1, i))
        g.append(total % mod * pow(2 * root, mod - 2, mod) % mod)
    return g[:n]


def naive_divmod(a, b, mod):
    a = [x % mod for x in a]
    b = [x % mod for x in b]
    while b and b[-1] == 0:
        b.pop()
    while a and a[-1] == 0:
        a.pop()
    quotient = [0] * max(0, len(a) - len(b) + 1)
    inv_lead = pow(b[-1], mod - 2, mod)
    while len(a) >= len(b):
        coefficient = a[-1] * inv_lead % mod
        shift = len(a) - len(b)
        quotient[shift] = coefficient
        for i, c in enumerate(b):
            a[shift + i] = (a[shift + i] - coefficient * c) % mod
        while a and a[-1] == 0:
            a.pop()
    while quotient and quotient[-1] == 0:
        quotient.pop()
    return quotient, a


def horner(f, x, mod):
    value = 0
    for c in reversed(f):
        value = (value * x + c) % mod
    return value


def random_poly(rng, length, mod, first=None):
    f = [rng.randrange(mod) for _ in range(length)]
    if first is not None and f:
        f[0] = first
    return f


def test_multiply_matches_schoolbook_across_both_code_paths():
    rng = random.Random(0)
    for mod in MODS + [3, 2]:
        for la, lb in [(1, 1), (5, 9), (24, 24), (25, 25), (25, 400), (300, 301), (1000, 7), (1000, 1000)]:
            a, b = random_poly(rng, la, mod), random_poly(rng, lb, mod)
            assert solution.multiply(a, b, mod) == naive_multiply(a, b, mod), (mod, la, lb)


def test_multiply_handles_empty_and_unreduced_input():
    assert solution.multiply([], [1, 2]) == []
    assert solution.multiply([1, 2], []) == []
    p = solution.MOD
    a, b = [p + 3, -5, 2 * p], [7, -1]
    assert solution.multiply(a, b) == naive_multiply([x % p for x in a], [x % p for x in b], p)
    big_a, big_b = [-1] * 60, [p + 1] * 50
    assert solution.multiply(big_a, big_b) == naive_multiply([p - 1] * 60, [1] * 50, p)


def test_multiply_reduces_huge_and_negative_coefficients_on_the_long_path():
    p = solution.MOD
    rng = random.Random(30)
    a = [rng.randrange(-10**30, 10**30) for _ in range(40)]
    b = [rng.randrange(-10**30, 10**30) for _ in range(35)]
    expected = naive_multiply([x % p for x in a], [y % p for y in b], p)
    assert solution.multiply(a, b) == expected
    assert solution.multiply(b, a) == expected


def test_inverse_matches_recurrence_and_is_a_true_inverse():
    rng = random.Random(1)
    for mod in MODS:
        for _ in range(30):
            n = rng.randint(1, 70)
            f = random_poly(rng, rng.randint(1, 80), mod)
            f[0] = f[0] or 1
            g = solution.poly_inverse(f, n, mod)
            assert len(g) == n and g == naive_inverse(f, n, mod)
            product = solution.multiply(f, g, mod)[:n]
            assert product == [1] + [0] * (n - 1)


def test_inverse_requires_a_unit_constant_term():
    with pytest.raises(ValueError, match="상수항"):
        solution.poly_inverse([0, 1], 4)
    with pytest.raises(ValueError, match="상수항"):
        solution.poly_inverse([], 4)
    assert solution.poly_inverse([5], 3) == [pow(5, solution.MOD - 2, solution.MOD), 0, 0]


def test_log_and_exp_match_recurrences_and_invert_each_other():
    rng = random.Random(2)
    for mod in MODS:
        for _ in range(25):
            n = rng.randint(1, 60)
            g = random_poly(rng, rng.randint(1, 70), mod, first=0)
            e = solution.poly_exp(g, n, mod)
            assert e == naive_exp(g, n, mod)
            h = random_poly(rng, rng.randint(1, 70), mod, first=1)
            lg = solution.poly_log(h, n, mod)
            assert lg == naive_log(h, n, mod)
            assert solution.poly_log(e, n, mod) == (g + [0] * n)[:n]
            assert solution.poly_exp(lg, n, mod) == (h + [0] * n)[:n]


def test_log_exp_domain_errors_and_trivial_sizes():
    with pytest.raises(ValueError, match="상수항이 1"):
        solution.poly_log([2, 1], 3)
    with pytest.raises(ValueError, match="상수항이 0"):
        solution.poly_exp([1, 1], 3)
    assert solution.poly_exp([], 4) == [1, 0, 0, 0]
    assert solution.poly_exp([0, 5], 0) == []
    assert solution.poly_log([1, 5], 0) == []
    assert solution.poly_log([1, 5], 1) == [0]


def test_pow_matches_repeated_multiplication_and_binomials():
    rng = random.Random(3)
    p = solution.MOD
    for _ in range(60):
        n = rng.randint(1, 40)
        f = random_poly(rng, rng.randint(1, 8), p)
        if rng.random() < 0.5:
            f = [0] * rng.randint(1, 3) + f  # 앞에 0 이 있는 경우
        k = rng.randint(0, 9)
        expected = [1] + [0] * (n - 1)
        for _ in range(k):
            expected = (naive_multiply(expected, f, p) + [0] * n)[:n]
        assert solution.poly_pow(f, k, n, p) == expected, (f, k, n)
    # (1 + x)^k = Σ C(k, j) x^j, k 가 매우 커도 j < p 이므로 항이 맞다
    for k in (10**9, 10**18, 2**70 + 3):
        got = solution.poly_pow([1, 1], k, 12, p)
        assert got == [comb(k, j) % p for j in range(12)]


def test_pow_zero_polynomial_and_overflowing_valuation():
    assert solution.poly_pow([0, 0], 0, 3) == [1, 0, 0]
    assert solution.poly_pow([0, 0], 5, 3) == [0, 0, 0]
    assert solution.poly_pow([], 5, 3) == [0, 0, 0]
    assert solution.poly_pow([0, 1], 3, 3) == [0, 0, 0]  # x^3 mod x^3
    assert solution.poly_pow([0, 1], 3, 5) == [0, 0, 0, 1, 0]
    assert solution.poly_pow([2, 3], 0, 0) == []
    with pytest.raises(ValueError, match="k"):
        solution.poly_pow([1, 1], -1, 3)


def test_mod_sqrt_returns_the_smaller_root_or_none():
    for mod in (7, 13, 17, 10007, 998244353):
        rng = random.Random(mod)
        for a in [rng.randrange(mod) for _ in range(60)]:
            root = solution.mod_sqrt(a, mod)
            if root is None:
                assert pow(a, (mod - 1) // 2, mod) == mod - 1
            else:
                assert root * root % mod == a % mod
                assert root <= mod - root
    assert solution.mod_sqrt(0, 7) == 0
    assert solution.mod_sqrt(3, 2) == 1


def test_sqrt_of_perfect_squares_and_recurrence():
    rng = random.Random(4)
    for mod in MODS:
        for _ in range(30):
            n = rng.randint(1, 50)
            g = random_poly(rng, rng.randint(1, 20), mod)
            g[0] = g[0] or 1
            f = naive_multiply(g, g, mod)
            root = solution.poly_sqrt(f, n, mod)
            assert root is not None and len(root) == n
            assert naive_multiply(root, root, mod)[:n] == (f + [0] * n)[:n]
            assert root[0] == min(g[0], mod - g[0])
        for _ in range(20):
            n = rng.randint(1, 40)
            f = random_poly(rng, rng.randint(1, 30), mod)
            f[0] = pow(f[0] or 1, 2, mod)  # 제곱수로
            root = solution.poly_sqrt(f, n, mod)
            assert root == naive_sqrt_series(f, n, mod, root[0])


def test_sqrt_with_leading_zeros_and_missing_roots():
    p = solution.MOD
    f = [0, 0] + naive_multiply([3, 1], [3, 1], p)  # x² (3 + x)²
    assert solution.poly_sqrt(f, 6) == [0, 3, 1, 0, 0, 0]
    assert solution.poly_sqrt([0, 1, 1], 4) is None  # x 의 차수가 홀수
    assert solution.poly_sqrt([0, 0, 0], 3) == [0, 0, 0]
    non_residue = next(a for a in range(2, 100) if pow(a, (p - 1) // 2, p) == p - 1)
    assert solution.poly_sqrt([non_residue, 1], 4) is None
    assert solution.poly_sqrt([1, 2], 0) == []
    assert solution.poly_sqrt([0] * 5 + [1], 3) == [0, 0, 0]  # 낮은 차수가 n 이상 비어 있으면 mod x^n 에서 0 의 제곱근은 0
    assert solution.poly_sqrt([0] * 6 + [4], 3) == [0, 0, 0]
    assert solution.poly_sqrt([0, 0, 0, 1], 3) == [0, 0, 0]


def test_divmod_matches_long_division():
    rng = random.Random(5)
    for mod in MODS:
        for _ in range(60):
            a = random_poly(rng, rng.randint(0, 80), mod)
            b = random_poly(rng, rng.randint(1, 40), mod)
            b[-1] = b[-1] or 1
            q, r = solution.poly_divmod(a, b, mod)
            eq, er = naive_divmod(a, b, mod) if any(a) else ([], [])
            assert (q, r) == (eq, er)
            reconstructed = naive_multiply(b, q, mod) if q else []
            total = [((reconstructed[i] if i < len(reconstructed) else 0) + (r[i] if i < len(r) else 0)) % mod
                     for i in range(max(len(reconstructed), len(r), len(a)))]
            assert total[:len(a)] == [x % mod for x in a] and not any(total[len(a):])
            assert len(r) < len(b)


def test_divmod_edge_cases():
    assert solution.poly_divmod([1, 2], [0, 0, 1]) == ([], [1, 2])
    assert solution.poly_divmod([], [1, 1]) == ([], [])
    assert solution.poly_divmod([6, 5, 1], [2, 1]) == ([3, 1], [])
    assert solution.poly_divmod([1, 2, 3], [5]) == ([pow(5, solution.MOD - 2, solution.MOD) * c % solution.MOD for c in (1, 2, 3)], [])
    with pytest.raises(ValueError, match="0 으로"):
        solution.poly_divmod([1, 2], [0, 0])
    with pytest.raises(ValueError, match="0 으로"):
        solution.poly_divmod([1, 2], [])


def test_multipoint_evaluation_matches_horner():
    rng = random.Random(6)
    for mod in MODS:
        for _ in range(25):
            f = random_poly(rng, rng.randint(0, 90), mod)
            xs = [rng.randrange(mod) for _ in range(rng.randint(0, 70))]
            assert solution.multipoint_evaluate(f, xs, mod) == [horner(f, x, mod) for x in xs]
    assert solution.multipoint_evaluate([1, 1], []) == []
    assert solution.multipoint_evaluate([], [1, 2, 3]) == [0, 0, 0]
    assert solution.multipoint_evaluate([5], [1, 2, 3, 4]) == [5, 5, 5, 5]
    xs = [3, 3, 3, 3] * 5  # 같은 점이 여러 번 나와도 평가는 된다
    assert solution.multipoint_evaluate([1, 2, 3], xs) == [horner([1, 2, 3], 3, solution.MOD)] * 20


def test_multipoint_evaluation_reduces_the_polynomial_while_descending(monkeypatch):
    """나머지를 내려 보내는 이유: 잎 근처에서는 다항식의 차수가 작아야 호너 평가가 싸다 (그렇지 않으면 O(n²))."""
    lengths = []
    original = solution._horner
    monkeypatch.setattr(solution, "_horner", lambda f, x, mod: (lengths.append(len(f)), original(f, x, mod))[1])
    rng = random.Random(31)
    p = solution.MOD
    f = random_poly(rng, 300, p)
    xs = rng.sample(range(p), 200)
    assert solution.multipoint_evaluate(f, xs) == [horner(f, x, p) for x in xs]
    assert lengths and max(lengths) <= 16


def test_interpolation_passes_through_points_and_matches_lagrange():
    rng = random.Random(7)
    for mod in MODS:
        for _ in range(25):
            n = rng.randint(0, 60)
            xs = rng.sample(range(mod), n)
            ys = [rng.randrange(mod) for _ in range(n)]
            f = solution.interpolate(xs, ys, mod)
            assert len(f) <= n and (not f or f[-1] != 0)
            assert [horner(f, x, mod) for x in xs] == ys
            if n <= 12:  # 라그랑주 공식으로 직접
                expected = [0] * n
                for i in range(n):
                    term = [1]
                    denominator = 1
                    for j in range(n):
                        if j != i:
                            term = naive_multiply(term, [(-xs[j]) % mod, 1], mod)
                            denominator = denominator * (xs[i] - xs[j]) % mod
                    scale = ys[i] * pow(denominator, mod - 2, mod) % mod
                    expected = [(e + scale * (term[k] if k < len(term) else 0)) % mod for k, e in enumerate(expected)]
                while expected and expected[-1] == 0:
                    expected.pop()
                assert f == expected


def test_interpolation_recovers_a_polynomial_and_rejects_bad_input():
    p = solution.MOD
    f = [4, 0, 7, 1]
    xs = [10, 20, 30, 40, 50]
    ys = [horner(f, x, p) for x in xs]
    assert solution.interpolate(xs, ys) == f
    with pytest.raises(ValueError, match="서로 달라야"):
        solution.interpolate([1, 2, 1], [0, 0, 0])
    with pytest.raises(ValueError, match="길이"):
        solution.interpolate([1, 2], [3])
    assert solution.interpolate([], []) == []
    assert solution.interpolate([5], [0]) == []


def test_taylor_shift_matches_binomial_expansion():
    rng = random.Random(8)
    for mod in MODS:
        for _ in range(30):
            f = random_poly(rng, rng.randint(1, 70), mod)
            c = rng.randrange(mod)
            expected = [sum(f[i] * comb(i, j) * pow(c, i - j, mod) for i in range(j, len(f))) % mod for j in range(len(f))]
            assert solution.taylor_shift(f, c, mod) == expected
    assert solution.taylor_shift([], 3) == []
    assert solution.taylor_shift([1, 2, 3], 0) == [1, 2, 3]
    assert solution.taylor_shift([1, 2, 3], 2) == [17, 14, 3]


def test_bell_numbers_match_the_bell_triangle():
    row, bell = [1], [1]
    for _ in range(40):
        new = [row[-1]]
        for x in row:
            new.append(new[-1] + x)
        row = new
        bell.append(row[0])
    n = len(bell)
    assert solution.bell_numbers(n, solution.MOD) == [b % solution.MOD for b in bell[:n]]
    assert solution.bell_numbers(0) == [] and solution.bell_numbers(1) == [1]
    assert solution.bell_numbers(10) == [1, 1, 2, 5, 15, 52, 203, 877, 4140, 21147]


def test_partition_numbers_match_dynamic_programming():
    n = 80
    p = [1] + [0] * (n - 1)
    for k in range(1, n):
        for i in range(k, n):
            p[i] += p[i - k]
    assert solution.partition_numbers(n) == [x % solution.MOD for x in p]
    assert solution.partition_numbers(0) == [] and solution.partition_numbers(1) == [1]
    assert solution.partition_numbers(8) == [1, 1, 2, 3, 5, 7, 11, 15]


def test_catalan_numbers_match_the_binomial_formula():
    n = 60
    expected = [comb(2 * k, k) // (k + 1) % solution.MOD for k in range(n)]
    assert solution.catalan_numbers(n) == expected
    assert solution.catalan_numbers(0) == [] and solution.catalan_numbers(1) == [1]
    assert solution.catalan_numbers(5, 10007) == [comb(2 * k, k) // (k + 1) % 10007 for k in range(5)]


def test_newton_iterations_cost_about_one_multiplication():
    rng = random.Random(9)
    p = solution.MOD
    n = 1 << 13
    f = random_poly(rng, n, p, first=1)
    start = time.perf_counter()
    g = solution.poly_inverse(f, n)
    elapsed_inverse = time.perf_counter() - start
    assert solution.multiply(f, g)[:n] == [1] + [0] * (n - 1)
    f[0] = 0
    start = time.perf_counter()
    e = solution.poly_exp(f, n)
    elapsed_exp = time.perf_counter() - start
    f[0] = 1
    assert solution.poly_log(e, n) == [0] + f[1:n]
    assert elapsed_inverse < 30 and elapsed_exp < 60


def test_main_reads_every_coefficient(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("3\n0 0 1\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["1", "0", "1"]  # exp(x²) = 1 + x² + …


def test_main_prints_exp_of_series(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("5\n0 1 0 0 0\n"))
    solution.main()
    inv = [pow(k, solution.MOD - 2, solution.MOD) for k in (1, 1, 2, 6, 24)]
    assert capsys.readouterr().out.split() == [str(x) for x in inv]
