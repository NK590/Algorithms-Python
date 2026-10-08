"""시간 복잡도 — 입력 크기에 따라 연산 횟수가 얼마나 늘어나는지 읽는 법

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 반복문이 몇 번 도는지를 직접 세어 보고, 공식과 같은지 확인합니다.
- `max_n` 은 "1초에 약 1억 번" 이라는 어림값에서 복잡도별로 풀 수 있는 최대 입력 크기를 구합니다.
- 직접 실행하면 복잡도 이름(예: `n^2`)을 한 줄씩 받아, 연산 1억 번 안에 풀 수 있는 최대 n 을 출력합니다.
"""
import math
import sys

# 복잡도 이름 → 입력 크기 n 에서의 연산 횟수
COST = {
    "n": lambda n: n,
    "n log n": lambda n: n * math.log2(n) if n > 1 else 0,
    "n^2": lambda n: n ** 2,
    "n^3": lambda n: n ** 3,
    "2^n": lambda n: 2 ** n,
    "n!": lambda n: math.factorial(n),
}


def count_single_loop(n: int) -> int:
    """for i in range(n) : n 번 → O(n)"""
    count = 0
    for _ in range(n):
        count += 1
    return count


def count_nested_loops(n: int) -> int:
    """이중 반복문: n × n 번 → O(n²)"""
    count = 0
    for _ in range(n):
        for _ in range(n):
            count += 1
    return count


def count_triangle_loops(n: int) -> int:
    """안쪽 반복이 i 번인 이중 반복문: 0 + 1 + ... + (n-1) = n(n-1)/2 번 → 여전히 O(n²)"""
    count = 0
    for i in range(n):
        for _ in range(i):
            count += 1
    return count


def count_halving(n: int) -> int:
    """매번 절반으로 줄이는 반복: ⌊log2 n⌋ 번 → O(log n)"""
    count = 0
    while n > 1:
        n //= 2
        count += 1
    return count


def count_sqrt_loop(n: int) -> int:
    """d*d <= n 인 동안 도는 반복: ⌊√n⌋ 번 → O(√n)"""
    count = 0
    d = 1
    while d * d <= n:
        d += 1
        count += 1
    return count


def max_n(complexity: str, budget: int = 10 ** 8) -> int:
    """연산 횟수가 budget 을 넘지 않는 가장 큰 n. 연산 횟수는 n 이 클수록 늘어나므로 이분 탐색한다."""
    cost = COST[complexity]
    low, high = 1, 2
    while cost(high) <= budget:  # 답이 들어 있는 구간의 위쪽 끝을 두 배씩 늘려 가며 찾는다
        low, high = high, high * 2
    while high - low > 1:
        mid = (low + high) // 2
        if cost(mid) <= budget:
            low = mid
        else:
            high = mid
    return low


def main() -> None:
    for line in sys.stdin:
        name = line.strip()
        if name:
            print(max_n(name))


if __name__ == "__main__":
    main()
