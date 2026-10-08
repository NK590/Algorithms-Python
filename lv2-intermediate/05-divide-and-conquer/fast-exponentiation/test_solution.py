"""solution.py 검증: 파이썬 내장 pow / 단순 곱셈 반복과 비교, 곱셈 횟수가 정말 O(log b) 인지 확인"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def test_power_matches_builtin():
    for a in range(-5, 8):
        for b in range(0, 25):
            assert solution.power(a, b) == a**b, (a, b)
    assert solution.power(2, 100) == 2**100 and solution.power(0, 0) == 1


def test_power_mod_matches_builtin_pow():
    rng = random.Random(0)
    for _ in range(2000):
        a, b, m = rng.randint(0, 10**9), rng.randint(0, 10**9), rng.randint(1, 10**9)
        expected = pow(a, b, m)
        assert solution.power_mod(a, b, m) == expected, (a, b, m)
        assert solution.power_mod_recursive(a, b, m) == expected
    assert solution.power_mod(2, 10, 1000) == 24 and solution.power_mod(5, 0, 7) == 1
    assert solution.power_mod(7, 5, 1) == 0 and solution.power_mod(0, 0, 1) == 0  # 어떤 수든 1 로 나눈 나머지는 0
    assert solution.power_mod(10, 11, 12) == 4


def test_huge_exponent_is_fast():
    # 지수가 10^18 이어도 곱셈은 60 번 정도
    b = 10**18
    assert solution.power_mod(3, b, 10**9 + 7) == pow(3, b, 10**9 + 7)
    assert solution.power_mod_recursive(3, b, 10**9 + 7) == pow(3, b, 10**9 + 7)


class Counted(int):
    """곱셈 횟수를 세는 정수 (Python 의 int 를 상속해 * 만 센다)"""
    count = 0

    def __mul__(self, other):
        Counted.count += 1
        return Counted(int(self) * int(other))


def test_number_of_multiplications_is_logarithmic():
    for b in [1, 2, 3, 7, 8, 100, 1023, 1024, 10**6]:
        Counted.count = 0
        solution.power(Counted(3), b)  # 재귀 버전이 하는 곱셈을 센다 (half·half 와 ·a)
        assert Counted.count <= 2 * b.bit_length(), (b, Counted.count)
    for b in [1, 2, 3, 100, 1023, 1024, 10**6, 10**18]:
        assert solution.count_multiplications(b) <= 2 * b.bit_length()
    assert solution.count_multiplications(0) == 0
    assert solution.count_multiplications(1) == 2 and solution.count_multiplications(10) == 4 + 2


def test_power_float_with_negative_exponent():
    for x in (0.5, 2.0, 3.0, -2.0, 1.5):
        for n in range(-8, 9):
            assert abs(solution.power_float(x, n) - x**n) <= 1e-9 * max(1, abs(x**n)), (x, n)
    assert solution.power_float(2.0, 0) == 1.0


def fib_by_loop(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a, b


def test_fibonacci_doubling_matches_loop():
    for n in range(0, 200):
        assert solution.fibonacci_doubling(n) == fib_by_loop(n), n
    assert solution.fibonacci_doubling(1000)[0] == fib_by_loop(1000)[0]
    # n 이 매우 커도 재귀 깊이는 log n
    assert solution.fibonacci_doubling(10**5)[0] == fib_by_loop(10**5)[0]


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("10 11 12\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "4"
