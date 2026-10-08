"""연결 요소 — 간선으로 서로 오갈 수 있는 정점들의 덩어리

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 무방향 그래프를 다룹니다. 정점은 0 ~ n-1 번이고 간선은 (u, v) 튜플입니다.
- 직접 실행하면 `N M` 과 M 개의 `u v` (번호는 1부터) 를 받아 연결 요소의 개수를 출력합니다.
"""
import sys
from collections import deque


def _adjacency(n: int, edges: list) -> list:
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def component_ids(n: int, edges: list) -> list:
    """정점마다 속한 연결 요소의 번호(0, 1, 2 … 처음 발견한 순서). 같은 번호면 서로 오갈 수 있다."""
    adj = _adjacency(n, edges)
    ids = [-1] * n
    count = 0
    for start in range(n):
        if ids[start] != -1:
            continue
        ids[start] = count
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if ids[v] == -1:
                    ids[v] = count
                    queue.append(v)
        count += 1
    return ids


def connected_components(n: int, edges: list) -> list:
    """연결 요소별 정점 목록. 각 목록은 오름차순이고, 목록들은 가장 작은 정점 순서로 나열된다."""
    ids = component_ids(n, edges)
    groups = [[] for _ in range(max(ids, default=-1) + 1)]
    for v, comp in enumerate(ids):
        groups[comp].append(v)
    return groups


def count_components(n: int, edges: list) -> int:
    return len(connected_components(n, edges))


def is_connected(n: int, edges: list) -> bool:
    return n > 0 and count_components(n, edges) == 1


def largest_component_size(n: int, edges: list) -> int:
    return max((len(g) for g in connected_components(n, edges)), default=0)


def has_cycle(n: int, edges: list) -> bool:
    """무방향 그래프에 사이클이 있는지. DFS 중에 방문한 정점을 다시 만나면(부모로 되돌아가는 간선 하나는 제외) 사이클이다.

    간선 하나로 두 정점이 이어진 것은 사이클이 아니지만, 같은 두 정점을 잇는 간선이 두 개면 사이클이다.
    자기 자신으로 가는 간선 (u, u) 는 u 의 이웃 목록에 두 번 들어가므로, 별도 처리 없이 이미 방문한 정점을 만나 사이클로 잡힌다.
    """
    adj = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        adj[u].append((v, i))
        adj[v].append((u, i))
    visited = [False] * n
    for root in range(n):
        if visited[root]:
            continue
        visited[root] = True
        stack = [(root, -1)]  # (정점, 이 정점에 도착할 때 쓴 간선의 번호)
        while stack:
            u, via = stack.pop()
            for v, edge_id in adj[u]:
                if edge_id == via:
                    continue  # 방금 온 바로 그 간선으로 되돌아가는 것은 사이클이 아니다
                if visited[v]:
                    return True
                visited[v] = True
                stack.append((v, edge_id))
    return False


def main() -> None:
    input = sys.stdin.readline
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        u, v = map(int, input().split())
        edges.append((u - 1, v - 1))
    print(count_components(n, edges))


if __name__ == "__main__":
    main()
