"""프림 알고리즘 — 한 정점에서 시작해, 지금 만든 트리에서 뻗어 나가는 가장 싼 간선을 하나씩 붙여 최소 신장 트리(MST)를 만들기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 무방향 그래프를 인접 리스트 `graph[u] = [(v, w), ...]` 로 받습니다. (양방향 간선은 양쪽에 모두 넣어야 합니다) 정점 번호는 0 ~ n-1.
- 다익스트라와 거의 같은 모양입니다. 차이는 힙의 키가 "시작점으로부터의 거리" 가 아니라 "트리에 붙는 간선 하나의 가중치" 라는 점입니다.
- 시작 정점이 속한 연결 요소만 만듭니다. 그래프가 연결되어 있지 않으면 정점마다 prim 을 따로 불러야 합니다.
- 직접 실행하면 아래 형식의 입력(최소 스패닝 트리)을 받아 MST 의 가중치 합을 출력합니다. (정점은 1부터)

      V E          정점 수, 간선 수
      A B C        (E 줄) A 와 B 를 잇는 가중치 C 의 간선
"""
import heapq
import sys

Graph = list[list[tuple[int, int]]]


def prim(graph: Graph, start: int = 0) -> tuple[int, list[tuple[int, int, int]]]:
    """(가중치 합, 채택한 간선들 (부모, 자식, 가중치)) 를 반환한다. start 가 속한 연결 요소만 다룬다."""
    visited = [False] * len(graph)
    heap = [(0, start, -1)]  # (트리에 붙는 간선의 가중치, 붙을 정점, 그 간선의 반대쪽 끝)
    total = 0
    chosen = []
    while heap:
        w, u, parent = heapq.heappop(heap)
        if visited[u]:  # 다른 간선으로 이미 트리에 붙은 정점: 낡은 항목
            continue
        visited[u] = True
        total += w
        if parent != -1:
            chosen.append((parent, u, w))
        for v, weight in graph[u]:
            if not visited[v]:
                heapq.heappush(heap, (weight, v, u))
    return total, chosen


def prim_dense(matrix: list[list[float]]) -> float:
    """인접 행렬(matrix[i][j] = 가중치, 간선이 없으면 float("inf")) 로 O(V²) 에 구하는 MST 의 가중치 합.

    간선이 정점 수의 제곱에 가까운 밀집 그래프에서는 힙 없이 배열로 "트리에서 가장 가까운 정점" 을 찾는 편이 낫다.
    연결되어 있지 않으면 시작 정점(0)이 속한 연결 요소의 합."""
    n = len(matrix)
    if n == 0:
        return 0
    inf = float("inf")
    best = [inf] * n  # best[v] = 지금 트리에서 v 까지 닿는 가장 싼 간선
    in_tree = [False] * n
    best[0] = 0
    total = 0
    for _ in range(n):
        u = -1
        for v in range(n):
            if not in_tree[v] and (u == -1 or best[v] < best[u]):
                u = v
        if best[u] == inf:  # 남은 정점에 닿을 간선이 없다 (연결 요소가 끝났다)
            break
        in_tree[u] = True
        total += best[u]
        for v in range(n):
            if not in_tree[v] and matrix[u][v] < best[v]:
                best[v] = matrix[u][v]
    return total


def main() -> None:
    input = sys.stdin.readline
    v, e = map(int, input().split())
    graph: Graph = [[] for _ in range(v)]
    for _ in range(e):
        a, b, c = map(int, input().split())
        graph[a - 1].append((b - 1, c))
        graph[b - 1].append((a - 1, c))
    print(prim(graph)[0])


if __name__ == "__main__":
    main()
