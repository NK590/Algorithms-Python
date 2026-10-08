"""solution.py 검증: math.comb 로 구한 정확한 값을 나머지로 비교"""
import io
import math
import random

from tools.loader import load_solution

solution = load_solution(__file__)
P = solution.MOD


def test_factorial_tables():
    fact, inv_fact = solution.build_factorials(1000, P)
    assert fact[0] == 1 and fact[5] == 120 and fact[1000] == math.factorial(1000) % P
    for i in range(0, 1001, 37):
        assert fact[i] * inv_fact[i] % P == 1
    assert solution.build_factorials(0, 7) == ([1], [1])


def test_binomial_mod_matches_exact_values():
    fact, inv_fact = solution.build_factorials(2000, P)
    for n in range(0, 30):
        for r in range(-1, n + 3):
            expected = math.comb(n, r) % P if 0 <= r <= n else 0
            assert solution.binomial_mod(n, r, P, fact, inv_fact) == expected, (n, r)
    rng = random.Random(0)
    for _ in range(500):
        n = rng.randint(0, 2000)
        r = rng.randint(0, n)
        assert solution.binomial_mod(n, r, P, fact, inv_fact) == math.comb(n, r) % P


def test_binomial_once_matches_exact_values_including_huge_n():
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(0, 3000)
        r = rng.randint(-2, n + 2)
        assert solution.binomial_once(n, r, P) == (math.comb(n, r) % P if 0 <= r <= n else 0)
    # n 이 매우 커도 r 이 작으면 된다
    assert solution.binomial_once(4_000_000, 3, P) == math.comb(4_000_000, 3) % P
    # 대칭: r 이 n 에 가까우면 n - r 번만 곱한다 (10^9 번 곱하면 끝나지 않는다)
    assert solution.binomial_once(10**9, 10**9 - 3, P) == math.comb(10**9, 3) % P


def test_pascal_works_for_composite_moduli():
    rng = random.Random(2)
    for _ in range(300):
        n = rng.randint(0, 40)
        r = rng.randint(-1, n + 1)
        mod = rng.choice([2, 4, 6, 9, 10, 12, 100, 1000, P])
        expected = math.comb(n, r) % mod if 0 <= r <= n else 0
        assert solution.binomial_pascal(n, r, mod) == expected, (n, r, mod)
    # 소수가 아닌 모듈러에서는 역원 방식으로는 틀린다 (4! 의 역원이 mod 10 에 없다)
    assert solution.binomial_pascal(10, 4, 10) == 0 and math.comb(10, 4) == 210


def test_catalan_numbers():
    fact, inv_fact = solution.build_factorials(100, P)
    known = [1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796]
    assert [solution.catalan_mod(n, P, fact, inv_fact) for n in range(11)] == known
    for n in range(0, 40):
        assert solution.catalan_mod(n, P, fact, inv_fact) == math.comb(2 * n, n) // (n + 1) % P


def test_grid_paths_and_multisets():
    fact, inv_fact = solution.build_factorials(100, P)
    assert solution.grid_paths_mod(3, 3, P, fact, inv_fact) == 6
    assert solution.grid_paths_mod(1, 5, P, fact, inv_fact) == 1
    assert solution.grid_paths_mod(18, 18, P, fact, inv_fact) == math.comb(34, 17) % P
    # 3 종류에서 중복을 허용해 2 개: AA AB AC BB BC CC
    assert solution.multiset_count(3, 2, P, fact, inv_fact) == 6


def test_large_table_is_fast():
    fact, inv_fact = solution.build_factorials(10**6, P)
    assert solution.binomial_mod(10**6, 500_000, P, fact, inv_fact) == solution.binomial_once(10**6, 500_000, P)


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("5 2\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "10"
    monkeypatch.setattr("sys.stdin", io.StringIO("1000 500\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == str(math.comb(1000, 500) % P)
