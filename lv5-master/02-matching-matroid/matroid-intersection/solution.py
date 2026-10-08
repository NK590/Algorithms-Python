"""매트로이드 교집합(Matroid Intersection) — 두 매트로이드에서 동시에 독립인 부분집합 중 가장 큰 것 (가중치 판은 가장 무거운 것)

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 매트로이드는 "독립 집합" 의 족: 공집합이 독립, 부분집합도 독립, 크기가 작은 독립 집합 I 와 큰 J 사이에는 J 에서 x 를 더해 I + x 도 독립이 되는 x 가 있다 (교환 성질).
  이 구현은 매트로이드를 독립성 오라클 independent(items) 로만 다룬다.
- 현재 공통 독립 집합 I 에 대해 교환 그래프를 만든다 (원소가 정점).
  y ∈ I, x ∉ I 일 때 I - y + x 가 M1 에서 독립이면 간선 y → x, M2 에서 독립이면 간선 x → y.
  출발점 X1 = {x ∉ I : I + x 가 M1 에서 독립}, 도착점 X2 = {x ∉ I : I + x 가 M2 에서 독립}.
  X1 에서 X2 로 가는 가장 짧은 경로(정점 수가 최소) 의 원소를 I 와의 대칭차로 뒤집으면 크기가 1 커진 공통 독립 집합이 된다. 경로가 없으면 I 가 최대.
- 가중치 판은 정점에 무게(x ∉ I 는 -w[x], y ∈ I 는 +w[y]) 를 주고 (무게 합, 정점 수) 가 사전순으로 가장 작은 경로를 벨만-포드로 찾는다.
  I 가 "크기 |I| 의 공통 독립 집합 중 최대 가중치" 이면 음수 사이클이 없고, 뒤집은 결과도 크기 |I| + 1 중 최대 가중치다.
- matroid_intersection(n, m1, m2): 최대 크기 공통 독립 집합 (정렬된 리스트).
- weighted_matroid_intersection(n, m1, m2, weight): 크기 k = 0, 1, ... 마다의 (최대 가중치, 집합) 목록.
- 매트로이드: UniformMatroid, PartitionMatroid, GraphicMatroid, LinearMatroid (GF(2) 위의 벡터를 비트마스크로).
- 직접 실행하면 "무지개 신장 포레스트" 형식 — `N M`, 이어서 M 줄의 `a b color` — 를 받아 서로 다른 색의 간선만 쓰는 가장 큰 포레스트(간선 번호 0 부터)를 출력합니다.
"""
import sys
from collections import deque
from typing import Optional, Sequence


class Matroid:
    """독립성 오라클만 구현하면 되는 매트로이드의 인터페이스."""

    def independent(self, items: Sequence[int]) -> bool:
        raise NotImplementedError

    def exchangeable(self, current: Sequence[int], x: int) -> list[int]:
        """current (독립 집합) 에서 y 를 빼고 x 를 넣어도 독립인 y 의 목록. current + x 가 독립이면 current 전체.

        기본 구현은 오라클을 |current| 번 부르며, 하위 클래스가 구조를 이용해 더 빨리 돌려줄 수 있다.
        """
        rest = list(current)
        result = []
        for index, y in enumerate(current):
            trial = rest[:index] + rest[index + 1:] + [x]
            if self.independent(trial):
                result.append(y)
        return result


class UniformMatroid(Matroid):
    """크기가 k 이하인 집합이 모두 독립."""

    def __init__(self, k: int):
        self.k = k

    def independent(self, items: Sequence[int]) -> bool:
        return len(items) <= self.k

    def exchangeable(self, current: Sequence[int], x: int) -> list[int]:
        return list(current)  # 크기가 k 미만이면 x 를 그냥 넣을 수 있고, k 이면 아무 y 와 바꿔도 크기 k


class PartitionMatroid(Matroid):
    """원소를 그룹으로 나누고 그룹 g 에서 capacity[g] 개 이하만 고를 수 있다. group_of[e] = 원소 e 의 그룹."""

    def __init__(self, group_of: Sequence[int], capacity):
        self.group_of = list(group_of)
        groups = max(self.group_of, default=-1) + 1
        self.capacity = [capacity] * groups if isinstance(capacity, int) else list(capacity)

    def independent(self, items: Sequence[int]) -> bool:
        used: dict[int, int] = {}
        for e in items:
            g = self.group_of[e]
            used[g] = used.get(g, 0) + 1
            if used[g] > self.capacity[g]:
                return False
        return True

    def exchangeable(self, current: Sequence[int], x: int) -> list[int]:
        g = self.group_of[x]
        inside = [y for y in current if self.group_of[y] == g]
        if len(inside) < self.capacity[g]:
            return list(current)
        return inside


class GraphicMatroid(Matroid):
    """간선 집합이 사이클을 만들지 않으면 독립 (포레스트). edges[e] = (a, b)."""

    def __init__(self, n: int, edges: Sequence[Sequence[int]]):
        self.n = n
        self.edges = [tuple(e) for e in edges]

    def _find(self, parent: list[int], v: int) -> int:
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    def independent(self, items: Sequence[int]) -> bool:
        parent = list(range(self.n))
        for e in items:
            a, b = self.edges[e]
            ra, rb = self._find(parent, a), self._find(parent, b)
            if ra == rb:
                return False
            parent[ra] = rb
        return True

    def exchangeable(self, current: Sequence[int], x: int) -> list[int]:
        a, b = self.edges[x]
        adjacency: dict[int, list[tuple[int, int]]] = {}
        for e in current:
            u, v = self.edges[e]
            adjacency.setdefault(u, []).append((v, e))
            adjacency.setdefault(v, []).append((u, e))
        # a 에서 b 로 가는 포레스트 경로가 있으면 그 경로의 간선만 뺄 수 있다
        came: dict[int, Optional[tuple[int, int]]] = {a: None}
        queue = deque([a])
        while queue and b not in came:
            v = queue.popleft()
            for to, e in adjacency.get(v, []):
                if to not in came:
                    came[to] = (v, e)
                    queue.append(to)
        if b not in came:
            return list(current)  # x 가 두 트리를 잇는다: 아무 것도 빼지 않아도 독립
        path = []
        v = b
        while came[v] is not None:
            v, e = came[v]
            path.append(e)
        return path


class LinearMatroid(Matroid):
    """GF(2) 위의 벡터 (비트마스크 정수) 들이 일차 독립이면 독립. vectors[e] = 원소 e 의 벡터."""

    def __init__(self, vectors: Sequence[int]):
        self.vectors = list(vectors)

    def independent(self, items: Sequence[int]) -> bool:
        basis: dict[int, int] = {}  # 최상위 비트 -> 기저 벡터
        for e in items:
            v = self.vectors[e]
            while v:
                top = v.bit_length() - 1
                if top not in basis:
                    basis[top] = v
                    break
                v ^= basis[top]
            else:
                return False  # 0 벡터가 되었다: 일차 종속
        return True


def _exchange_graph(n: int, m1: Matroid, m2: Matroid, in_set: list[bool]):
    current = [e for e in range(n) if in_set[e]]
    outside = [e for e in range(n) if not in_set[e]]
    out_arcs: list[list[int]] = [[] for _ in range(n)]  # y -> x (M1), x -> y (M2)
    sources, sinks = [], []
    for x in outside:
        if m1.independent(current + [x]):
            sources.append(x)
        if m2.independent(current + [x]):
            sinks.append(x)
        for y in m1.exchangeable(current, x):
            out_arcs[y].append(x)
        for y in m2.exchangeable(current, x):
            out_arcs[x].append(y)
    return out_arcs, sources, sinks


def _flip(in_set: list[bool], path: list[int]) -> None:
    for v in path:
        in_set[v] = not in_set[v]


def _trace(previous: list[int], end: int) -> list[int]:
    path = []
    v = end
    while v != -1:
        path.append(v)
        v = previous[v]
    return path[::-1]


def _shortest_path(n: int, m1: Matroid, m2: Matroid, in_set: list[bool]) -> Optional[list[int]]:
    """교환 그래프에서 출발점(X1)에서 도착점(X2)으로 가는 정점 수가 최소인 경로 (BFS). 없으면 None."""
    out_arcs, sources, sinks = _exchange_graph(n, m1, m2, in_set)
    sink_set = set(sinks)
    previous = [-2] * n  # -2 = 아직 못 감, -1 = 출발점
    queue = deque(sources)
    for s in sources:
        previous[s] = -1
    while queue:
        v = queue.popleft()
        if v in sink_set:
            return _trace(previous, v)
        for to in out_arcs[v]:
            if previous[to] == -2:
                previous[to] = v
                queue.append(to)
    return None


def _lightest_path(n: int, m1: Matroid, m2: Matroid, weight: Sequence[float], in_set: list[bool]) -> Optional[list[int]]:
    """정점 값(넣을 원소는 -w, 뺄 원소는 +w) 의 합이 가장 작고, 같으면 정점 수가 가장 적은 경로 (벨만-포드). 없으면 None."""
    out_arcs, sources, sinks = _exchange_graph(n, m1, m2, in_set)
    cost = [(-weight[v] if not in_set[v] else weight[v]) for v in range(n)]
    best: list[Optional[tuple[float, int]]] = [None] * n  # (무게 합, 정점 수)
    previous = [-1] * n
    for s in sources:
        best[s] = (cost[s], 1)
    for _ in range(n):  # 음수 사이클이 없으므로 최대 n 번이면 수렴
        changed = False
        for v in range(n):
            if best[v] is None:
                continue
            for to in out_arcs[v]:
                candidate = (best[v][0] + cost[to], best[v][1] + 1)
                if best[to] is None or candidate < best[to]:
                    best[to] = candidate
                    previous[to] = v
                    changed = True
        if not changed:
            break
    reachable = [x for x in sinks if best[x] is not None]
    if not reachable:
        return None
    return _trace(previous, min(reachable, key=lambda x: best[x]))


def matroid_intersection(n: int, m1: Matroid, m2: Matroid, initial: Sequence[int] = ()) -> list[int]:
    """원소 0..n-1 에서 M1, M2 양쪽에서 독립인 최대 크기 집합 (정렬된 리스트).

    initial 은 시작할 공통 독립 집합 (기본 빈 집합).
    """
    in_set = [False] * n
    for e in initial:
        in_set[e] = True
    start = [e for e in range(n) if in_set[e]]
    if not (m1.independent(start) and m2.independent(start)):
        raise ValueError("initial 이 공통 독립 집합이 아닙니다")
    while True:
        path = _shortest_path(n, m1, m2, in_set)
        if path is None:
            return [e for e in range(n) if in_set[e]]
        _flip(in_set, path)


def weighted_matroid_intersection(n: int, m1: Matroid, m2: Matroid, weight: Sequence[float]) -> list[tuple[float, list[int]]]:
    """크기 k 마다 가중치 합이 최대인 공통 독립 집합. 결과의 k 번째 항은 (최대 가중치, 정렬된 집합).

    크기 k 의 공통 독립 집합이 없으면 거기서 끝난다 (목록의 길이 = 최대 공통 독립 집합의 크기 + 1).
    """
    in_set = [False] * n
    results: list[tuple[float, list[int]]] = [(0, [])]
    while True:
        path = _lightest_path(n, m1, m2, weight, in_set)
        if path is None:
            return results
        _flip(in_set, path)
        chosen = [e for e in range(n) if in_set[e]]
        results.append((sum(weight[e] for e in chosen), chosen))


def main() -> None:
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    edges, colors = [], []
    for i in range(m):
        a, b, c = (int(data[2 + 3 * i + j]) for j in range(3))
        edges.append((a, b))
        colors.append(c)
    # 색 번호를 0.. 로 압축
    color_id = {c: i for i, c in enumerate(sorted(set(colors)))}
    chosen = matroid_intersection(m, GraphicMatroid(n, edges), PartitionMatroid([color_id[c] for c in colors], 1))
    print(len(chosen))
    print(" ".join(map(str, chosen)))


if __name__ == "__main__":
    main()
