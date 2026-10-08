"""중간에서 만나기(Meet in the Middle) — 2^n 가지를 절반씩 나눠 세어 2·2^(n/2) 로 줄이기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- n 이 40 안팎이면 모든 부분집합(2^40)을 보는 것은 불가능하지만, 절반(2^20)씩 따로 나열한 뒤 "왼쪽 값 하나에 맞는 오른쪽 값" 을 정렬 + 이진 탐색(또는 해시) 으로 찾으면 O(2^(n/2)·n) 입니다.
- subset_sums: 부분집합 합 전부 (원소를 하나씩 넣으며 목록을 두 배로). 빈 집합의 합 0 을 포함합니다.
- count_subsets_at_most: 합이 limit 이하인 부분집합 수 (빈 집합 포함).    count_subsets_with_sum: 합이 정확히 target 인 부분집합 수 (빈 집합 포함).
- closest_subset_sum: target 에 가장 가까운 부분집합 합 (같은 거리면 작은 쪽).
- knapsack_meet: 무게가 너무 커서 DP 표를 못 만드는 0/1 배낭을 풀기 (원소 수 ≤ 40 정도).
- four_sum_zero_count: 네 배열에서 하나씩 골라 합이 0 인 (i, j, k, l) 의 수 — 두 배열씩 묶어 4 중이 아니라 2 + 2 로.
- 직접 실행하면 BOJ 1450 형식 — `N C` 와 N 개의 무게 — 을 받아 무게의 합이 C 이하인 부분집합(빈 집합 포함) 의 수를 출력합니다.
"""
import sys
from bisect import bisect_left, bisect_right
from collections import Counter
from typing import Sequence


def subset_sums(values: Sequence[int]) -> list[int]:
    """모든 부분집합의 합 (길이 2^len(values), 빈 집합의 합 0 포함, 정렬되어 있지 않음)."""
    sums = [0]
    for v in values:
        sums += [s + v for s in sums]
    return sums


def _halves(values: Sequence[int]) -> tuple[Sequence[int], Sequence[int]]:
    middle = len(values) // 2
    return values[:middle], values[middle:]


def count_subsets_at_most(values: Sequence[int], limit: int) -> int:
    """합이 limit 이하인 부분집합의 수 (빈 집합 포함). 음수 원소도 된다."""
    left_part, right_part = _halves(values)
    right = sorted(subset_sums(right_part))
    return sum(bisect_right(right, limit - s) for s in subset_sums(left_part))  # 오른쪽에서 limit - s 이하인 것의 수


def count_subsets_with_sum(values: Sequence[int], target: int) -> int:
    """합이 정확히 target 인 부분집합의 수 (target 이 0 이면 빈 집합도 센다)."""
    left_part, right_part = _halves(values)
    right = Counter(subset_sums(right_part))
    return sum(right[target - s] for s in subset_sums(left_part))


def closest_subset_sum(values: Sequence[int], target: int) -> int:
    """target 에 가장 가까운 부분집합 합 (같은 거리면 작은 쪽, 빈 집합의 합 0 도 후보)."""
    left_part, right_part = _halves(values)
    right = sorted(subset_sums(right_part))
    best = None
    for s in subset_sums(left_part):
        index = bisect_left(right, target - s)  # target - s 이상인 첫 오른쪽 값과 그 바로 앞의 값이 후보
        for j in (index - 1, index):
            if 0 <= j < len(right):
                total = s + right[j]
                if best is None or (abs(total - target), total) < (abs(best - target), best):
                    best = total
    return best


def knapsack_meet(items: Sequence[tuple[int, int]], capacity: int) -> int:
    """items = [(무게, 가치), …] (무게·가치 ≥ 0). 무게의 합이 capacity 이하인 부분집합의 최대 가치.
    오른쪽 절반의 (무게, 가치) 를 무게순으로 정렬하고 가치의 prefix 최댓값을 만들어 두면, 왼쪽 부분집합마다 남은 무게에 들어가는 최선을 이진 탐색으로 찾는다."""

    def enumerate_half(half: Sequence[tuple[int, int]]) -> list[tuple[int, int]]:
        pairs = [(0, 0)]
        for w, v in half:
            pairs += [(pw + w, pv + v) for pw, pv in pairs]
        return pairs

    middle = len(items) // 2
    right = sorted(enumerate_half(items[middle:]))
    weights = [w for w, _ in right]
    best_value = []  # best_value[i] = right[0..i] 중 가치의 최댓값
    running = 0
    for _, v in right:
        running = max(running, v)
        best_value.append(running)
    best = 0
    for w, v in enumerate_half(items[:middle]):
        if w > capacity:
            continue
        index = bisect_right(weights, capacity - w) - 1  # 남은 무게에 들어가는 오른쪽 부분집합 중 가장 무거운 것의 위치. (0, 0) 이 있어 index ≥ 0
        best = max(best, v + best_value[index])
    return best


def four_sum_zero_count(a: Sequence[int], b: Sequence[int], c: Sequence[int], d: Sequence[int]) -> int:
    """a[i] + b[j] + c[k] + d[l] == 0 인 (i, j, k, l) 의 수. O(n²) 시간·공간 (4 중 반복의 O(n⁴) 대신)."""
    pair_sums = Counter(x + y for x in a for y in b)
    return sum(pair_sums[-(x + y)] for x in c for y in d)


def main() -> None:
    data = sys.stdin.read().split()
    n, limit = int(data[0]), int(data[1])
    print(count_subsets_at_most([int(x) for x in data[2 : 2 + n]], limit))


if __name__ == "__main__":
    main()
