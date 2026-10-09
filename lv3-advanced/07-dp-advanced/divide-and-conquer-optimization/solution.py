"""분할 정복 최적화(Divide and Conquer Optimization) — dp[k][i] = min_j dp[k-1][j] + cost(j, i) 를 O(k n log n) 에

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 문제 모양: 앞에서부터 n 개를 k 개의 연속한 묶음으로 나누고, 묶음 (j, i] (j+1 번째부터 i 번째까지) 의 비용이 cost(j, i) 일 때 비용의 합의 최솟값.
  dp[g][i] = g 개의 묶음으로 앞 i 개를 나눈 최소 비용 = min over j<i of dp[g-1][j] + cost(j, i).  직접 구하면 O(k n²).
- 조건: opt(g, i) (최소를 만드는 가장 작은 j) 가 i 에 대해 단조 증가. cost 가 사각 부등식(monge)  cost(a,c) + cost(b,d) ≤ cost(a,d) + cost(b,c)  (a ≤ b ≤ c ≤ d) 를 만족하면 성립합니다.
- 방법: 가운데 i = mid 의 최적 j 를 j 의 허용 범위 [opt_lo, opt_hi] 에서 모두 확인해 찾고, mid 의 왼쪽은 [opt_lo, j*] 에서, 오른쪽은 [j*, opt_hi] 에서만 찾는다.
  한 층의 모든 i 를 O(n log n) 에 계산한다. 재귀의 깊이는 log n 이라 안전합니다.
- partition_cost: 이 방법으로 n 개를 정확히 k 개(비어 있지 않은)의 묶음으로 나눌 때의 최소 비용. naive_partition_cost 는 O(k n²) 기준 구현.
- 직접 실행하면 구역 분할 예제 형식 — `L G` 와 L 개의 위험도 — 을 받아, 감옥을 G 개의 연속한 구역으로 나눌 때 (구역 크기 × 구역 위험도의 합) 의 합의 최솟값을 출력합니다.
"""
import sys
from typing import Callable, Optional, Sequence

INF = float("inf")
Cost = Callable[[int, int], int]


def cost_size_times_sum(values: Sequence[int]) -> Cost:
    """cost(j, i) = (i - j) · (values[j] + … + values[i-1]). 값이 음이 아니면 Monge 비용."""
    prefix = [0]
    for v in values:
        prefix.append(prefix[-1] + v)
    return lambda j, i: (i - j) * (prefix[i] - prefix[j])


def cost_square_of_sum(values: Sequence[int]) -> Cost:
    """cost(j, i) = (values[j] + … + values[i-1])²  — 값이 음이 아니면 monge."""
    prefix = [0]
    for v in values:
        prefix.append(prefix[-1] + v)
    return lambda j, i: (prefix[i] - prefix[j]) ** 2


def is_monge(n: int, cost: Cost) -> bool:
    """0 ≤ a ≤ b ≤ c ≤ d ≤ n 인 모든 네 점에서 cost(a,c) + cost(b,d) ≤ cost(a,d) + cost(b,c) 인지 (O(n⁴), 작은 n 의 확인용)."""
    for a in range(n + 1):
        for b in range(a, n + 1):
            for c in range(b + 1, n + 1):  # cost(b, c) 는 b < c 일 때만 의미가 있다
                for d in range(c, n + 1):
                    if cost(a, c) + cost(b, d) > cost(a, d) + cost(b, c):
                        return False
    return True


def next_layer(previous: Sequence, n: int, cost: Cost, low: int) -> tuple[list, list]:
    """previous[j] (j = 0..n) 로부터 cur[i] = min_{low ≤ j < i} previous[j] + cost(j, i) 와 그 최적 j 를 i = low+1..n 에 대해 구한다.
    previous[j] 가 INF 인 j 는 쓸 수 없다. 결과는 길이 n + 1 의 리스트 (i ≤ low 인 칸은 INF, -1)."""
    current = [INF] * (n + 1)
    best_j = [-1] * (n + 1)
    # (구하려는 i 의 구간 [lo, hi], 최적 j 가 있을 수 있는 구간 [opt_lo, opt_hi]) 를 스택으로 처리
    stack = [(low + 1, n, low, n - 1)]
    while stack:
        lo, hi, opt_lo, opt_hi = stack.pop()
        if lo > hi:
            continue
        mid = (lo + hi) // 2
        best_value, best_choice = INF, -1
        for j in range(opt_lo, min(mid - 1, opt_hi) + 1):  # j < mid
            value = previous[j] + cost(j, mid)
            if value < best_value:
                best_value, best_choice = value, j
        current[mid], best_j[mid] = best_value, best_choice
        stack.append((lo, mid - 1, opt_lo, best_choice))
        stack.append((mid + 1, hi, best_choice, opt_hi))
    return current, best_j


def partition_cost(n: int, k: int, cost: Cost) -> int:
    """앞 n 개를 정확히 k 개의 비어 있지 않은 연속한 묶음으로 나눌 때 비용 합의 최솟값 (cost 가 monge 라고 가정)."""
    if not 1 <= k <= n:
        raise ValueError("1 ≤ k ≤ n 이어야 합니다")
    layer = [INF] + [cost(0, i) for i in range(1, n + 1)]  # 묶음 1 개: dp[1][i] = cost(0, i)
    layer[0] = INF
    for g in range(2, k + 1):
        previous = layer
        layer, _ = next_layer(previous, n, cost, g - 1)  # g 개로 나누려면 앞의 g-1 개 묶음에 최소 g-1 개 원소
    return layer[n]


def naive_partition_cost(n: int, k: int, cost: Cost) -> int:
    """O(k n²) 기준 구현."""
    if not 1 <= k <= n:
        raise ValueError("1 ≤ k ≤ n 이어야 합니다")
    previous = [INF] + [cost(0, i) for i in range(1, n + 1)]
    for _ in range(2, k + 1):
        previous = [INF] + [min((previous[j] + cost(j, i) for j in range(1, i)), default=INF) for i in range(1, n + 1)]
    return previous[n]


def main() -> None:
    data = sys.stdin.read().split()
    length, groups = int(data[0]), int(data[1])
    values = [int(x) for x in data[2 : 2 + length]]
    print(partition_cost(length, min(groups, length), cost_size_times_sum(values)))


if __name__ == "__main__":
    main()
