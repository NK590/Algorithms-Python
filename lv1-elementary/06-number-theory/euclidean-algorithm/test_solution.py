"""solution.py 검증: 정의(공통 약수 중 최대)와 math.gcd 와 비교 + 피보나치가 최악의 입력"""
import io
import math
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def gcd_by_definition(a, b):
    return max(d for d in range(1, max(a, b, 1) + 1) if a % d == 0 and b % d == 0)


def test_readme_example():
    assert solution.gcd(48, 18) == 6
    assert solution.lcm(48, 18) == 144


def test_matches_definition_for_small_numbers():
    for a in range(1, 40):
        for b in range(1, 40):
            assert solution.gcd(a, b) == gcd_by_definition(a, b) == solution.gcd_recursive(a, b), (a, b)


def test_matches_math_gcd_on_large_and_edge_inputs():
    rng = random.Random(0)
    for _ in range(500):
        a, b = rng.randint(0, 10**18), rng.randint(0, 10**18)
        assert solution.gcd(a, b) == solution.gcd_recursive(a, b) == math.gcd(a, b)
        assert solution.lcm(a, b) == math.lcm(a, b)
    assert solution.gcd(0, 7) == 7 and solution.gcd(7, 0) == 7 and solution.gcd(0, 0) == 0
    assert solution.gcd(-12, 18) == 6  # 부호는 무시한다
    assert solution.gcd(12, -18) == 6 and solution.gcd(-12, -18) == 6 and solution.gcd_recursive(12, -18) == 6
    assert solution.lcm(0, 5) == 0 and solution.lcm(5, 0) == 0 and solution.lcm(0, 0) == 0
    assert solution.lcm(-4, 6) == 12


def test_lcm_gcd_product_identity():
    for a in range(1, 30):
        for b in range(1, 30):
            assert solution.gcd(a, b) * solution.lcm(a, b) == a * b


def test_gcd_of_list():
    assert solution.gcd_of_list([12, 18, 30]) == 6
    assert solution.gcd_of_list([7]) == 7
    assert solution.gcd_of_list([]) == 0
    rng = random.Random(1)
    for _ in range(200):
        numbers = [rng.randint(1, 100) for _ in range(rng.randint(1, 5))]
        assert solution.gcd_of_list(numbers) == math.gcd(*numbers)


def test_fibonacci_pairs_take_the_most_steps():
    fib = [1, 1]
    while len(fib) < 60:
        fib.append(fib[-1] + fib[-2])
    # 연속한 피보나치 수 (F(k+1), F(k)) 는 k - 1 번 만에 끝난다
    for k in range(3, 50):
        assert solution.gcd_steps(fib[k], fib[k - 1]) == k - 1
    # 작은 범위에서는 같은 크기의 어떤 쌍도 피보나치 쌍보다 많은 단계를 쓰지 않는다 (a ≤ 1000 에서 전수 확인)
    for a in range(2, 1001):
        worst = max(solution.gcd_steps(a, b) for b in range(1, a))
        k = max(i for i in range(2, 60) if fib[i] <= a)
        assert worst <= k - 1, (a, worst, k)


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("24 18\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["6", "72"]
