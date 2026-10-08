"""블로섬 알고리즘(Blossom Algorithm, Edmonds) — 일반 그래프(이분 그래프가 아니어도 됨)의 최대 매칭, O(V³)

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 매칭을 키우는 "증가 경로(augmenting path)" 를 찾아 뒤집는 것은 이분 매칭과 같다. 다른 점은 홀수 길이 사이클 때문에 BFS 가 헷갈린다는 것:
  홀수 사이클(꽃, blossom) 을 만나면 사이클 전체를 한 정점으로 "수축" 해서 계속 탐색한다.
- root 에서 시작해 교대 트리를 BFS 로 키운다. 짝(match)이 있는 정점 v 의 짝은 "홀수 정점", 그 짝의 짝은 "짝수 정점" 으로 이어진다.
  짝수 정점 v 에서 짝수 정점 to 로 가는 간선을 만나면 둘의 lca 까지 사이클이 생긴 것이므로 base[] 를 lca 로 바꿔 수축한다.
  이때 홀수 정점이었던 것들도 짝수 정점이 되어 (큐에 다시 들어가) 탐색을 이어 간다.
- 짝이 없는 정점에 닿으면 증가 경로가 발견된 것이다. parent[] 와 match[] 를 번갈아 따라가며 뒤집는다.
- max_matching(n, edges): (매칭 크기, mate) — mate[v] 는 v 의 짝 (없으면 -1).
- gallai_edmonds(n, edges): 최대 매칭과 함께 갈라이-에드먼즈 분해 (D, A, C) 를 돌려준다. 최대 매칭에서 짝 없는 정점들을 한꺼번에 뿌리로 교대 트리를 키워 짝수 정점이 된 것들이 D (어떤 최대 매칭에서 짝이 없을 수 있는 정점),
  D 의 이웃 중 D 밖이 A, 나머지가 C. A 는 투테-버지 공식의 증명서가 된다: n - 2·ν = (G - A 의 홀수 성분 수) - |A|.
- 직접 실행하면 Library Checker "General Matching" 형식 — `N M`, 이어서 M 줄의 `a b` — 를 받아 매칭 크기와 짝 지은 간선(`a b`)을 출력합니다.
"""
import sys
from collections import deque
from typing import Iterable, Sequence


def _adjacency(n: int, edges: Iterable[Sequence[int]]) -> list[list[int]]:
    adj: list[set[int]] = [set() for _ in range(n)]
    for a, b in edges:
        if not (0 <= a < n and 0 <= b < n):
            raise ValueError("정점 번호가 범위를 벗어났습니다")
        if a != b:  # 자기 루프는 매칭에 쓸 수 없다
            adj[a].add(b)
            adj[b].add(a)
    return [sorted(s) for s in adj]


class _Matcher:
    """한 그래프에 대해 mate 를 들고 증가 경로를 찾는 작업대."""

    def __init__(self, n: int, adj: list[list[int]]):
        self.n = n
        self.adj = adj
        self.mate = [-1] * n
        self.parent = [-1] * n
        self.base = list(range(n))
        self.is_even = [False] * n  # 교대 트리의 짝수 정점 (큐에 들어간 적이 있는 정점)
        self.in_blossom = [False] * n

    def _lca(self, a: int, b: int) -> int:
        """교대 트리에서 a, b 가 속한 꽃(base) 의 가장 가까운 공통 조상."""
        seen = [False] * self.n
        while True:  # a 에서 뿌리까지 올라가며 표시
            a = self.base[a]
            seen[a] = True
            if self.mate[a] == -1:
                break
            a = self.parent[self.mate[a]]
        while True:  # b 에서 올라가다 표시된 곳을 만나면 그곳이 lca
            b = self.base[b]
            if seen[b]:
                return b
            b = self.parent[self.mate[b]]

    def _mark_path(self, v: int, b: int, child: int) -> None:
        """v 에서 꽃의 base b 까지 경로의 꽃 소속을 표시하고, 홀수였던 정점이 맞은편을 부모로 갖게 한다."""
        while self.base[v] != b:
            self.in_blossom[self.base[v]] = True
            self.in_blossom[self.base[self.mate[v]]] = True
            self.parent[v] = child
            child = self.mate[v]
            v = self.parent[self.mate[v]]

    def search(self, roots: list[int]) -> int:
        """roots (짝 없는 정점들) 에서 시작하는 교대 트리를 키워 증가 경로의 끝(짝 없는 정점) 을 찾는다. 없으면 -1.

        뿌리가 둘 이상일 때는 서로 다른 트리의 짝수 정점이 간선으로 이어지지 않는다는 보장(= 현재 매칭이 최대)이 필요하다.
        """
        n = self.n
        self.parent = [-1] * n
        self.base = list(range(n))
        self.is_even = [False] * n
        queue: deque[int] = deque()
        for r in roots:
            self.is_even[r] = True
            queue.append(r)
        while queue:
            v = queue.popleft()
            for to in self.adj[v]:
                if self.base[v] == self.base[to]:
                    continue  # 같은 꽃 안 (v 의 짝은 같은 꽃 안이거나 이미 홀수 표가 붙어 있다)
                if self.is_even[to]:
                    # to 도 짝수 정점: 홀수 길이 사이클 발견, 꽃을 수축한다
                    current_base = self._lca(v, to)
                    self.in_blossom = [False] * n
                    self._mark_path(v, current_base, to)
                    self._mark_path(to, current_base, v)
                    for i in range(n):
                        if self.in_blossom[self.base[i]]:
                            self.base[i] = current_base
                            if not self.is_even[i]:
                                self.is_even[i] = True
                                queue.append(i)
                elif self.parent[to] == -1:
                    self.parent[to] = v
                    if self.mate[to] == -1:
                        return to
                    self.is_even[self.mate[to]] = True
                    queue.append(self.mate[to])
        return -1

    def augment_from(self, root: int) -> bool:
        end = self.search([root])
        if end == -1:
            return False
        while end != -1:  # 증가 경로를 따라 짝을 뒤집는다
            prev = self.parent[end]
            nxt = self.mate[prev]
            self.mate[end], self.mate[prev] = prev, end
            end = nxt
        return True


def max_matching(n: int, edges: Iterable[Sequence[int]]) -> tuple[int, list[int]]:
    """정점 0..n-1, 무방향 간선 목록 → (최대 매칭의 크기, mate 배열). 다중 간선·자기 루프는 무시한다."""
    matcher = _Matcher(n, _adjacency(n, edges))
    # 탐욕으로 초기 매칭을 만들어 증가 경로 탐색 횟수를 줄인다
    for v in range(n):
        if matcher.mate[v] == -1:
            for to in matcher.adj[v]:
                if matcher.mate[to] == -1:
                    matcher.mate[v], matcher.mate[to] = to, v
                    break
    for v in range(n):
        if matcher.mate[v] == -1:
            matcher.augment_from(v)
    mate = matcher.mate
    return sum(1 for v in range(n) if mate[v] > v), mate


def gallai_edmonds(n: int, edges: Iterable[Sequence[int]]) -> dict:
    """최대 매칭과 갈라이-에드먼즈 분해.

    돌려주는 dict: size, mate, D (어떤 최대 매칭에서 짝이 없을 수 있는 정점), A (D 의 이웃 중 D 밖), C (나머지).
    """
    adj = _adjacency(n, edges)
    size, mate = max_matching(n, [(a, b) for a in range(n) for b in adj[a] if a < b])
    matcher = _Matcher(n, adj)
    matcher.mate = list(mate)
    roots = [v for v in range(n) if mate[v] == -1]
    matcher.search(roots)  # 최대 매칭이므로 항상 -1: 짝수 정점 집합이 곧 D
    d_set = {v for v in range(n) if matcher.is_even[v]}
    a_set = {to for v in d_set for to in adj[v] if to not in d_set}
    c_set = set(range(n)) - d_set - a_set
    return {"size": size, "mate": mate, "D": sorted(d_set), "A": sorted(a_set), "C": sorted(c_set)}


def main() -> None:
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    edges = [(int(data[2 + 2 * i]), int(data[3 + 2 * i])) for i in range(m)]
    size, mate = max_matching(n, edges)
    out = [str(size)]
    for v in range(n):
        if mate[v] > v:
            out.append(f"{v} {mate[v]}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
