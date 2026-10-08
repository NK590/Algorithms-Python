"""다익스트라 알고리즘 — 한 정점에서 모든 정점까지의 최단 거리 (간선 가중치가 모두 0 이상일 때)

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 그래프는 인접 리스트 `graph[u] = [(v, w), ...]` (u → v, 가중치 w) 로 받고, 정점 번호는 0 ~ n-1 입니다.
- 도달할 수 없는 정점의 거리는 INF 입니다.
- 직접 실행하면 아래 형식의 입력을 표준 입력으로 받아 각 정점까지의 거리를 한 줄씩 출력합니다. (정점 번호는 1부터)

      V E          정점 수, 간선 수
      K            시작 정점
      u v w        (E 줄) u → v 간선, 가중치 w
"""
import heapq
import sys

INF = float("inf")

Graph = list[list[tuple[int, int]]]


def dijkstra(graph: Graph, start: int) -> list[float]:
    """start 에서 각 정점까지의 최단 거리를 반환한다. (가장 기본형)"""
    dist = [INF] * len(graph)
    dist[start] = 0
    heap = [(0, start)]  # (start 로부터의 거리, 정점) — 거리가 앞에 와야 거리순으로 꺼내진다

    while heap:
        d, u = heapq.heappop(heap)
        # 힙에는 갱신 전의 낡은 항목이 남아 있을 수 있다. 이미 더 짧은 거리가 기록됐다면 건너뛴다.
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:  # u 를 거쳐 가는 길이 지금까지 알던 길보다 짧을 때만 갱신
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    return dist


def dijkstra_with_prev(graph: Graph, start: int) -> tuple[list[float], list[int]]:
    """최단 거리와 함께, 각 정점 바로 앞 정점(prev)을 반환한다. 경로 복원이 필요할 때 쓴다.

    dijkstra() 와 같은 코드에 `prev[v] = u` 한 줄만 더해진 것이다.
    """
    dist = [INF] * len(graph)
    prev = [-1] * len(graph)
    dist[start] = 0
    heap = [(0, start)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u  # v 로 가는 최단 경로에서 v 바로 앞 정점은 u
                heapq.heappush(heap, (nd, v))

    return dist, prev


def restore_path(prev: list[int], start: int, target: int) -> list[int] | None:
    """prev 를 target 에서 start 까지 거슬러 올라가 경로를 복원한다. 도달할 수 없으면 None."""
    if target != start and prev[target] == -1:
        return None
    path = [target]
    while path[-1] != start:
        path.append(prev[path[-1]])
    path.reverse()
    return path


def main() -> None:
    input = sys.stdin.readline
    v, e = map(int, input().split())
    start = int(input())
    graph: Graph = [[] for _ in range(v + 1)]  # 정점 번호가 1부터라 0번은 쓰지 않는다
    for _ in range(e):
        a, b, w = map(int, input().split())
        graph[a].append((b, w))

    dist = dijkstra(graph, start)
    print("\n".join("INF" if d == INF else str(d) for d in dist[1:]))


if __name__ == "__main__":
    main()
