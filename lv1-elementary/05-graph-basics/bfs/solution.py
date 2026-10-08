"""BFS (너비 우선 탐색) — 가까운 정점부터 한 겹씩 넓혀 가며 탐색, 가중치 없는 그래프의 최단 거리

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 그래프는 인접 리스트 `adj[u] = [이웃, ...]` 이고 정점은 0 ~ n-1 번입니다.
- 거리는 지나온 간선의 수이고, 도달할 수 없는 정점은 -1 입니다.
- 직접 실행하면 `V E S` 와 E 개의 `u v` 를 받아, S 에서 각 정점까지의 거리를 정점 순서대로 한 줄씩 출력합니다. (번호는 1부터)
"""
import sys
from collections import deque


def bfs_order(adj: list, start: int) -> list:
    """start 에서 가까운 정점부터(같은 거리에서는 이웃 목록 순서대로) 방문한 순서."""
    visited = [False] * len(adj)
    visited[start] = True  # 큐에 넣을 때 방문 표시를 해야 같은 정점이 큐에 두 번 들어가지 않는다
    queue = deque([start])
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                queue.append(v)
    return order


def bfs_distances(adj: list, start: int) -> list:
    """start 에서 각 정점까지의 최소 간선 수. 도달할 수 없으면 -1."""
    dist = [-1] * len(adj)
    dist[start] = 0
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if dist[v] == -1:  # 거리가 정해지지 않은 정점 = 아직 방문하지 않은 정점
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist


def bfs_shortest_path(adj: list, start: int, target: int):
    """start 에서 target 까지 간선 수가 가장 적은 경로. 도달할 수 없으면 None."""
    parent = [-1] * len(adj)
    seen = [False] * len(adj)
    seen[start] = True
    queue = deque([start])
    while queue:
        u = queue.popleft()
        if u == target:
            break
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                parent[v] = u
                queue.append(v)
    if not seen[target]:
        return None
    path = [target]
    while path[-1] != start:
        path.append(parent[path[-1]])
    return path[::-1]


def bfs_levels(adj: list, start: int) -> list:
    """거리별로 묶은 정점 목록. levels[d] 는 start 에서 거리가 d 인 정점들."""
    dist = bfs_distances(adj, start)
    levels = []
    for v, d in enumerate(dist):
        if d == -1:
            continue
        while len(levels) <= d:
            levels.append([])
        levels[d].append(v)
    return levels


def main() -> None:
    input = sys.stdin.readline
    n, m, start = map(int, input().split())
    adj = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        adj[u - 1].append(v - 1)
        adj[v - 1].append(u - 1)
    print("\n".join(map(str, bfs_distances(adj, start - 1))))


if __name__ == "__main__":
    main()
