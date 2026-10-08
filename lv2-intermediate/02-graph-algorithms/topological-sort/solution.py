"""위상 정렬 — 방향 그래프의 간선 u → v 를 "u 가 v 보다 먼저" 로 읽고 모든 정점을 그 순서에 맞게 한 줄로 세우기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 사이클이 없는 방향 그래프(DAG)에서만 가능하고, 사이클이 있으면 None 입니다. 가능한 순서는 보통 여러 개입니다.
- 간선 목록 `edges = [(u, v), ...]` 와 정점 수 `n` 으로 받고, 정점 번호는 0 ~ n-1 입니다.
- 두 가지 방법: ① 진입 차수가 0 인 정점부터 꺼내는 칸 알고리즘 ② DFS 후위 순서를 뒤집기.
- 직접 실행하면 `N M` 과 M 개의 `A B`(A 가 B 앞) 를 받아 가능한 순서 하나를 출력합니다. (정점은 1부터)
"""
import heapq
import sys
from collections import deque

Edges = list[tuple[int, int]]


def _build(n: int, edges: Edges) -> tuple[list[list[int]], list[int]]:
    graph = [[] for _ in range(n)]
    indegree = [0] * n
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1
    return graph, indegree


def topological_sort(n: int, edges: Edges) -> list[int] | None:
    """칸 알고리즘(Kahn). 진입 차수가 0 인 정점을 꺼내 순서에 넣고, 그 정점에서 나가는 간선을 지운다.

    모든 정점을 꺼내지 못했다면 남은 정점은 사이클 위에(또는 사이클 뒤에) 있다."""
    graph, indegree = _build(n, edges)
    queue = deque(v for v in range(n) if indegree[v] == 0)
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    return order if len(order) == n else None


def topological_sort_dfs(n: int, edges: Edges) -> list[int] | None:
    """DFS 후위 순서를 뒤집는다. 정점의 모든 후손이 끝난 뒤에야 그 정점이 후위 순서에 들어가기 때문이다.

    색: 0 = 아직, 1 = 탐색 중(스택 위), 2 = 끝. 탐색 중인 정점을 다시 만나면 사이클이다. 재귀 한도를 피하려고 반복문으로 쓴다."""
    graph, _ = _build(n, edges)
    color = [0] * n
    post = []
    for s in range(n):
        if color[s]:
            continue
        color[s] = 1
        stack = [(s, 0)]  # (정점, 다음에 볼 이웃의 위치)
        while stack:
            u, i = stack.pop()
            if i < len(graph[u]):
                stack.append((u, i + 1))
                v = graph[u][i]
                if color[v] == 1:
                    return None
                if color[v] == 0:
                    color[v] = 1
                    stack.append((v, 0))
            else:
                color[u] = 2
                post.append(u)
    return post[::-1]


def has_cycle(n: int, edges: Edges) -> bool:
    return topological_sort(n, edges) is None


def smallest_topological_order(n: int, edges: Edges) -> list[int] | None:
    """가능한 순서 중 사전순으로 가장 앞선 것. 큐 대신 최소 힙을 써서 항상 번호가 가장 작은 정점을 먼저 꺼낸다."""
    graph, indegree = _build(n, edges)
    heap = [v for v in range(n) if indegree[v] == 0]
    heapq.heapify(heap)
    order = []
    while heap:
        u = heapq.heappop(heap)
        order.append(u)
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                heapq.heappush(heap, v)
    return order if len(order) == n else None


def earliest_finish_times(durations: list[int], edges: Edges) -> list[int] | None:
    """각 작업이 걸리는 시간 `durations` 와 선행 관계 `edges`(u → v: u 가 끝나야 v 시작) 가 있을 때 작업마다 가장 빨리 끝나는 시각.

    위상 순서로 보면서 finish[v] = durations[v] + max(선행 작업들의 finish). 사이클이면 None."""
    n = len(durations)
    graph, indegree = _build(n, edges)
    order = topological_sort(n, edges)
    if order is None:
        return None
    start = [0] * n
    finish = [0] * n
    for u in order:
        finish[u] = start[u] + durations[u]
        for v in graph[u]:
            start[v] = max(start[v], finish[u])
    return finish


def main() -> None:
    input = sys.stdin.readline
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a - 1, b - 1))
    order = topological_sort(n, edges)
    print(" ".join(str(v + 1) for v in order) if order is not None else "-1")


if __name__ == "__main__":
    main()
