"""센트로이드 분해(Centroid Decomposition) — 트리를 "중심 정점" 으로 재귀적으로 쪼개 경로 문제를 O(n log n) 개의 (정점, 조상) 쌍으로 바꾸기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 센트로이드: 지우면 남는 모든 조각의 크기가 (전체 / 2) 이하인 정점 (모든 트리에 하나 이상 있다).
  트리의 센트로이드 c 를 고르고 지운 뒤, 남은 조각들에서 같은 일을 되풀이하면 깊이가 log₂ n 이하인 "센트로이드 트리" 가 만들어진다.
- 임의의 두 정점 u, v 를 잇는 경로는 센트로이드 트리에서 두 정점의 가장 가까운 공통 조상 c 를 지난다 (c 를 지운 순간 둘이 다른 조각으로 갈라지므로).
  그래서 dist(u, v) = min over 공통 조상 a 의 dist(u, a) + dist(a, v) 이고, 경로에 관한 질문은 "센트로이드를 지나는 경로만" 세면 된다.
- CentroidDecomposition: parent(센트로이드 트리의 부모), level, dist[v][i] (v 에서 레벨 i 인 센트로이드 조상까지의 거리), 각 센트로이드의 조각에 있는 거리들과 자식 조각별 거리들.
  모든 작업이 반복문이라 사슬 모양 트리(깊이 10^5) 에서도 재귀 깊이 문제가 없다.
- NearestMarked: 정점을 칠하고 "가장 가까운 칠한 정점까지의 거리" 질의 (조상 O(log n) 개만 갱신/조회).
- count_paths_at_most(k), count_paths_with_length(k): 거리가 k 이하 / 정확히 k 인 정점 쌍의 수.
- 직접 실행하면 CF 342E 형식 — 트리(1부터), 정점 1 은 처음부터 빨강, 질의 `1 v`(v 를 빨강으로), `2 v`(v 에서 가장 가까운 빨간 정점까지의 거리) — 를 처리해 2 번 질의의 답을 출력합니다.
"""
import sys
from collections import Counter, deque
from typing import Sequence

INF = float("inf")


class CentroidDecomposition:
    def __init__(self, n: int, edges: Sequence[tuple[int, int]]):
        adj: list[list[int]] = [[] for _ in range(n)]
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)
        if len(edges) != n - 1:
            raise ValueError("트리가 아닙니다 (간선이 n - 1 개가 아님)")
        self.n = n
        self.parent = [-1] * n  # 센트로이드 트리의 부모
        self.level = [0] * n  # 센트로이드 트리에서의 깊이 (루트 0)
        self.dist: list[list[int]] = [[] for _ in range(n)]  # dist[v][i] = v 에서 레벨 i 의 센트로이드 조상까지의 거리
        self.group_distances: list[list[list[int]]] = [[] for _ in range(n)]  # 센트로이드 c 의 조각을 자식 조각별로 나눈 c 로부터의 거리들
        self.root = -1
        removed = [False] * n
        seen_count = 0
        work = [(0, -1, 0)]  # (조각 안의 아무 정점, 센트로이드 트리의 부모, 레벨)
        size = [0] * n
        tparent = [-1] * n
        while work:
            start, centroid_parent, level = work.pop()
            # 1) 조각을 BFS 로 훑어 크기를 구한다
            order = [start]
            tparent[start] = -1
            index = 0
            while index < len(order):
                v = order[index]
                index += 1
                for w in adj[v]:
                    if not removed[w] and w != tparent[v]:
                        tparent[w] = v
                        order.append(w)
            for v in reversed(order):
                size[v] = 1
            for v in reversed(order):
                p = tparent[v]
                if p != -1:
                    size[p] += size[v]
            total = len(order)
            # 2) 센트로이드: 가장 큰 자식 조각이 total/2 를 넘지 않을 때까지 무거운 쪽으로 내려간다
            c = start
            while True:
                heavy = next((w for w in adj[c] if not removed[w] and w != tparent[c] and size[w] * 2 > total), None)
                if heavy is None:
                    break
                c = heavy
            self.parent[c] = centroid_parent
            self.level[c] = level
            if centroid_parent == -1:
                self.root = c
            # 3) c 에서 조각 전체를 BFS 해서 거리를 기록하고, 이웃마다(= 자식 조각마다) 거리들을 모은다
            self.dist[c].append(0)
            groups: list[list[int]] = []
            for first in adj[c]:
                if removed[first]:
                    continue
                group: list[int] = []
                queue = deque([(first, c, 1)])
                while queue:
                    v, p, d = queue.popleft()
                    self.dist[v].append(d)
                    group.append(d)
                    for w in adj[v]:
                        if w != p and not removed[w]:
                            queue.append((w, v, d + 1))
                groups.append(group)
            self.group_distances[c] = groups
            removed[c] = True
            seen_count += 1
            for first in adj[c]:
                if not removed[first]:
                    work.append((first, c, level + 1))
        assert seen_count == n

    def ancestors(self, v: int) -> list[int]:
        """v 의 센트로이드 조상들을 레벨 0(루트) 부터 v 자신까지."""
        chain = []
        while v != -1:
            chain.append(v)
            v = self.parent[v]
        return chain[::-1]

    def distance(self, u: int, v: int) -> int:
        """두 정점 사이의 거리 = 공통 센트로이드 조상에서의 거리 합의 최솟값."""
        chain_u, chain_v = self.ancestors(u), self.ancestors(v)
        best = INF
        for i, (a, b) in enumerate(zip(chain_u, chain_v)):
            if a != b:
                break  # 공통 조상은 여기까지
            best = min(best, self.dist[u][i] + self.dist[v][i])
        return int(best)

    def count_paths_at_most(self, k: int) -> int:
        """거리가 k 이하인 정점 쌍(순서 없는, 서로 다른 두 정점) 의 수. 센트로이드 c 를 지나는 쌍 = (c 조각 전체의 쌍) - (같은 자식 조각 안의 쌍)."""

        def pairs(distances: list[int]) -> int:
            ordered = sorted(distances)
            count, low, high = 0, 0, len(ordered) - 1
            while low < high:  # 두 포인터: 합이 k 이하인 (low < high) 쌍의 수
                if ordered[low] + ordered[high] <= k:
                    count += high - low
                    low += 1
                else:
                    high -= 1
            return count

        total = 0
        for c in range(self.n):
            groups = self.group_distances[c]
            whole = [0] + [d for group in groups for d in group]
            total += pairs(whole) - sum(pairs(group) for group in groups)
        return total

    def count_paths_with_length(self, k: int) -> int:
        """거리가 정확히 k 인 정점 쌍의 수."""
        total = 0
        for c in range(self.n):
            seen: Counter = Counter({0: 1})  # c 자신
            for group in self.group_distances[c]:
                total += sum(seen[k - d] for d in group)
                for d in group:
                    seen[d] += 1
        return total


class NearestMarked:
    """정점을 칠하고 가장 가까운 칠한 정점까지의 거리를 묻는다. 칠하기·질의 모두 O(log n)."""

    def __init__(self, decomposition: CentroidDecomposition):
        self.cd = decomposition
        self.best = [INF] * decomposition.n  # best[c] = c 의 조각 안에서 칠한 정점까지의 c 로부터의 최소 거리
        self.chains = [decomposition.ancestors(v) for v in range(decomposition.n)]

    def mark(self, v: int) -> None:
        for i, a in enumerate(self.chains[v]):
            self.best[a] = min(self.best[a], self.cd.dist[v][i])

    def nearest(self, v: int) -> float:
        """가장 가까운 칠한 정점까지의 거리. 칠한 정점이 없으면 무한대."""
        return min((self.best[a] + self.cd.dist[v][i] for i, a in enumerate(self.chains[v])), default=INF)


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    edges = [(int(data[2 + 2 * i]) - 1, int(data[3 + 2 * i]) - 1) for i in range(n - 1)]
    pos = 2 + 2 * (n - 1)
    structure = NearestMarked(CentroidDecomposition(n, edges))
    structure.mark(0)
    out = []
    for _ in range(m):
        v = int(data[pos + 1]) - 1
        if data[pos] == b"1":
            structure.mark(v)
        else:
            out.append(int(structure.nearest(v)))
        pos += 2
    print("\n".join(map(str, out)))


if __name__ == "__main__":
    main()
