"""solution.py 검증: 손으로 확인한 예제 + 느리지만 확실한 풀이(브루트 포스)와의 랜덤 비교"""
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def brute_force(values: list[int]) -> int:
    """가장 단순하게 짠, 느려도 확실히 맞는 풀이"""
    total = 0
    for v in values:
        total += v
    return total


def test_sample():
    assert solution.solve([1, 2, 3]) == 6


def test_edge_cases():
    assert solution.solve([]) == 0


def test_matches_brute_force_on_random_inputs():
    rng = random.Random(0)          # 시드를 고정해 실패를 재현할 수 있게 한다
    for _ in range(300):
        values = [rng.randint(-10, 10) for _ in range(rng.randint(0, 8))]
        assert solution.solve(values) == brute_force(values), values
