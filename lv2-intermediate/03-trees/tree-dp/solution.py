"""트리 DP — 루트를 정하고, 자식 서브트리의 답을 합쳐 부모의 답을 만드는 DP

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 무방향 트리를 간선 목록 `edges = [(u, v), ...]` 와 정점 수 `n` 으로 받고, 정점 번호는 0 ~ n-1, 루트는 0 입니다.
- 각 정점 v 에서 "v 를 루트로 하는 서브트리" 만 보고 `dp[v][상태]` 를 정의합니다. 상태는 v 를 고르는지 여부 등입니다.
- 자식을 먼저 계산해야 하므로 BFS 순서를 뒤집어 처리합니다(재귀를 쓰지 않아 깊은 트리에서도 안전).
- 직접 실행하면 `N`, N 개의 정점 가중치, N-1 개의 간선을 받아 인접하지 않게 고른 정점 가중치 합의 최댓값을 출력합니다. (정점은 1부터)
"""
import sys
from collections import deque


def _rooted(n: int, edges: list[tuple[int, int]], root: int = 0) -> tuple[list[int], list[list[int]]]:
    """(부모 배열, BFS 순서 목록의 children 정보)를 만든다. 반환: (order, children). order 는 루트부터 BFS 순서."""
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    parent = [-1] * n
    order = []
    children = [[] for _ in range(n)]
    seen = [False] * n
    seen[root] = True
    queue = deque([root])
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                parent[v] = u
                children[u].append(v)
                queue.append(v)
    return order, children


def max_weight_independent_set(n: int, weights: list[int], edges: list[tuple[int, int]]) -> tuple[int, list[int]]:
    """서로 인접하지 않은 정점들을 골라 가중치 합을 최대로. (최댓값, 고른 정점들) 을 반환한다.

    dp[v][0] = v 를 고르지 않을 때 v 의 서브트리의 최대,  dp[v][1] = v 를 고를 때.
    dp[v][1] = weights[v] + Σ dp[자식][0]   (고르면 자식은 고를 수 없다)
    dp[v][0] = Σ max(dp[자식][0], dp[자식][1])"""
    if n == 0:
        return 0, []
    order, children = _rooted(n, edges)
    dp = [[0, 0] for _ in range(n)]
    for v in reversed(order):  # 자식이 부모보다 먼저 계산된다
        dp[v][1] = weights[v]
        for c in children[v]:
            dp[v][1] += dp[c][0]
            dp[v][0] += max(dp[c][0], dp[c][1])
    # 복원: 루트에서 시작해 어느 상태를 택했는지 따라 내려간다
    chosen = []
    take = {order[0]: dp[order[0]][1] > dp[order[0]][0]}
    for v in order:
        if take[v]:
            chosen.append(v)
            for c in children[v]:
                take[c] = False
        else:
            for c in children[v]:
                take[c] = dp[c][1] > dp[c][0]
    return max(dp[order[0]]), sorted(chosen)


def min_vertex_cover(n: int, edges: list[tuple[int, int]]) -> int:
    """모든 간선의 적어도 한 끝점을 포함하도록 고르는 최소 정점 수.

    dp[v][0] = v 를 고르지 않으면 모든 자식을 골라야 한다,  dp[v][1] = v 를 고르면 자식은 자유."""
    if n == 0:
        return 0
    order, children = _rooted(n, edges)
    dp = [[0, 1] for _ in range(n)]
    for v in reversed(order):
        for c in children[v]:
            dp[v][0] += dp[c][1]
            dp[v][1] += min(dp[c][0], dp[c][1])
    return min(dp[order[0]])


def min_dominating_set(n: int, edges: list[tuple[int, int]]) -> int:
    """모든 정점이 "골라졌거나 골라진 이웃이 있도록" 고르는 최소 정점 수 (지배 집합).

    세 상태: 0 = v 를 고름,  1 = v 는 안 고르고 자식 중 하나가 골라져 v 는 이미 덮임,  2 = v 는 안 고르고 아직 덮이지 않음(부모가 덮어 줄 것)."""
    if n == 0:
        return 0
    inf = float("inf")
    order, children = _rooted(n, edges)
    dp = [[0, 0, 0] for _ in range(n)]
    for v in reversed(order):
        chosen = 1  # v 를 고르면 자식은 어느 상태여도 된다
        covered_by_child = 0  # v 를 고르지 않고 자식이 덮는 경우: 자식은 상태 0 또는 1 이어야 한다
        extra = inf  # 자식 중 적어도 하나는 상태 0 이어야 v 가 덮인다
        waiting = 0  # v 가 덮이지 않은 채로 두는 경우: 자식은 상태 1 이어야 한다(자기 자신은 덮여 있어야 하므로)
        for c in children[v]:
            chosen += min(dp[c])
            best = min(dp[c][0], dp[c][1])
            covered_by_child += best
            extra = min(extra, dp[c][0] - best)
            waiting += dp[c][1]
        dp[v][0] = chosen
        dp[v][1] = covered_by_child + extra if children[v] else inf
        dp[v][2] = waiting
    root = order[0]
    return min(dp[root][0], dp[root][1])


def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    weights = list(map(int, input().split()))
    edges = []
    for _ in range(n - 1):
        a, b = map(int, input().split())
        edges.append((a - 1, b - 1))
    total, chosen = max_weight_independent_set(n, weights, edges)
    print(total)
    print(" ".join(str(v + 1) for v in chosen))


if __name__ == "__main__":
    main()
