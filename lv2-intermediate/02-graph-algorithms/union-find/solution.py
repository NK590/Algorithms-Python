"""유니온 파인드(서로소 집합, Disjoint Set Union) — 원소들이 어느 집합에 속하는지 합치고(union) 찾는(find) 자료구조

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 집합마다 하나의 "대표(루트)"가 있는 트리로 표현합니다. 두 원소가 같은 집합인지는 루트가 같은지로 확인합니다.
- 두 가지 최적화: ① 경로 압축(find 하면서 지나온 모든 원소를 루트에 직접 연결) ② 크기에 따른 합치기(작은 트리를 큰 트리 밑에 붙임).
  둘을 함께 쓰면 연산 하나가 분할 상환으로 O(α(n)) ≈ 상수다.
- 원소는 0 ~ n-1 번호입니다. find 는 반복문으로 구현해 깊은 트리에서도 재귀 한도에 걸리지 않습니다.
- 직접 실행하면 아래 형식의 입력(집합의 표현)을 받아 확인 연산마다 YES/NO 를 출력합니다.

      n m          원소는 0 ~ n, m 개의 연산
      0 a b        a 가 속한 집합과 b 가 속한 집합을 합친다
      1 a b        a 와 b 가 같은 집합인지 YES/NO 로 출력한다
"""
import sys


class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))  # 처음에는 모두 자기 자신이 루트
        self.size = [1] * n  # 루트에 대해서만 의미 있는 집합의 크기
        self.count = n  # 집합의 개수

    def find(self, x: int) -> int:
        """x 가 속한 집합의 루트. 루트까지 올라간 뒤, 지나온 모든 원소의 부모를 루트로 바꾼다(경로 압축)."""
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a: int, b: int) -> bool:
        """a 와 b 의 집합을 합친다. 원래 다른 집합이어서 실제로 합쳐졌으면 True, 이미 같은 집합이었으면 False."""
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:  # 작은 쪽을 큰 쪽 밑에 붙여 트리가 깊어지는 것을 막는다
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.count -= 1
        return True

    def connected(self, a: int, b: int) -> bool:
        return self.find(a) == self.find(b)

    def size_of(self, x: int) -> int:
        """x 가 속한 집합의 크기."""
        return self.size[self.find(x)]

    def groups(self) -> list[list[int]]:
        """모든 집합을 원소 목록으로. 각 집합은 오름차순이고, 집합들은 가장 작은 원소 순서."""
        by_root: dict[int, list[int]] = {}
        for x in range(len(self.parent)):
            by_root.setdefault(self.find(x), []).append(x)
        return sorted(by_root.values(), key=lambda g: g[0])


def count_components(n: int, edges: list[tuple[int, int]]) -> int:
    """간선을 모두 합친 뒤 남은 연결 요소의 수."""
    uf = UnionFind(n)
    for a, b in edges:
        uf.union(a, b)
    return uf.count


def first_cycle_edge(n: int, edges: list[tuple[int, int]]) -> int:
    """간선을 순서대로 추가할 때 처음으로 사이클을 만드는 간선의 번호(1부터)를 반환한다. 끝까지 사이클이 없으면 0.

    무방향 그래프에서 이미 같은 집합인 두 정점을 잇는 간선이 사이클을 만든다."""
    uf = UnionFind(n)
    for i, (a, b) in enumerate(edges, start=1):
        if not uf.union(a, b):
            return i
    return 0


def main() -> None:
    input = sys.stdin.readline
    n, m = map(int, input().split())
    uf = UnionFind(n + 1)
    out = []
    for _ in range(m):
        op, a, b = map(int, input().split())
        if op == 0:
            uf.union(a, b)
        else:
            out.append("YES" if uf.connected(a, b) else "NO")
    print("\n".join(out))


if __name__ == "__main__":
    main()
