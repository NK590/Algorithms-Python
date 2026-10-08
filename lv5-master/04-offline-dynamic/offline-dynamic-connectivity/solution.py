"""오프라인 동적 연결성(Offline Dynamic Connectivity) — 간선이 추가·삭제되는 그래프에서 연결성을 묻는 질의에, 모든 연산을 미리 알고 있다는 점을 이용해 답하기, O((T + E) log T · log n)

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 삭제를 지원하는 유니온-파인드는 어렵지만 "되돌리기(rollback)" 는 쉽다 (경로 압축 없이 크기로 합치면 한 번의 합치기는 기록 하나로 되돌릴 수 있다).
  그래서 연산을 시간 순서대로 풀지 않고 거꾸로 생각한다: 간선 하나는 [추가된 시각, 삭제된 시각) 이라는 *시간 구간* 동안만 살아 있다.
- 시간 축 [0, T) 위에 구간 트리를 만들고, 간선의 시간 구간을 O(log T) 개의 노드에 나누어 저장한다.
  루트에서 DFS 하며 노드에 들어갈 때 그 노드의 간선을 모두 합치고, 잎(= 한 시각) 에서 질의에 답하고, 노드를 나갈 때 합친 것을 되돌린다.
  어떤 시각에 살아 있는 간선은 그 시각의 잎까지 가는 경로 위 노드에 정확히 한 번씩 들어 있다.
- 유니온-파인드는 부모와의 홀짝(색) 도 함께 들고 있어서 "이분 그래프인가" 도 같이 답할 수 있다 (홀수 사이클을 만드는 간선이 있으면 이분 그래프가 아님).
- offline_dynamic_graph(n, operations): operations 의 항목은
    ("add", u, v)       간선 추가 (같은 간선을 여러 번 추가하면 다중 간선으로 센다)
    ("remove", u, v)    간선 하나 삭제 (없으면 ValueError)
    ("connected", u, v) u, v 가 지금 연결되어 있는가 → bool
    ("components",)     지금 연결 성분의 수 → int
    ("bipartite",)      지금 그래프가 이분 그래프인가 → bool
  질의 항목마다 하나씩, 순서대로 답을 모은 리스트를 돌려준다.
- 직접 실행하면 BOJ 16911 형식 — `N M`, 이어서 M 줄의 `1 u v`(추가) / `2 u v`(삭제) / `3 u v`(연결 질의) — 을 받아 질의마다 0 또는 1 을 출력합니다.
"""
import sys
from typing import Sequence


class RollbackDSU:
    """경로 압축 없이 크기로 합치는 유니온-파인드. 각 정점은 부모에 대한 홀짝(0/1)을 가진다."""

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
        self.parity = [0] * n  # 자기 색 ≠ 부모 색 이면 1
        self.components = n
        self.odd_cycles = 0  # 홀수 사이클을 만든 간선의 수 (0 이면 이분 그래프)
        self._history: list[tuple[int, int, int]] = []  # (붙은 쪽 뿌리, 큰 쪽 뿌리, 홀수 사이클 증가분); 홀수 사이클 간선은 (-1, -1, 1)

    def find(self, v: int) -> tuple[int, int]:
        """(뿌리, v 의 색을 뿌리의 색과 비교한 홀짝)."""
        color = 0
        while self.parent[v] != v:
            color ^= self.parity[v]
            v = self.parent[v]
        return v, color

    def union(self, a: int, b: int) -> bool:
        """a, b 를 서로 다른 색으로 이어 붙인다. 새로 합쳐졌으면 True."""
        ra, ca = self.find(a)
        rb, cb = self.find(b)
        if ra == rb:
            if ca == cb:  # 같은 색인 두 정점을 잇는 간선: 홀수 사이클
                self.odd_cycles += 1
                self._history.append((-1, -1, 1))
            else:
                self._history.append((-1, -1, 0))
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra  # ca ^ cb 는 대칭이라 색은 바꿀 필요가 없다
        self.parent[rb] = ra
        self.parity[rb] = ca ^ cb ^ 1  # a 와 b 의 색이 달라지도록
        self.size[ra] += self.size[rb]
        self.components -= 1
        self._history.append((rb, ra, 0))
        return True

    def snapshot(self) -> int:
        return len(self._history)

    def rollback(self, snapshot: int) -> None:
        while len(self._history) > snapshot:
            child, root, odd = self._history.pop()
            if child == -1:
                self.odd_cycles -= odd
                continue
            self.parent[child] = child
            self.size[root] -= self.size[child]
            self.components += 1


def _normalize(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u <= v else (v, u)


def offline_dynamic_graph(n: int, operations: Sequence[Sequence]) -> list:
    """정점 0..n-1 에서 operations 를 차례로 실행하며 질의 항목마다 답을 모은다."""
    total = len(operations)
    for op in operations:
        if op[0] in ("add", "remove", "connected") and not (0 <= op[1] < n and 0 <= op[2] < n):
            raise ValueError("정점 번호가 범위를 벗어났습니다")
    # 간선마다 [시작, 끝) 시간 구간 (연산 번호). add 는 자기 다음 시각부터, remove 는 자기 시각 직전까지.
    tree: list[list[tuple[int, int]]] = [[] for _ in range(4 * max(total, 1))]

    def insert(node: int, lo: int, hi: int, left: int, right: int, edge: tuple[int, int]) -> None:
        if right <= lo or hi <= left:
            return
        if left <= lo and hi <= right:
            tree[node].append(edge)
            return
        mid = (lo + hi) // 2
        insert(2 * node, lo, mid, left, right, edge)
        insert(2 * node + 1, mid, hi, left, right, edge)

    alive: dict[tuple[int, int], list[int]] = {}
    for time, op in enumerate(operations):
        if op[0] == "add":
            alive.setdefault(_normalize(op[1], op[2]), []).append(time + 1)
        elif op[0] == "remove":
            edge = _normalize(op[1], op[2])
            starts = alive.get(edge)
            if not starts:
                raise ValueError(f"그런 간선이 없습니다: {edge}")
            insert(1, 0, total, starts.pop(), time, edge)  # 가장 최근에 추가된 것부터 삭제 (연결성에는 차이가 없다)
    for edge, starts in alive.items():
        for start in starts:
            insert(1, 0, total, start, total, edge)

    answers: list = []
    dsu = RollbackDSU(n)

    def visit(node: int, lo: int, hi: int) -> None:
        snapshot = dsu.snapshot()
        for a, b in tree[node]:
            dsu.union(a, b)
        if hi - lo == 1:
            op = operations[lo]
            if op[0] == "connected":
                answers.append(dsu.find(op[1])[0] == dsu.find(op[2])[0])
            elif op[0] == "components":
                answers.append(dsu.components)
            elif op[0] == "bipartite":
                answers.append(dsu.odd_cycles == 0)
        else:
            mid = (lo + hi) // 2
            visit(2 * node, lo, mid)
            visit(2 * node + 1, mid, hi)
        dsu.rollback(snapshot)

    if total:
        visit(1, 0, total)
    return answers


def main() -> None:
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    operations = []
    for i in range(m):
        kind, u, v = int(data[2 + 3 * i]), int(data[3 + 3 * i]) - 1, int(data[4 + 3 * i]) - 1
        operations.append((("add", "remove", "connected")[kind - 1], u, v))
    print("\n".join("1" if x else "0" for x in offline_dynamic_graph(n, operations)))


if __name__ == "__main__":
    main()
