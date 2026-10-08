"""탑 트리(Top Tree) — 정적 탑 트리: 모양이 고정된 트리의 DP 를 점 갱신과 함께 O(log n) 에 (rake / compress 클러스터)

README.md 의 설명과 짝을 이루는 참고 구현입니다. **범위를 먼저 밝힙니다**: 간선이 추가·삭제되는 완전한 동적 탑 트리(Alstrup 등, 자기 조정 탑 트리) 는 구현하지 않았고,
위상(트리 모양)은 고정이고 정점의 값만 바뀌는 "정적 탑 트리" 를 구현했습니다. 이것이 대회에서 "동적 트리 DP" 를 푸는 표준 도구이고, 클러스터·rake·compress 라는 탑 트리의 핵심 개념이 그대로 드러납니다.
(위상이 바뀌면 링크-컷 트리, 정점 값만 바뀌면 이 구조 — 03 의 이전 개념에 연결.)
- 클러스터 두 종류: 경로 클러스터 P (위에서 아래로 내려가는 경로 + 그 경로 위 정점들에 매달린 가벼운 서브트리들) 와 점 클러스터 Q (간선 하나에 매달린 서브트리 요약).
- 연산 네 개를 사용자가 준다: add_vertex(v, q or None) -> P (정점 v 와 가벼운 자식들의 요약 q), compress(upper, lower) -> P (위쪽 경로와 아래쪽 경로 이어 붙이기),
  add_edge(p) -> Q (가벼운 자식의 무거운 경로를 부모에서 본 요약으로), rake(q1, q2) -> Q (같은 정점에 매달린 두 요약 합치기, 교환 가능해야 한다).
- 구성: 서브트리 크기로 무거운 자식을 정해 경로(heavy path) 로 쪼개고, 경로의 정점 클러스터들을 compress 로 (가중치 균형) 이진 트리로 묶고, 가벼운 자식들은 rake 로 묶는다.
  가중치 균형 덕분에 클러스터 트리의 깊이는 전체 O(log n) → 정점 하나를 갱신하면 그 정점의 클러스터에서 루트까지 O(log n) 개만 다시 계산한다.
- 예제 두 개: TreeMaxIndependentSet (정점 가중치 최대 독립 집합, 최대-합 2 × 2 행렬), LinearTreeDP (val(v) = A_v + B_v · Σ val(자식) mod p, 아핀 함수 합성).
- 직접 실행하면 Luogu P4719 "动态 DP" 형식 — `n m`, 정점 가중치, 간선 n-1 개, 질의 `x y`(a_x = y 로 바꾸고) — 마다 최대 가중치 독립 집합의 값을 출력합니다.
"""
import sys
from bisect import bisect_left
from itertools import accumulate
from typing import Any, Callable, Optional, Sequence

NEG = float("-inf")

VERTEX, COMPRESS, ADD_EDGE, RAKE = range(4)


class StaticTopTree:
    def __init__(
        self,
        n: int,
        edges: Sequence[tuple[int, int]],
        add_vertex: Callable[[int, Any], Any],
        compress: Callable[[Any, Any], Any],
        add_edge: Callable[[Any], Any],
        rake: Callable[[Any, Any], Any],
        root: int = 0,
    ):
        if n < 1:
            raise ValueError("정점이 하나 이상 있어야 합니다")
        if len(edges) != n - 1:
            raise ValueError("트리가 아닙니다 (간선이 n - 1 개가 아님)")
        self.n = n
        self._add_vertex, self._compress, self._add_edge, self._rake = add_vertex, compress, add_edge, rake
        adj: list[list[int]] = [[] for _ in range(n)]
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)
        parent = [-1] * n
        order = [root]
        for v in order:  # BFS 순서
            for w in adj[v]:
                if w != parent[v]:
                    if parent[w] != -1 or w == root:
                        raise ValueError("트리가 아닙니다 (사이클)")
                    parent[w] = v
                    order.append(w)
        if len(order) != n:
            raise ValueError("연결된 트리가 아닙니다")
        size = [1] * n
        for v in reversed(order):
            if parent[v] != -1:
                size[parent[v]] += size[v]
        heavy = [-1] * n
        lights: list[list[int]] = [[] for _ in range(n)]
        for v in order:
            children = [w for w in adj[v] if w != parent[v]]
            if children:
                heavy[v] = max(children, key=size.__getitem__)
                lights[v] = [w for w in children if w != heavy[v]]
        # 클러스터 트리 노드 (자식이 항상 부모보다 먼저 만들어진다 = 번호 순서가 계산 순서)
        self.kind: list[int] = []
        self.child_a: list[int] = []  # VERTEX: 가벼운 자식들의 rake 루트(없으면 -1) / COMPRESS, RAKE: 첫째 자식 / ADD_EDGE: 자식
        self.child_b: list[int] = []
        self.node_parent: list[int] = []
        self.value: list[Any] = []
        self.vertex_node = [-1] * n
        self.vertex_of: list[int] = []  # VERTEX 노드의 정점 번호 (아니면 -1)
        self.root_node = self._build_path(root, heavy, lights, size)

    def _new_node(self, kind: int, a: int, b: int, vertex: int = -1) -> int:
        node = len(self.kind)
        self.kind.append(kind)
        self.child_a.append(a)
        self.child_b.append(b)
        self.node_parent.append(-1)
        self.vertex_of.append(vertex)
        for child in ((a, b) if kind in (COMPRESS, RAKE) else (a,)):
            if child != -1:
                self.node_parent[child] = node
        self.value.append(self._compute(node, kind, a, b, vertex))
        return node

    def _compute(self, node: int, kind: int, a: int, b: int, vertex: int) -> Any:
        if kind == VERTEX:
            return self._add_vertex(vertex, None if a == -1 else self.value[a])
        if kind == COMPRESS:
            return self._compress(self.value[a], self.value[b])
        if kind == ADD_EDGE:
            return self._add_edge(self.value[a])
        return self._rake(self.value[a], self.value[b])

    def _balanced(self, nodes: list[int], weights: list[int], kind: int) -> int:
        """nodes 를 가중치 균형을 맞춰 kind(COMPRESS 또는 RAKE) 노드들의 이진 트리로 묶는다 (순서 유지)."""
        prefix = [0] + list(accumulate(weights))

        def build(lo: int, hi: int) -> int:
            if hi - lo == 1:
                return nodes[lo]
            half = prefix[lo] + (prefix[hi] - prefix[lo]) / 2
            split = bisect_left(prefix, half, lo + 1, hi)  # 앞쪽 가중치가 전체의 절반 이상이 되는 첫 위치
            split = min(max(split, lo + 1), hi - 1)
            left = build(lo, split)
            right = build(split, hi)
            return self._new_node(kind, left, right)

        return build(0, len(nodes))

    def _build_path(self, top: int, heavy: list[int], lights: list[list[int]], size: list[int]) -> int:
        path = []
        v = top
        while v != -1:
            path.append(v)
            v = heavy[v]
        vertex_nodes, weights = [], []
        for v in path:
            rake_root = -1
            if lights[v]:
                light_nodes = []
                for child in lights[v]:
                    light_nodes.append(self._new_node(ADD_EDGE, self._build_path(child, heavy, lights, size), -1))
                rake_root = self._balanced(light_nodes, [size[c] for c in lights[v]], RAKE)
            node = self._new_node(VERTEX, rake_root, -1, v)
            self.vertex_node[v] = node
            vertex_nodes.append(node)
            weights.append(1 + sum(size[c] for c in lights[v]))
        return self._balanced(vertex_nodes, weights, COMPRESS)

    def update(self, v: int) -> None:
        """정점 v 에 대한 사용자 데이터가 바뀐 뒤 부른다: v 의 클러스터에서 루트까지 다시 계산한다."""
        node = self.vertex_node[v]
        while node != -1:
            self.value[node] = self._compute(node, self.kind[node], self.child_a[node], self.child_b[node], self.vertex_of[node])
            node = self.node_parent[node]

    def root_value(self) -> Any:
        return self.value[self.root_node]

    def depth_of(self, v: int) -> int:
        """v 의 클러스터에서 루트까지의 노드 수 (갱신 한 번의 비용)."""
        node, depth = self.vertex_node[v], 0
        while node != -1:
            depth += 1
            node = self.node_parent[node]
        return depth


class TreeMaxIndependentSet:
    """정점 가중치가 바뀌는 트리의 최대 가중치 독립 집합 (이웃한 두 정점을 함께 고르지 않는다). 가중치는 음수가 있어도 되고 빈 집합이 허용된다."""

    def __init__(self, n: int, edges: Sequence[tuple[int, int]], weights: Sequence[int], root: int = 0):
        self.weights = list(weights)

        def add_vertex(v: int, light: Optional[tuple[int, int]]):
            s0, s1 = light if light is not None else (0, 0)  # s0: 가벼운 자식 각각의 max(안 고름, 고름) 합, s1: 자식들을 안 고를 때의 합
            # [dp0, dp1] (v 의 상태) = M ⊗ [무거운 자식의 dp0, dp1]  (최대-합 행렬)
            return ((s0, s0), (self.weights[v] + s1, NEG))

        def compress(upper, lower):
            return tuple(tuple(max(upper[i][k] + lower[k][j] for k in range(2)) for j in range(2)) for i in range(2))

        def add_edge(path):  # 경로 클러스터를 아래 상태 (0, -inf) 에 적용: (dp0, dp1) = (M[0][0], M[1][0]). 부모가 쓰는 요약은 (max(dp0, dp1), dp0)
            dp0, dp1 = path[0][0], path[1][0]
            return (max(dp0, dp1), dp0)

        def rake(a, b):
            return (a[0] + b[0], a[1] + b[1])

        self.tree = StaticTopTree(n, edges, add_vertex, compress, add_edge, rake, root)

    def set_weight(self, v: int, weight: int) -> None:
        self.weights[v] = weight
        self.tree.update(v)

    def best(self) -> int:
        matrix = self.tree.root_value()
        return max(matrix[0][0], matrix[1][0])  # 아래 상태 (0, -inf) 에 적용한 dp0, dp1 의 최댓값


class LinearTreeDP:
    """val(v) = A_v + B_v · Σ_{c ∈ 자식} val(c)  (mod p) 의 루트 값. A, B 가 점 갱신된다. 잎은 val = A_v."""

    def __init__(self, n: int, edges: Sequence[tuple[int, int]], a: Sequence[int], b: Sequence[int], mod: int, root: int = 0):
        self.a, self.b, self.mod = list(a), list(b), mod

        def add_vertex(v: int, light: Optional[int]):
            s = light if light is not None else 0  # 가벼운 자식들의 val 합
            # val(v) = B_v · x + (A_v + B_v · s)  (x = 무거운 자식의 val): 아핀 함수 (기울기, 절편)
            return (self.b[v] % mod, (self.a[v] + self.b[v] * s) % mod)

        def compress(upper, lower):  # upper(lower(x))
            return (upper[0] * lower[0] % mod, (upper[0] * lower[1] + upper[1]) % mod)

        def add_edge(path):  # 무거운 자식이 없는 맨 아래 정점은 x = 0 이므로 val = 절편
            return path[1]

        def rake(x, y):
            return (x + y) % mod

        self.tree = StaticTopTree(n, edges, add_vertex, compress, add_edge, rake, root)

    def set_values(self, v: int, a: Optional[int] = None, b: Optional[int] = None) -> None:
        if a is not None:
            self.a[v] = a
        if b is not None:
            self.b[v] = b
        self.tree.update(v)

    def root_val(self) -> int:
        return self.tree.root_value()[1]  # 루트 경로의 맨 아래는 x = 0


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    weights = [int(x) for x in data[2 : 2 + n]]
    pos = 2 + n
    edges = [(int(data[pos + 2 * i]) - 1, int(data[pos + 2 * i + 1]) - 1) for i in range(n - 1)]
    pos += 2 * (n - 1)
    solver = TreeMaxIndependentSet(n, edges, weights)
    out = []
    for _ in range(m):
        solver.set_weight(int(data[pos]) - 1, int(data[pos + 1]))
        out.append(solver.best())
        pos += 2
    print("\n".join(map(str, out)))


if __name__ == "__main__":
    main()
