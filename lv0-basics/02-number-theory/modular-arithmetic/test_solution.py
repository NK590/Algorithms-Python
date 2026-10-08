"""solution.py 검증: 큰 정수를 그대로 계산한 뒤 나머지를 취한 값과 비교"""
import io
import math
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def test_add_sub_mul_match_direct_computation():
    rng = random.Random(0)
    for _ in range(1000):
        a, b = rng.randint(-10**12, 10**12), rng.randint(-10**12, 10**12)
        m = rng.randint(1, 10**9)
        assert solution.add_mod(a, b, m) == (a + b) % m
        assert solution.sub_mod(a, b, m) == (a - b) % m
        assert solution.mul_mod(a, b, m) == (a * b) % m


def test_results_are_in_range_even_for_negative_inputs():
    for a in range(-20, 20):
        for b in range(-20, 20):
            assert 0 <= solution.sub_mod(a, b, 7) < 7
            assert 0 <= solution.add_mod(a, b, 7) < 7


def test_factorial_mod():
    for n in range(0, 40):
        for m in (1, 2, 7, 1000, 10**9 + 7):
            assert solution.factorial_mod(n, m) == math.factorial(n) % m


def test_fibonacci_mod():
    fib = [0, 1]
    for _ in range(300):
        fib.append(fib[-1] + fib[-2])
    for n in range(0, 300, 7):
        for m in (1, 2, 10, 1000, 10**9 + 7):
            assert solution.fibonacci_mod(n, m) == fib[n] % m
    assert solution.fibonacci_mod(1, 1) == 0  # m = 1 이면 모든 나머지가 0 이다. 초깃값 F1 도 나머지를 취해야 한다
    assert solution.fibonacci_mod(0, 1) == 0
    assert solution.fibonacci_mod(1, 10) == 1


def test_power_mod_slow_matches_pow():
    rng = random.Random(1)
    for _ in range(300):
        a, b, m = rng.randint(0, 10**6), rng.randint(0, 200), rng.randint(1, 10**6)
        assert solution.power_mod_slow(a, b, m) == pow(a, b, m)


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("5 8 4\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["1", "1", "0", "0"]
