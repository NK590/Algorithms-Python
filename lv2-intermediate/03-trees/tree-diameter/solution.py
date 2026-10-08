"""트리의 지름 — 트리에서 가장 멀리 떨어진 두 정점 사이의 거리(경로 길이)

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 가중치가 있는 무방향 트리를 간선 목록 `edges = [(u, v, w), ...]` 와 정점 수 `n` 으로 받고, 정점 번호는 0 ~ n-1 입니다.
  가중치는 0 이상이어야 합니다. (음수 가중치에서는 두 번 탐색하는 방법이 틀립니다)
- 두 가지 방법: ① 임의의 정점에서 가장 먼 정점 u 를 찾고, u 에서 가장 먼 정점 v 를 찾는다 → (u, v) 가 지름의 양 끝
  ② 트리 DP: 각 정점에서 (가장 깊은 두 자식 방향의 합) 의 최댓값.
- 직접 실행하면 `N`, N-1 개의 간선 `A B C` 를 받아 지름의 길이를 출력합니다. (정점은 1부터)
"""
import sys
from collections import deque

Edge = tuple[int, int, int]


def _adjacency(n: int, edges: list[Edge]) -> list[list[tuple[int, int]]]:
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj


def distances_from(adj: list[list[tuple[int, int]]], source: int) -> tuple[list[int], list[int]]:
    """source 에서 모든 정점까지의 거리와 BFS 트리의 부모. 트리에서는 경로가 하나뿐이라 BFS 로 충분하다."""
    n = len(adj)
    dist = [-1] * n
    parent = [-1] * n
    dist[source] = 0
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v, w in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + w
                parent[v] = u
                queue.append(v)
    return dist, parent


def tree_diameter(n: int, edges: list[Edge]) -> tuple[int, int, int]:
    """(지름의 길이, 한 끝점, 다른 끝점). 정점이 하나면 (0, 0, 0). 연결된 트리여야 한다."""
    if n <= 1:
        return 0, 0, 0
    adj = _adjacency(n, edges)
    d0, _ = distances_from(adj, 0)
    u = max(range(n), key=lambda x: d0[x])  # 어느 정점에서든 가장 먼 정점은 지름의 한 끝점이다
    du, _ = distances_from(adj, u)
    v = max(range(n), key=lambda x: du[x])
    return du[v], u, v


def diameter_path(n: int, edges: list[Edge]) -> list[int]:
    """지름을 이루는 경로의 정점 목록 (한 끝점에서 다른 끝점까지)."""
    if n <= 1:
        return [0] if n == 1 else []
    adj = _adjacency(n, edges)
    _, u, v = tree_diameter(n, edges)
    _, parent = distances_from(adj, u)
    path = [v]
    while path[-1] != u:
        path.append(parent[path[-1]])
    return path


def tree_diameter_dp(n: int, edges: list[Edge]) -> int:
    """트리 DP 로 구한 지름. down[v] = v 에서 서브트리 안으로 내려가는 가장 긴 경로.
    v 를 "꼭대기" 로 하는 가장 긴 경로 = (가장 긴 두 자식 방향 down + 간선 가중치) 의 합. 음수 가중치가 없다는 가정 위에서 맞다."""
    if n <= 1:
        return 0
    adj = _adjacency(n, edges)
    order, parent = [], [-1] * n
    seen = [False] * n
    seen[0] = True
    stack = [0]
    while stack:
        u = stack.pop()
        order.append(u)
        for v, w in adj[u]:
            if not seen[v]:
                seen[v] = True
                parent[v] = u
                stack.append(v)
    down = [0] * n
    best = 0
    top1 = [0] * n  # 가장 긴 자식 방향
    top2 = [0] * n  # 두 번째로 긴 자식 방향
    for v in reversed(order):
        best = max(best, top1[v] + top2[v])
        p = parent[v]
        if p != -1:
            weight = next(w for x, w in adj[v] if x == p)
            length = down[v] = top1[v] + weight
            if length > top1[p]:
                top1[p], top2[p] = length, top1[p]
            elif length > top2[p]:
                top2[p] = length
    return best


def eccentricities(n: int, edges: list[Edge]) -> list[int]:
    """각 정점에서 가장 먼 정점까지의 거리. 어떤 정점에서든 가장 먼 정점은 지름의 두 끝점 중 하나이므로
    max(u 까지의 거리, v 까지의 거리) 로 구한다. BFS 두 번이면 모든 정점의 답이 나온다."""
    if n == 0:
        return []
    if n == 1:
        return [0]
    adj = _adjacency(n, edges)
    _, u, v = tree_diameter(n, edges)
    du, _ = distances_from(adj, u)
    dv, _ = distances_from(adj, v)
    return [max(du[x], dv[x]) for x in range(n)]


def tree_centers(n: int, edges: list[Edge]) -> list[int]:
    """트리의 중심: 가장 먼 정점까지의 거리가 최소인 정점 (한 개 또는 인접한 두 개). 지름 경로의 가운데에 있다."""
    ecc = eccentricities(n, edges)
    if not ecc:
        return []
    smallest = min(ecc)
    return [x for x in range(n) if ecc[x] == smallest]


def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    edges = []
    for _ in range(n - 1):
        a, b, c = map(int, input().split())
        edges.append((a - 1, b - 1, c))
    print(tree_diameter(n, edges)[0])


if __name__ == "__main__":
    main()
