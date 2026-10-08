"""에일리언 트릭(Aliens trick, WQS 이분 탐색 / 라그랑주 완화) — "정확히 k 개" 제약을 항목당 벌점 λ 로 바꿔 이분 탐색하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 문제: 항목을 정확히 k 개 골라 값 F(k) 를 최대(또는 최소)로 하는 DP 가 O(n·k) 이상 걸린다. F 가 k 에 대해 **오목(최대화) / 볼록(최소화)** 이면,
  항목 하나당 벌점 λ 를 매긴 완화 문제 h(λ) = max_c ( F(c) - λ·c ) 는 "개수 제한 없음" 이라 O(n) 쯤으로 풀리고, 최적일 때의 개수 c(λ) 는 λ 가 클수록 줄어든다 (단조).
  c(λ) 가 k 이상인 가장 큰 정수 λ 를 이분 탐색으로 찾으면, 그 λ 에서 k 가 최적 개수 구간에 들어 있어 F(k) = h(λ) + λ·k.
- 동점 처리가 핵심: 완화 문제의 최적해가 여러 개수를 가질 수 있으므로, evaluate 는 최적값이 같을 때 **개수가 가장 많은 쪽** 을 돌려줘야 한다 (이 파일의 모든 evaluate 가 그렇게 한다).
- aliens_trick(evaluate, k, low, high, maximize): evaluate(λ) -> (완화 문제의 최적값, 최대 개수). [low, high] 는 λ 의 탐색 범위 (정수).
- 응용 세 가지 (각각 느린 DP 로 교차 검증):
  ① max_sum_k_subarrays(a, k): 서로 겹치지 않는 k 개의 비어 있지 않은 구간의 합의 최댓값 (인접 허용 여부 선택). 벌점 DP 는 O(n).
  ② partition_min_cost(n, cost, k): 1..n 을 k 개의 연속 구간으로 나눠 구간 비용 cost(l, r) 의 합 최소화 (비용이 사각 부등식을 만족해야 F 가 볼록). 벌점 DP 는 O(n²).
  ③ partition_sum_of_squares(a, k): 음이 아닌 수열을 k 개의 연속 구간으로 나눠 (구간 합)² 의 합 최소화. 벌점 DP 를 볼록 껍질 트릭으로 O(n).
- 직접 실행하면 BOJ 2228 "구간 나누기" 와 같은 형태 — `N M`, 이어서 N 개의 정수 — 를 받아 서로 인접하지 않는 M 개의 구간의 합의 최댓값을 출력합니다.
"""
import sys
from typing import Callable, Optional, Sequence

NEG = float("-inf")


def aliens_trick(
    evaluate: Callable[[int], tuple[int, int]],
    k: int,
    low: int,
    high: int,
    maximize: bool = True,
) -> int:
    """F(k). evaluate(lam) 은 (완화 문제의 최적값, 그 최적해들 중 가장 많은 개수) 를 돌려준다.
    maximize=True: 최적값 = max_c (F(c) - lam·c) 이고 F(k) = 값 + lam·k.  maximize=False: 최적값 = min_c (F(c) + lam·c) 이고 F(k) = 값 - lam·k.
    개수는 lam 이 클수록 줄어든다. [low, high] 안에서 개수 ≥ k 인 가장 큰 lam 을 찾는다 (low 에서도 개수가 k 미만이면 k 개는 불가능)."""
    if low > high:
        raise ValueError("low ≤ high 여야 합니다")
    if evaluate(low)[1] < k:
        raise ValueError("k 개를 고를 수 없습니다 (low 에서도 최대 개수가 k 미만)")
    lo, hi = low, high  # 불변: 개수(lo) ≥ k
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if evaluate(mid)[1] >= k:
            lo = mid
        else:
            hi = mid - 1
    value, _ = evaluate(lo)
    return value + lo * k if maximize else value - lo * k


def _penalized_subarrays(a: Sequence[int], lam: int, allow_adjacent: bool) -> tuple[int, int]:
    """max over c of (c 개의 서로 겹치지 않는 구간의 합 - lam·c) 과, 최적일 때의 최대 c. (값, 개수) 튜플 비교가 동점에서 개수가 많은 쪽을 고른다."""
    outside = (0, 0)  # 직전 원소가 어느 구간에도 속하지 않는 상태
    inside = (NEG, 0)  # 직전 원소가 구간에 속한(열려 있는) 상태
    for x in a:
        start_from = max(outside, inside) if allow_adjacent else outside  # 새 구간을 시작할 수 있는 상태
        extend = (inside[0] + x, inside[1])
        begin = (start_from[0] + x - lam, start_from[1] + 1)
        new_inside = max(extend, begin)
        new_outside = max(outside, inside)  # 이 원소를 쓰지 않는다
        outside, inside = new_outside, new_inside
    return max(outside, inside)


def max_sum_k_subarrays(a: Sequence[int], k: int, allow_adjacent: bool = False) -> int:
    """서로 겹치지 않는 비어 있지 않은 연속 구간 k 개의 합의 최댓값 (allow_adjacent=False 면 구간 사이에 원소가 하나 이상 있어야 한다). O(n log 값)."""
    n = len(a)
    limit = n if allow_adjacent else (n + 1) // 2
    if k < 0 or k > limit:
        raise ValueError("k 개의 구간을 고를 수 없습니다")
    bound = 2 * sum(abs(x) for x in a) + 1
    return aliens_trick(lambda lam: _penalized_subarrays(a, lam, allow_adjacent), k, -bound, bound, maximize=True)


def max_sum_k_subarrays_dp(a: Sequence[int], k: int, allow_adjacent: bool = False) -> int:
    """교차 검증용 O(n·k) DP."""
    n = len(a)
    outside = [NEG] * (k + 1)  # outside[c]: 지금까지 c 개의 구간을 닫았고 직전 원소는 구간 밖
    inside = [NEG] * (k + 1)  # inside[c]: 지금 c 번째 구간이 열려 있다
    outside[0] = 0
    for x in a:
        new_outside, new_inside = [NEG] * (k + 1), [NEG] * (k + 1)
        for c in range(k + 1):
            new_outside[c] = max(outside[c], inside[c])
            if c >= 1:
                start = max(outside[c - 1], inside[c - 1]) if allow_adjacent else outside[c - 1]
                new_inside[c] = max(inside[c] + x, start + x)
        outside, inside = new_outside, new_inside
    result = max(outside[k], inside[k])
    if result == NEG:
        raise ValueError("k 개의 구간을 고를 수 없습니다")
    return int(result)


def partition_min_cost(n: int, cost: Callable[[int, int], int], k: int) -> int:
    """0..n 을 k 개의 연속 구간 [l, r) 로 나눈 구간 비용의 합의 최솟값. cost(l, r) 은 0 이상이고 사각 부등식을 만족해야 한다 (그래야 k 에 대해 볼록). O(n² log)."""
    if not 1 <= k <= n:
        raise ValueError("1 ≤ k ≤ n 이어야 합니다")

    def evaluate(lam: int) -> tuple[int, int]:
        best: list[tuple[int, int]] = [(0, 0)] + [(10**30, 0)] * n  # (비용 + lam·구간 수, 구간 수)
        for i in range(1, n + 1):
            candidate = (10**30, 0)
            for j in range(i):
                value = best[j][0] + cost(j, i) + lam
                # 동점이면 구간 수가 많은 쪽: (값, -개수) 가 작은 쪽을 고른다
                if (value, -(best[j][1] + 1)) < (candidate[0], -candidate[1]):
                    candidate = (value, best[j][1] + 1)
            best[i] = candidate
        return best[n]

    bound = max(cost(0, n), sum(cost(i, i + 1) for i in range(n))) + 1
    return aliens_trick(evaluate, k, -bound, bound, maximize=False)


def partition_min_cost_dp(n: int, cost: Callable[[int, int], int], k: int) -> int:
    """교차 검증용 O(n²·k) DP."""
    INF = float("inf")
    dp = [[INF] * (n + 1) for _ in range(k + 1)]
    dp[0][0] = 0
    for c in range(1, k + 1):
        for i in range(1, n + 1):
            dp[c][i] = min(dp[c - 1][j] + cost(j, i) for j in range(i))
    return int(dp[k][n])


def partition_sum_of_squares(a: Sequence[int], k: int) -> int:
    """음이 아닌 수열을 k 개의 연속 구간으로 나눠 (구간 합)² 의 합을 최소화. 벌점 DP 를 볼록 껍질 트릭(단조 큐)으로 O(n) 에 푼다."""
    n = len(a)
    if any(x < 0 for x in a):
        raise ValueError("음이 아닌 수열이어야 합니다 (접두사 합이 단조여야 단조 큐를 쓸 수 있습니다)")
    if not 1 <= k <= n:
        raise ValueError("1 ≤ k ≤ n 이어야 합니다")
    prefix = [0]
    for x in a:
        prefix.append(prefix[-1] + x)
    scale = n + 1  # 동점에서 구간 수가 많은 쪽을 고르기 위해 값에 scale 을 곱하고 구간마다 1 을 뺀다: 값' = 값·scale - 개수

    def evaluate(lam: int) -> tuple[int, int]:
        # dp'[i] = min_j dp'[j] + scale·(P_i - P_j)² + scale·lam - 1.  직선 j: 기울기 -2·scale·P_j, 절편 dp'[j] + scale·P_j², 질의 x = P_i (비감소)
        dp = [0] * (n + 1)
        hull: list[tuple[int, int]] = [(0, 0)]  # (기울기, 절편)
        head = 0
        for i in range(1, n + 1):
            x = prefix[i]
            while head + 1 < len(hull) and hull[head + 1][0] * x + hull[head + 1][1] <= hull[head][0] * x + hull[head][1]:
                head += 1
            m, b = hull[head]
            dp[i] = m * x + b + scale * x * x + scale * lam - 1
            line = (-2 * scale * prefix[i], dp[i] + scale * prefix[i] ** 2)
            while len(hull) - head >= 2:
                (m1, b1), (m2, b2) = hull[-2], hull[-1]
                # 마지막 직선이 새 직선과 그 앞 직선 사이에서 한 번도 최소가 아니면 버린다 (교점 비교를 곱셈으로)
                if (line[1] - b1) * (m1 - m2) <= (b2 - b1) * (m1 - line[0]):
                    hull.pop()
                else:
                    break
            hull.append(line)
        total = dp[n]
        count = (-total) % scale
        return (total + count) // scale, count

    bound = (prefix[-1] ** 2) + 1
    return aliens_trick(evaluate, k, -bound, bound, maximize=False)


def convexity_violations(values: Sequence[int]) -> list[int]:
    """F(1), F(2), … 에서 볼록(2차 차분 ≥ 0) 이 깨지는 위치 c (F(c-1) + F(c+1) < 2·F(c)). 에일리언 트릭을 쓸 수 있는지 검사할 때."""
    return [c for c in range(1, len(values) - 1) if values[c - 1] + values[c + 1] < 2 * values[c]]


def main() -> None:
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    print(max_sum_k_subarrays([int(x) for x in data[2 : 2 + n]], m))


if __name__ == "__main__":
    main()
