"""그리디 — 매 단계에서 지금 가장 좋아 보이는 선택을 하고, 한 번 고른 것은 되돌리지 않기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 그리디가 맞으려면 "지금의 최선이 전체의 최선으로 이어진다"는 증명(보통 교환 논증)이 있어야 합니다.
- 틀리는 예(동전 [1, 3, 4])와 맞는 예(활동 선택, 쪼갤 수 있는 배낭)를 함께 둡니다.
- 직접 실행하면 `L P V` 를 받아 캠핑장을 쓸 수 있는 최대 일수를 출력합니다.
"""
import sys
from fractions import Fraction


def max_camping_days(l: int, p: int, v: int) -> int:
    """P 일마다 L 일만 쓸 수 있는 캠핑장을 V 일의 휴가 동안 최대 며칠 쓰는가.

    P 일짜리 한 주기마다 L 일을 다 쓰는 게 최선이고, 마지막에 남는 (v % p) 일은 L 일까지만 쓸 수 있다."""
    return l * (v // p) + min(l, v % p)


def greedy_coin_change(coins: list, amount: int) -> int:
    """큰 동전부터 최대한 쓴다. 필요한 동전 수를 반환하고, 정확히 맞추지 못하면 -1.

    동전 단위가 서로 배수 관계(예: 1, 5, 10, 50, 100, 500)일 때만 최적이다."""
    count = 0
    for coin in sorted(coins, reverse=True):
        count += amount // coin
        amount %= coin
    return count if amount == 0 else -1


def min_coins_dp(coins: list, amount: int) -> int:
    """어떤 동전 체계에서도 맞는 답(비교용). best[a] = a 원을 만드는 최소 동전 수. 못 만들면 -1."""
    inf = float("inf")
    best = [0] + [inf] * amount
    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a and best[a - coin] + 1 < best[a]:
                best[a] = best[a - coin] + 1
    return best[amount] if best[amount] != inf else -1


def fractional_knapsack(items: list, capacity: int) -> Fraction:
    """쪼갤 수 있는 물건을 담을 때의 최대 가치. items = [(가치, 무게), ...].

    무게당 가치가 큰 것부터 담고, 마지막 하나만 쪼갠다. 정확한 값을 위해 Fraction 으로 반환한다."""
    total = Fraction(0)
    for value, weight in sorted(items, key=lambda it: Fraction(it[0], it[1]), reverse=True):
        if capacity <= 0:
            break
        take = min(weight, capacity)
        total += Fraction(value * take, weight)
        capacity -= take
    return total


def activity_selection(intervals: list) -> list:
    """겹치지 않게 고를 수 있는 구간의 최대 개수와 그 구간들. intervals = [(시작, 끝), ...].

    끝나는 시간이 빠른 것부터 고른다. 끝과 시작이 같은 구간끼리는 겹치지 않는다고 본다.
    끝이 같으면 시작이 빠른 것을 먼저 보아야 (3, 3) 같은 길이 0 구간을 놓치지 않는다."""
    chosen = []
    last_end = float("-inf")
    for start, end in sorted(intervals, key=lambda it: (it[1], it[0])):
        if start >= last_end:
            chosen.append((start, end))
            last_end = end
    return chosen


def main() -> None:
    l, p, v = map(int, sys.stdin.readline().split())
    print(max_camping_days(l, p, v))


if __name__ == "__main__":
    main()
