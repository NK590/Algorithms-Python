"""벨만-포드 알고리즘 — 음수 간선이 있어도 되는 단일 시작점 최단 거리, 음수 사이클 탐지

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 간선 목록 `edges = [(u, v, w), ...]` (u → v, 가중치 w) 와 정점 수 `n` 으로 받고, 정점 번호는 0 ~ n-1 입니다.
- 모든 간선을 훑는 "라운드"를 최대 n 번 반복합니다. 최단 경로는 간선이 최대 n-1 개이므로 n-1 라운드면 확정되고,
  n 번째 라운드에서도 갱신되면 음수 사이클이 있다는 뜻입니다.
- 도달할 수 없는 정점의 거리는 INF 입니다.
- 직접 실행하면 아래 형식의 입력을 받아 1번 정점에서 각 정점까지의 거리를 출력합니다. (음수 사이클이 있으면 -1 한 줄)

      N M          정점 수, 간선 수
      A B C        (M 줄) A → B 간선, 가중치 C (음수 가능)
"""
import sys
from collections import deque

INF = float("inf")

Edge = tuple[int, int, int]


def bellman_ford(n: int, edges: list[Edge], start: int) -> tuple[list[float], bool]:
    """(dist, negative_cycle) 를 반환한다.

    negative_cycle 이 True 이면 start 에서 도달할 수 있는 음수 사이클이 있다는 뜻이고, 이때 dist 는 믿을 수 없다."""
    dist = [INF] * n
    dist[start] = 0
    for _ in range(n):  # 마지막(n 번째) 라운드는 음수 사이클 확인용
        changed = False
        for u, v, w in edges:
            # INF 가 float("inf") 라서 도달하지 못한 정점에서는 inf + w = inf 가 되어 갱신되지 않는다.
            # (INF 를 큰 정수로 쓴다면 INF + 음수 < INF 가 되므로 `dist[u] != INF` 검사가 따로 필요하다)
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:  # 한 라운드 동안 아무것도 안 바뀌면 이미 확정이다 (조기 종료)
            return dist, False
    return dist, True


def bellman_ford_with_prev(n: int, edges: list[Edge], start: int) -> tuple[list[float], list[int], bool]:
    """bellman_ford 와 같지만 각 정점 바로 앞 정점(prev)도 돌려준다. 음수 사이클이 없을 때만 restore_path 에 쓸 수 있다."""
    dist = [INF] * n
    prev = [-1] * n
    dist[start] = 0
    for _ in range(n):
        changed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                changed = True
        if not changed:
            return dist, prev, False
    return dist, prev, True


def restore_path(prev: list[int], start: int, target: int) -> list[int]:
    """prev 를 거슬러 start → target 경로를 만든다. 도달할 수 없으면 빈 리스트."""
    if target != start and prev[target] == -1:
        return []
    path = [target]
    while path[-1] != start:
        path.append(prev[path[-1]])
    return path[::-1]


def find_negative_cycle(n: int, edges: list[Edge]) -> list[int] | None:
    """그래프 어디에든 음수 사이클이 있으면 그 사이클의 정점들을 (사이클 순서대로) 반환하고, 없으면 None.

    모든 정점의 거리를 0 으로 시작하는 것은 "모든 정점으로 가는 가상의 시작점"을 두는 것과 같아서,
    시작점에서 닿지 않는 사이클도 찾는다. n 번째 라운드에도 갱신된 정점은 음수 사이클 위에 있거나 그 사이클에서 닿는 곳이므로,
    prev 를 n 번 거슬러 올라가면 사이클 안에 들어간다."""
    dist = [0] * n
    prev = [-1] * n
    last = -1
    for _ in range(n):
        last = -1
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                last = v
        if last == -1:
            return None
    x = last
    for _ in range(n):
        x = prev[x]
    cycle = [x]
    v = prev[x]
    while v != x:
        cycle.append(v)
        v = prev[v]
    return cycle[::-1]


def spfa(graph: list[list[tuple[int, int]]], start: int) -> tuple[list[float], bool]:
    """큐를 이용한 벨만-포드의 개선(SPFA). graph[u] = [(v, w), ...]. 거리가 줄어든 정점만 다시 큐에 넣는다.

    평균적으로는 빠르지만 최악의 경우는 벨만-포드와 같은 O(VE) 다.
    경로의 간선 수(length)가 n 이상이 되면 음수 사이클이다."""
    n = len(graph)
    dist = [INF] * n
    length = [0] * n
    in_queue = [False] * n
    dist[start] = 0
    queue = deque([start])
    in_queue[start] = True
    while queue:
        u = queue.popleft()
        in_queue[u] = False
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                length[v] = length[u] + 1
                if length[v] >= n:
                    return dist, True
                if not in_queue[v]:
                    in_queue[v] = True
                    queue.append(v)
    return dist, False


def main() -> None:
    input = sys.stdin.readline
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        a, b, c = map(int, input().split())
        edges.append((a - 1, b - 1, c))
    dist, negative_cycle = bellman_ford(n, edges, 0)
    if negative_cycle:
        print(-1)
    else:
        print("\n".join(str(d) if d != INF else "-1" for d in dist[1:]))


if __name__ == "__main__":
    main()
