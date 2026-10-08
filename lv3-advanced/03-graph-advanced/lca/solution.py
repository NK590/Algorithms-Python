"""최소 공통 조상(LCA, Lowest Common Ancestor) — 루트가 있는 트리에서 두 정점의 가장 깊은 공통 조상 찾기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- BinaryLiftingLCA: up[k][v] = v 의 2^k 번째 조상을 표로 만들어 두고(희소 배열과 같은 아이디어), 두 정점의 깊이를 맞춘 뒤
  함께 올라갑니다. 구축 O(n log n), 질의 O(log n). 두 정점 사이의 거리, k 번째 조상도 같은 표로 구합니다.
- EulerTourLCA: DFS 방문 순서(오일러 투어)를 배열로 펴면 LCA 는 두 정점의 첫 등장 사이에서 깊이가 가장 작은 정점입니다.
  구간 최솟값을 희소 배열로 구해 질의 O(1) (구축 O(n log n)).
- 모두 반복문으로 구현해 정점이 10^5 개인 사슬 모양의 트리에서도 재귀 깊이 문제가 없습니다. 정점은 0 부터 n-1.
- 직접 실행하면 `N`, N-1 개의 간선(1 부터), `M`, M 개의 질의 `a b` 를 받아 각 질의의 LCA 를 출력합니다. 루트는 1.
"""
import sys
from collections import deque


def _build_adjacency(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adjacency: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        adjacency[a].append(b)
        adjacency[b].append(a)
    return adjacency


class BinaryLiftingLCA:
    """무방향 트리의 간선 목록과 루트로 만든다. n = 정점 수."""

    def __init__(self, n: int, edges: list[tuple[int, int]], root: int = 0):
        adjacency = _build_adjacency(n, edges)
        self.n = n
        self.root = root
        self.depth = [0] * n
        parent = [root] * n  # 루트의 부모는 자기 자신으로 둔다 (넘쳐 올라가도 루트에 머문다)
        seen = [False] * n
        seen[root] = True
        queue = deque([root])
        while queue:
            v = queue.popleft()
            for w in adjacency[v]:
                if not seen[w]:
                    seen[w] = True
                    parent[w] = v
                    self.depth[w] = self.depth[v] + 1
                    queue.append(w)
        self.log = max(1, (n - 1).bit_length())  # 올라갈 수 있는 최대 높이가 n - 1 이하
        self.up = [parent]
        for k in range(1, self.log):
            previous = self.up[-1]
            self.up.append([previous[previous[v]] for v in range(n)])

    def kth_ancestor(self, v: int, k: int) -> int:
        """v 의 k 번째 조상. 루트보다 위로 가면 루트."""
        if k < 0:
            raise ValueError("k 는 0 이상이어야 합니다")
        k = min(k, self.depth[v])  # 표가 다루는 높이를 넘지 않게 하면서, 루트를 지나친 경우는 루트로
        for bit in range(self.log):
            if k >> bit & 1:
                v = self.up[bit][v]
        return v

    def lca(self, u: int, v: int) -> int:
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        u = self.kth_ancestor(u, self.depth[u] - self.depth[v])  # 깊이를 맞춘다
        if u == v:
            return u
        for bit in range(self.log - 1, -1, -1):
            if self.up[bit][u] != self.up[bit][v]:  # 아직 만나지 않는 가장 높은 곳까지 함께 올라간다
                u = self.up[bit][u]
                v = self.up[bit][v]
        return self.up[0][u]

    def distance(self, u: int, v: int) -> int:
        """u 에서 v 까지 지나는 간선의 수."""
        return self.depth[u] + self.depth[v] - 2 * self.depth[self.lca(u, v)]

    def is_ancestor(self, u: int, v: int) -> bool:
        """u 가 v 의 조상(자기 자신 포함)인가."""
        return self.lca(u, v) == u


class EulerTourLCA:
    """오일러 투어 + 희소 배열. 질의 O(1)."""

    def __init__(self, n: int, edges: list[tuple[int, int]], root: int = 0):
        adjacency = _build_adjacency(n, edges)
        self.depth = [0] * n
        self.first = [0] * n
        tour: list[int] = []  # 정점을 방문하거나 자식에서 돌아올 때마다 기록한다
        visited = [False] * n
        visited[root] = True
        stack = [(root, 0)]  # (정점, 다음에 볼 이웃의 인덱스)
        self.first[root] = 0
        tour.append(root)
        while stack:
            v, i = stack.pop()
            if i < len(adjacency[v]):
                stack.append((v, i + 1))
                w = adjacency[v][i]
                if not visited[w]:
                    visited[w] = True
                    self.depth[w] = self.depth[v] + 1
                    self.first[w] = len(tour)
                    tour.append(w)
                    stack.append((w, 0))
            elif stack:  # v 의 모든 이웃을 봤고, 부모로 돌아간다
                tour.append(stack[-1][0])
        self.tour = tour
        # 희소 배열: table[k][i] = tour[i .. i + 2^k) 중 깊이가 가장 작은 정점
        self.table = [tour]
        k = 1
        while (1 << k) <= len(tour):
            previous = self.table[-1]
            half = 1 << (k - 1)
            self.table.append(
                [
                    previous[i] if self.depth[previous[i]] <= self.depth[previous[i + half]] else previous[i + half]
                    for i in range(len(tour) - (1 << k) + 1)
                ]
            )
            k += 1

    def lca(self, u: int, v: int) -> int:
        left, right = sorted((self.first[u], self.first[v]))
        k = (right - left + 1).bit_length() - 1
        a = self.table[k][left]
        b = self.table[k][right - (1 << k) + 1]
        return a if self.depth[a] <= self.depth[b] else b

    def distance(self, u: int, v: int) -> int:
        return self.depth[u] + self.depth[v] - 2 * self.depth[self.lca(u, v)]


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    edges = [(int(data[1 + 2 * i]) - 1, int(data[2 + 2 * i]) - 1) for i in range(n - 1)]
    pos = 1 + 2 * (n - 1)
    m = int(data[pos])
    tree = BinaryLiftingLCA(n, edges)
    out = []
    for i in range(m):
        a, b = int(data[pos + 1 + 2 * i]) - 1, int(data[pos + 2 + 2 * i]) - 1
        out.append(tree.lca(a, b) + 1)
    print("\n".join(map(str, out)))


if __name__ == "__main__":
    main()
