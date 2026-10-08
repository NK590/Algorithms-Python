"""디닉 알고리즘(Dinic) — 네트워크 플로우의 최대 유량을 BFS 레벨 그래프 + 막다른 길을 피하는 DFS 로 구하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 잔여 그래프: 간선마다 되돌리는 역간선을 함께 저장하고 (간선 e 의 역간선은 e ^ 1), 유량을 흘리면 용량이 줄고 역간선 용량이 늘어납니다.
- 한 단계(phase): ① BFS 로 s 에서의 거리(레벨)를 구하고 ② 레벨이 정확히 1 씩 늘어나는 간선만 써서 더 이상 못 보낼 때까지 DFS 로 흘립니다
  (블로킹 플로우). 정점마다 "다음에 볼 간선" 포인터(it)를 두어 막다른 길은 다시 보지 않습니다. 단계는 최대 V 번, 한 단계는 O(VE).
- DFS 도 반복문으로 구현했습니다(재귀 깊이 문제 없음). 경로를 하나 찾아 흘린 뒤 s 부터 다시 시작해도 포인터 덕분에 낭비가 없습니다.
- 정점은 0 부터 n-1. 무방향 간선은 add_edge(u, v, c, c) 처럼 역방향 용량도 c 로 주면 됩니다.
- 직접 실행하면 `N` 과 N 개의 파이프 `u v c` (정점은 알파벳 대문자 A-Z, 소문자 a-z, 파이프는 양방향)를 받아 A 에서 Z 까지의 최대 유량을 출력합니다.
"""
import sys
from collections import deque


class Dinic:
    def __init__(self, n: int):
        self.n = n
        self.to: list[int] = []  # 간선 e 의 도착 정점
        self.capacity: list[int] = []  # 간선 e 의 남은 용량
        self.original: list[int] = []  # 간선 e 의 처음 용량
        self.adjacency: list[list[int]] = [[] for _ in range(n)]  # 정점별 나가는 간선 번호

    def add_edge(self, u: int, v: int, capacity: int, reverse_capacity: int = 0) -> int:
        """u -> v (용량 capacity), 역방향은 reverse_capacity (무방향이면 capacity 와 같게). 간선 번호를 돌려준다 (역간선은 번호 ^ 1)."""
        edge_id = len(self.to)
        self.to.append(v)
        self.capacity.append(capacity)
        self.original.append(capacity)
        self.adjacency[u].append(edge_id)
        self.to.append(u)
        self.capacity.append(reverse_capacity)
        self.original.append(reverse_capacity)
        self.adjacency[v].append(edge_id + 1)
        return edge_id

    def flow_on(self, edge_id: int) -> int:
        """간선 edge_id 방향으로 흐르는 순유량 (처음 용량 - 남은 용량). 무방향 간선에서 반대로 흐르면 음수."""
        return self.original[edge_id] - self.capacity[edge_id]

    def _bfs(self, source: int, sink: int) -> list[int]:
        level = [-1] * self.n
        level[source] = 0
        queue = deque([source])
        while queue:
            v = queue.popleft()
            for e in self.adjacency[v]:
                w = self.to[e]
                if self.capacity[e] > 0 and level[w] < 0:
                    level[w] = level[v] + 1
                    queue.append(w)
        return level

    def max_flow(self, source: int, sink: int) -> int:
        if source == sink:
            raise ValueError("source 와 sink 가 같습니다")
        flow = 0
        while True:
            level = self._bfs(source, sink)
            if level[sink] < 0:
                return flow
            pointer = [0] * self.n  # 정점마다 다음에 볼 간선의 위치
            path: list[int] = []  # source 에서 현재 정점까지의 간선 번호
            v = source
            while True:
                if v == sink:  # 경로를 찾았다: 병목만큼 흘리고 처음부터 다시
                    pushed = min(self.capacity[e] for e in path)
                    for e in path:
                        self.capacity[e] -= pushed
                        self.capacity[e ^ 1] += pushed
                    flow += pushed
                    path.clear()
                    v = source
                    continue
                advanced = False
                while pointer[v] < len(self.adjacency[v]):
                    e = self.adjacency[v][pointer[v]]
                    w = self.to[e]
                    if self.capacity[e] > 0 and level[w] == level[v] + 1:
                        path.append(e)
                        v = w
                        advanced = True
                        break
                    pointer[v] += 1
                if not advanced:  # 막다른 길: 한 칸 물러나고 그 간선은 다시 보지 않는다
                    if v == source:
                        break
                    e = path.pop()
                    v = self.to[e ^ 1]
                    pointer[v] += 1

    def min_cut_source_side(self, source: int) -> list[bool]:
        """max_flow 를 한 뒤, 잔여 그래프에서 source 로부터 도달할 수 있는 정점들(최소 컷의 source 쪽)."""
        reachable = [False] * self.n
        reachable[source] = True
        stack = [source]
        while stack:
            v = stack.pop()
            for e in self.adjacency[v]:
                w = self.to[e]
                if self.capacity[e] > 0 and not reachable[w]:
                    reachable[w] = True
                    stack.append(w)
        return reachable


def _node_id(ch: str) -> int:
    return ord(ch) - 65 if ch.isupper() else ord(ch) - 97 + 26


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    network = Dinic(52)
    for i in range(n):
        u, v, c = _node_id(data[1 + 3 * i]), _node_id(data[2 + 3 * i]), int(data[3 + 3 * i])
        network.add_edge(u, v, c, c)
    print(network.max_flow(_node_id("A"), _node_id("Z")))


if __name__ == "__main__":
    main()
