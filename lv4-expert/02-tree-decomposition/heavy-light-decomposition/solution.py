"""헤비-라이트 분할(Heavy-Light Decomposition, HLD) — 트리 위의 경로·서브트리 질의를 배열 위의 O(log n) 개 구간으로 바꾸기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 각 정점에서 서브트리가 가장 큰 자식으로 가는 간선을 "무거운 간선(heavy)", 나머지를 "가벼운 간선(light)" 이라 하면 루트에서 어떤 정점까지 가벼운 간선은 O(log n) 개 (가벼운 간선을 한 번 지날 때마다 서브트리 크기가 절반 이하로 준다).
  무거운 간선들이 이어진 사슬(chain)을 위에서 아래로 번호를 이어 배열에 펴면, 정점 u 에서 루트까지는 O(log n) 개의 연속 구간이 된다.
- HLD: head[v] (v 가 속한 사슬의 맨 위), pos[v] (배열 위치), 서브트리는 [pos[v], pos[v] + size[v]) 의 연속 구간.
  path_segments(u, v): u-v 경로를 덮는 [l, r) 구간들 (정점 가중치 기준 / edge=True 이면 간선 가중치를 "아래쪽 정점"에 저장했다고 보고 LCA 를 뺀다).
- SegmentTree: 한 점 갱신·구간 합성(합, 최댓값, … 결합 법칙이 성립하는 연산) 의 반복형 구간 트리. PathQuery: HLD + SegmentTree 로 경로 질의·점 갱신.
- PathAddSubtreeSum: 펜윅 트리 두 개로 "경로 전체에 더하기" 와 "서브트리 합 / 경로 합" 을 처리.
- 모든 탐색이 반복문이라 정점이 10^5 개인 사슬에서도 재귀 깊이 문제가 없다.
- 직접 실행하면 트리 경로 최댓값 예제 형식 — 트리(1부터, 간선 가중치), 질의 `1 i c`(i 번째 간선의 가중치를 c 로), `2 u v`(경로의 최대 간선 가중치) — 를 처리해 2 번 질의의 답을 출력합니다.
"""
import sys
from typing import Callable, Optional, Sequence


class HLD:
    def __init__(self, n: int, edges: Sequence[tuple[int, int]], root: int = 0):
        adj: list[list[int]] = [[] for _ in range(n)]
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)
        self.n = n
        self.parent = [-1] * n
        self.depth = [0] * n
        order: list[int] = []  # BFS 순서 (부모가 자식보다 먼저)
        seen = [False] * n
        stack = [root]
        seen[root] = True
        while stack:
            v = stack.pop()
            order.append(v)
            for w in adj[v]:
                if not seen[w]:
                    seen[w] = True
                    self.parent[w] = v
                    self.depth[w] = self.depth[v] + 1
                    stack.append(w)
        if len(order) != n:
            raise ValueError("연결된 트리가 아닙니다")
        self.size = [1] * n
        self.heavy = [-1] * n
        for v in reversed(order):  # 자식들의 크기가 확정된 뒤 부모에 더한다
            p = self.parent[v]
            if p != -1:
                self.size[p] += self.size[v]
        for v in order:
            best = 0
            for w in adj[v]:
                if w != self.parent[v] and self.size[w] > best:
                    best, self.heavy[v] = self.size[w], w
        # 전위 순회로 번호를 매긴다: 무거운 자식을 가장 먼저(스택에 마지막으로 넣어 먼저 꺼낸다) 방문하므로
        # 사슬이 연속하고, 한 정점의 서브트리 전체도 연속한 구간이 된다.
        self.head = [0] * n
        self.pos = [0] * n
        self.order_by_pos = [0] * n  # pos -> 정점
        counter = 0
        self.head[root] = root
        stack = [root]
        while stack:
            v = stack.pop()
            self.pos[v] = counter
            self.order_by_pos[counter] = v
            counter += 1
            for w in adj[v]:
                if w != self.parent[v] and w != self.heavy[v]:
                    self.head[w] = w  # 가벼운 자식은 새 사슬의 머리
                    stack.append(w)
            if self.heavy[v] != -1:
                self.head[self.heavy[v]] = self.head[v]
                stack.append(self.heavy[v])

    def lca(self, u: int, v: int) -> int:
        while self.head[u] != self.head[v]:
            if self.depth[self.head[u]] < self.depth[self.head[v]]:
                u, v = v, u
            u = self.parent[self.head[u]]  # 더 깊은 사슬의 머리 위로 올라간다
        return u if self.depth[u] < self.depth[v] else v

    def distance(self, u: int, v: int) -> int:
        return self.depth[u] + self.depth[v] - 2 * self.depth[self.lca(u, v)]

    def subtree_range(self, v: int) -> tuple[int, int]:
        """v 의 서브트리가 차지하는 반열린 구간 [l, r)."""
        return self.pos[v], self.pos[v] + self.size[v]

    def path_segments(self, u: int, v: int, edge: bool = False) -> list[tuple[int, int]]:
        """u-v 경로를 덮는 위치 구간 [l, r) 의 목록. edge=True 이면 "각 간선 = 아래쪽 정점의 값" 으로 보고 LCA 의 값을 제외한다."""
        segments = []
        while self.head[u] != self.head[v]:
            if self.depth[self.head[u]] < self.depth[self.head[v]]:
                u, v = v, u
            segments.append((self.pos[self.head[u]], self.pos[u] + 1))
            u = self.parent[self.head[u]]
        if self.depth[u] > self.depth[v]:
            u, v = v, u
        # 같은 사슬 안: u 가 위, v 가 아래
        left = self.pos[u] + (1 if edge else 0)
        if left < self.pos[v] + 1:
            segments.append((left, self.pos[v] + 1))
        return segments


class SegmentTree:
    """반복형 구간 트리. combine 은 결합 법칙이 성립해야 하고(교환 법칙은 필요 없다) identity 는 항등원."""

    def __init__(self, values: Sequence, combine: Callable = lambda a, b: a + b, identity=0):
        self.n = len(values)
        self.combine = combine
        self.identity = identity
        size = max(1, self.n)  # 이 방식의 반복형 트리는 n 이 2 의 거듭제곱이 아니어도 된다 (왼쪽·오른쪽 결과를 따로 모으므로 비가환 combine 도 맞다)
        self.size = size
        self.tree = [identity] * (2 * size)
        for i, value in enumerate(values):
            self.tree[size + i] = value
        for i in range(size - 1, 0, -1):
            self.tree[i] = combine(self.tree[2 * i], self.tree[2 * i + 1])

    def set(self, index: int, value) -> None:
        i = index + self.size
        self.tree[i] = value
        i //= 2
        while i:
            self.tree[i] = self.combine(self.tree[2 * i], self.tree[2 * i + 1])
            i //= 2

    def get(self, index: int):
        return self.tree[index + self.size]

    def query(self, left: int, right: int):
        """반열린 [left, right)."""
        result_left = result_right = self.identity
        left += self.size
        right += self.size
        while left < right:
            if left & 1:
                result_left = self.combine(result_left, self.tree[left])
                left += 1
            if right & 1:
                right -= 1
                result_right = self.combine(self.tree[right], result_right)
            left //= 2
            right //= 2
        return self.combine(result_left, result_right)


class PathQuery:
    """HLD + 구간 트리: 정점 값(또는 간선 값) 의 점 갱신과 경로 질의 (경로의 구간들을 u 쪽부터 순서 없이 합치므로 combine 은 교환 법칙도 필요하다). edge=True 면 간선 (parent[v], v) 의 값을 정점 v 에 둔다."""

    def __init__(self, hld: HLD, values: Sequence, combine: Callable = lambda a, b: a + b, identity=0, edge: bool = False):
        self.hld = hld
        self.edge = edge
        self.identity = identity
        self.combine = combine
        ordered = [values[hld.order_by_pos[i]] for i in range(hld.n)]
        self.tree = SegmentTree(ordered, combine, identity)

    def update(self, v: int, value) -> None:
        self.tree.set(self.hld.pos[v], value)

    def value(self, v: int):
        return self.tree.get(self.hld.pos[v])

    def query(self, u: int, v: int):
        result = self.identity
        for left, right in self.hld.path_segments(u, v, self.edge):
            result = self.combine(result, self.tree.query(left, right))
        return result

    def query_subtree(self, v: int):
        left, right = self.hld.subtree_range(v)
        return self.tree.query(left, right)


class _RangeAddRangeSum:
    """펜윅 트리 두 개로 구간 더하기·구간 합 (0 부터, 반열린)."""

    def __init__(self, n: int):
        self.n = n
        self.b1 = [0] * (n + 2)
        self.b2 = [0] * (n + 2)

    def _add(self, tree: list[int], i: int, value: int) -> None:
        i += 1
        while i <= self.n + 1:
            tree[i] += value
            i += i & -i

    def _prefix(self, tree: list[int], i: int) -> int:
        total = 0
        while i > 0:
            total += tree[i]
            i -= i & -i
        return total

    def add(self, left: int, right: int, value: int) -> None:
        self._add(self.b1, left, value)
        self._add(self.b1, right, -value)
        self._add(self.b2, left, value * left)
        self._add(self.b2, right, -value * right)

    def prefix_sum(self, i: int) -> int:  # [0, i) 의 합
        return self._prefix(self.b1, i) * i - self._prefix(self.b2, i)

    def sum(self, left: int, right: int) -> int:
        return self.prefix_sum(right) - self.prefix_sum(left)


class PathAddSubtreeSum:
    """정점 값에 대한 "경로 전체에 더하기", "경로의 합", "서브트리의 합"."""

    def __init__(self, hld: HLD, values: Optional[Sequence[int]] = None):
        self.hld = hld
        self.bit = _RangeAddRangeSum(hld.n)
        if values is not None:
            for v in range(hld.n):
                self.bit.add(hld.pos[v], hld.pos[v] + 1, values[v])

    def add_path(self, u: int, v: int, value: int) -> None:
        for left, right in self.hld.path_segments(u, v):
            self.bit.add(left, right, value)

    def sum_path(self, u: int, v: int) -> int:
        return sum(self.bit.sum(left, right) for left, right in self.hld.path_segments(u, v))

    def add_subtree(self, v: int, value: int) -> None:
        left, right = self.hld.subtree_range(v)
        self.bit.add(left, right, value)

    def sum_subtree(self, v: int) -> int:
        left, right = self.hld.subtree_range(v)
        return self.bit.sum(left, right)


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    edges, weights = [], []
    pos = 1
    for _ in range(n - 1):
        edges.append((int(data[pos]) - 1, int(data[pos + 1]) - 1))
        weights.append(int(data[pos + 2]))
        pos += 3
    hld = HLD(n, edges)
    values = [0] * n
    child_of_edge = []
    for (a, b), w in zip(edges, weights):
        child = b if hld.parent[b] == a else a  # 간선의 아래쪽 정점
        child_of_edge.append(child)
        values[child] = w
    path = PathQuery(hld, values, max, 0, edge=True)
    m = int(data[pos])
    pos += 1
    out = []
    for _ in range(m):
        if data[pos] == b"1":
            path.update(child_of_edge[int(data[pos + 1]) - 1], int(data[pos + 2]))
        else:
            out.append(path.query(int(data[pos + 1]) - 1, int(data[pos + 2]) - 1))
        pos += 3
    print("\n".join(map(str, out)))


if __name__ == "__main__":
    main()
