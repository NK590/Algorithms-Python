"""최소 비용 최대 유량(Min-Cost Max-Flow, MCMF) — 가장 싼 증가 경로를 하나씩 찾아 흘리는 연속 최단 경로(SSP) 알고리즘

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 잔여 그래프: 간선 e 마다 역간선 e ^ 1 (용량 0, 비용 -cost) 을 함께 두고, 유량을 흘리면 용량이 줄고 역간선 용량이 는다 (Dinic 과 같은 저장 방식).
- 연속 최단 경로: "비용이 가장 작은 증가 경로" 를 반복해서 흘린다. 항상 가장 싼 경로를 고르면 지금까지 흘린 f 만큼의 유량이 그 f 에서의 최소 비용 유량이 된다 (최적성은 잔여 그래프에 음의 사이클이 없다는 것과 동치).
  그래서 flow 를 f 로 제한하면 "정확히 f 만큼 보내는 최소 비용", 제한이 없으면 "최대 유량 중 최소 비용" 이다.
- 두 가지 최단 경로 구현: ① SPFA(큐 기반 벨만-포드, 음수 비용 간선 가능) ② 다익스트라 + 퍼텐셜(존슨): 처음에만 벨만-포드로 퍼텐셜을 구하고, 이후엔 줄인 비용 cost + h[u] - h[v] ≥ 0 으로 다익스트라.
  경로 비용이 단조 증가하므로 flow_curve() 는 "유량 → 최소 비용" 이 아래로 볼록한 조각 직선(볼록 함수)임을 보여 준다.
- 음의 사이클이 처음부터 있으면 ValueError. 정점은 0 부터 n-1.
- assignment_by_flow(cost): 왼쪽 n 명을 오른쪽 m 개(n ≤ m)에 하나씩 배정하는 최소 비용 (헝가리안 알고리즘과 같은 문제를 흐름으로).
- 직접 실행하면 비용 배정 예제 형식 — `N M`, 이어서 직원마다 `k` 와 k 개의 `(일 번호, 월급)` — 을 받아 최대로 할 수 있는 일의 수와 그때 월급의 최소 합을 출력합니다.
"""
import heapq
import sys
from collections import deque
from typing import Optional, Sequence

INF = float("inf")


class MinCostFlow:
    def __init__(self, n: int):
        self.n = n
        self.to: list[int] = []
        self.capacity: list[int] = []
        self.original: list[int] = []
        self.cost: list[int] = []
        self.adjacency: list[list[int]] = [[] for _ in range(n)]
        self.augmentations: list[tuple[int, int]] = []  # (경로의 단위당 비용, 그 경로로 보낸 양): flow() 가 마지막으로 한 일
        self.potential: list[float] = [0] * n  # 다익스트라용 퍼텐셜: 닿을 수 있는 정점에서는 모든 잔여 간선의 줄인 비용 cost + h[u] - h[v] 가 0 이상

    def add_edge(self, u: int, v: int, capacity: int, cost: int) -> int:
        """u -> v (용량 capacity, 단위당 비용 cost). 간선 번호를 돌려준다 (역간선은 번호 ^ 1)."""
        if not (0 <= u < self.n and 0 <= v < self.n):
            raise IndexError("정점 번호가 범위를 벗어났습니다")
        if capacity < 0:
            raise ValueError("용량은 음수가 될 수 없습니다")
        edge_id = len(self.to)
        for a, b, cap, c in ((u, v, capacity, cost), (v, u, 0, -cost)):
            self.to.append(b)
            self.capacity.append(cap)
            self.original.append(cap)
            self.cost.append(c)
            self.adjacency[a].append(len(self.to) - 1)
        return edge_id

    def flow_on(self, edge_id: int) -> int:
        """간선 edge_id 로 흐른 양."""
        return self.original[edge_id] - self.capacity[edge_id]

    def _bellman_ford(self, source: int) -> list[float]:
        dist = [INF] * self.n
        dist[source] = 0
        for _ in range(self.n):
            changed = False
            for u in range(self.n):
                if dist[u] == INF:
                    continue
                for e in self.adjacency[u]:
                    if self.capacity[e] > 0 and dist[u] + self.cost[e] < dist[self.to[e]]:
                        dist[self.to[e]] = dist[u] + self.cost[e]
                        changed = True
            if not changed:
                return dist
        raise ValueError("음의 사이클이 있습니다")

    def _shortest_spfa(self, source: int, sink: int) -> Optional[tuple[list[float], list[int]]]:
        dist = [INF] * self.n
        parent_edge = [-1] * self.n
        in_queue = [False] * self.n
        dist[source] = 0
        queue = deque([source])
        while queue:
            u = queue.popleft()
            in_queue[u] = False
            for e in self.adjacency[u]:
                v = self.to[e]
                if self.capacity[e] > 0 and dist[u] + self.cost[e] < dist[v]:
                    dist[v] = dist[u] + self.cost[e]
                    parent_edge[v] = e
                    if not in_queue[v]:
                        in_queue[v] = True
                        queue.append(v)
        return (dist, parent_edge) if dist[sink] < INF else None

    def _shortest_dijkstra(self, source: int, sink: int, potential: list[float]) -> Optional[tuple[list[float], list[int]]]:
        dist = [INF] * self.n
        parent_edge = [-1] * self.n
        dist[source] = 0
        heap = [(0, source)]
        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            for e in self.adjacency[u]:
                v = self.to[e]
                if self.capacity[e] > 0:
                    nd = d + self.cost[e] + potential[u] - potential[v]  # 줄인 비용은 0 이상
                    if nd < dist[v]:
                        dist[v] = nd
                        parent_edge[v] = e
                        heapq.heappush(heap, (nd, v))
        if dist[sink] == INF:
            return None
        for v in range(self.n):  # 닿은 정점의 퍼텐셜을 갱신 (닿지 못한 정점은 앞으로도 닿지 못한다)
            if dist[v] < INF:
                potential[v] += dist[v]
        return dist, parent_edge

    def flow(self, source: int, sink: int, limit: float = INF, algorithm: str = "dijkstra") -> tuple[int, int]:
        """source 에서 sink 로 최대 limit 만큼 보내는 최소 비용 유량. (보낸 양, 총 비용) 을 돌려준다."""
        if source == sink:
            raise ValueError("source 와 sink 가 같습니다")
        if algorithm not in ("dijkstra", "spfa"):
            raise ValueError("algorithm 은 'dijkstra' 또는 'spfa'")
        # 음수 비용 간선이 있어도 음의 사이클만 없으면 된다. 벨만-포드가 사이클을 걸러 내고(SPFA 는 사이클이 있으면 영원히 돈다) 다익스트라의 시작 퍼텐셜도 준다
        potential = [0 if d == INF else d for d in self._bellman_ford(source)]
        self.potential = potential
        self.augmentations = []
        total_flow = total_cost = 0
        while total_flow < limit:
            if algorithm == "dijkstra":
                found = self._shortest_dijkstra(source, sink, potential)
            else:
                found = self._shortest_spfa(source, sink)
            if found is None:
                break
            _, parent_edge = found
            push = limit - total_flow
            v = sink
            while v != source:  # 경로의 병목 용량
                e = parent_edge[v]
                push = min(push, self.capacity[e])
                v = self.to[e ^ 1]
            path_cost = 0
            v = sink
            while v != source:
                e = parent_edge[v]
                self.capacity[e] -= push
                self.capacity[e ^ 1] += push
                path_cost += self.cost[e]
                v = self.to[e ^ 1]
            total_flow += push
            total_cost += push * path_cost
            self.augmentations.append((path_cost, push))
        return int(total_flow), int(total_cost)

    def flow_curve(self) -> list[tuple[int, int]]:
        """마지막 flow() 호출에서 증가 경로를 쓸 때마다의 (누적 유량, 누적 최소 비용). 이 점들을 이은 선분의 기울기(경로 비용)는 늘기만 한다 (볼록)."""
        points = [(0, 0)]
        for path_cost, amount in self.augmentations:
            points.append((points[-1][0] + amount, points[-1][1] + amount * path_cost))
        return points


def assignment_by_flow(cost: Sequence[Sequence[int]]) -> tuple[int, list[int]]:
    """n × m (n ≤ m) 비용 행렬에서 행마다 서로 다른 열을 하나씩 골라 비용의 합을 최소로. (최소 합, 행 i 에 배정된 열) 을 돌려준다."""
    n = len(cost)
    m = len(cost[0]) if n else 0
    if n > m:
        raise ValueError("행 수가 열 수보다 클 수 없습니다")
    source, sink = n + m, n + m + 1
    network = MinCostFlow(n + m + 2)
    edges = []
    for i in range(n):
        network.add_edge(source, i, 1, 0)
        edges.append([network.add_edge(i, n + j, 1, cost[i][j]) for j in range(m)])
    for j in range(m):
        network.add_edge(n + j, sink, 1, 0)
    _, total = network.flow(source, sink)
    assignment = [next(j for j in range(m) if network.flow_on(edges[i][j]) == 1) for i in range(n)]
    return total, assignment


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    source, sink = n + m, n + m + 1
    network = MinCostFlow(n + m + 2)
    pos = 2
    for worker in range(n):
        network.add_edge(source, worker, 1, 0)
        k = int(data[pos])
        pos += 1
        for _ in range(k):
            task, salary = int(data[pos]) - 1, int(data[pos + 1])
            pos += 2
            network.add_edge(worker, n + task, 1, salary)
    for task in range(m):
        network.add_edge(n + task, sink, 1, 0)
    flow, cost = network.flow(source, sink)
    print(flow)
    print(cost)


if __name__ == "__main__":
    main()
