"""배낭 문제 — 무게 한도 안에서 가치의 합을 최대로 (0/1, 무한, 개수 제한) 와 그 변형들(동전 문제, 부분집합의 합)

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 물건은 `(무게, 가치)` 로 받습니다. dp[w] = 무게 한도 w 에서의 최대 가치. 물건 하나를 차례로 고려하며 표를 갱신합니다.
- 0/1 배낭은 물건을 한 번만 쓰므로 한도를 큰 쪽에서 작은 쪽으로 갱신하고(1 차원 표), 무한 배낭은 작은 쪽에서 큰 쪽으로 갱신합니다.
- 직접 실행하면 `N K` 와 N 개의 `W V` 를 받아 무게 K 이하로 담을 수 있는 가치의 최댓값을 출력합니다.
"""
import sys

NEG_INF = float("-inf")


def knapsack_table(items: list[tuple[int, int]], capacity: int) -> list[list[int]]:
    """2 차원 표 dp[i][w] = 앞의 i 개 물건만 쓰고 무게 한도가 w 일 때의 최대 가치. 복원과 설명을 위한 가장 기본형."""
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        weight, value = items[i - 1]
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]  # i 번째를 안 담는다
            if w >= weight:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - weight] + value)  # 담는다
    return dp


def knapsack_01(items: list[tuple[int, int]], capacity: int) -> int:
    """0/1 배낭의 1 차원 표. w 를 큰 쪽에서 작은 쪽으로 돌아야 같은 물건을 두 번 쓰지 않는다. 공간 O(K)."""
    dp = [0] * (capacity + 1)
    for weight, value in items:
        for w in range(capacity, weight - 1, -1):
            if dp[w - weight] + value > dp[w]:
                dp[w] = dp[w - weight] + value
    return dp[capacity]


def knapsack_01_items(items: list[tuple[int, int]], capacity: int) -> tuple[int, list[int]]:
    """(최대 가치, 담은 물건의 번호들). 2 차원 표를 거꾸로 따라가며 i 번째를 담았는지 확인한다."""
    dp = knapsack_table(items, capacity)
    chosen = []
    w = capacity
    for i in range(len(items), 0, -1):
        if dp[i][w] != dp[i - 1][w]:  # i 번째를 안 담았다면 값이 같았을 것이다
            chosen.append(i - 1)
            w -= items[i - 1][0]
    return dp[len(items)][capacity], sorted(chosen)


def knapsack_unbounded(items: list[tuple[int, int]], capacity: int) -> int:
    """물건을 몇 개든 쓸 수 있는 배낭. w 를 작은 쪽에서 큰 쪽으로 돌면 같은 물건을 여러 번 쓸 수 있다."""
    dp = [0] * (capacity + 1)
    for weight, value in items:
        for w in range(weight, capacity + 1):
            if dp[w - weight] + value > dp[w]:
                dp[w] = dp[w - weight] + value
    return dp[capacity]


def knapsack_bounded(items: list[tuple[int, int, int]], capacity: int) -> int:
    """물건마다 쓸 수 있는 개수가 정해진 배낭. items = [(무게, 가치, 개수), ...].

    개수 c 를 1, 2, 4, …, 나머지로 쪼개면 그 묶음들의 부분집합으로 0 ~ c 의 모든 개수를 만들 수 있다. 쪼갠 묶음을 0/1 물건으로 푼다."""
    pieces = []
    for weight, value, count in items:
        k = 1
        while count > 0:
            take = min(k, count)
            pieces.append((weight * take, value * take))
            count -= take
            k *= 2
    return knapsack_01(pieces, capacity)


def min_coins(coins: list[int], amount: int) -> int:
    """amount 를 만드는 최소 동전 수 (동전은 무한히 쓸 수 있다). 만들 수 없으면 -1. 무한 배낭의 '개수' 버전."""
    inf = float("inf")
    dp = [0] + [inf] * amount
    for coin in coins:
        for a in range(coin, amount + 1):
            if dp[a - coin] + 1 < dp[a]:
                dp[a] = dp[a - coin] + 1
    return dp[amount] if dp[amount] != inf else -1


def count_coin_ways(coins: list[int], amount: int) -> int:
    """amount 를 만드는 서로 다른 조합의 수 (순서는 무시: 1+2 와 2+1 은 같다). 동전을 바깥 반복으로 돌려야 순서가 구분되지 않는다."""
    dp = [1] + [0] * amount
    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] += dp[a - coin]
    return dp[amount]


def count_coin_orderings(coins: list[int], amount: int) -> int:
    """순서까지 구분하는 경우의 수 (1+2 와 2+1 은 다르다). 금액을 바깥 반복으로 돌린다."""
    dp = [1] + [0] * amount
    for a in range(1, amount + 1):
        for coin in coins:
            if a >= coin:
                dp[a] += dp[a - coin]
    return dp[amount]


def subset_sum(numbers: list[int], target: int) -> bool:
    """일부 수를 골라 합이 정확히 target 이 될 수 있는가 (numbers 는 0 이상). 가치 = 무게인 0/1 배낭의 가능 여부 버전."""
    if target < 0:
        return False
    reachable = [True] + [False] * target
    for x in numbers:
        for s in range(target, x - 1, -1):
            if reachable[s - x]:
                reachable[s] = True
    return reachable[target]


def can_partition_equal(numbers: list[int]) -> bool:
    """수들을 합이 같은 두 묶음으로 나눌 수 있는가."""
    total = sum(numbers)
    return total % 2 == 0 and subset_sum(numbers, total // 2)


def main() -> None:
    input = sys.stdin.readline
    n, k = map(int, input().split())
    items = [tuple(map(int, input().split())) for _ in range(n)]
    print(knapsack_01(items, k))


if __name__ == "__main__":
    main()
