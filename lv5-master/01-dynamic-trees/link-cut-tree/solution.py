"""링크-컷 트리(Link-Cut Tree) — 간선이 추가·삭제되는 숲(forest)에서 경로 질의·연결성·LCA 를 분할 상환 O(log n) 에

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 아이디어: 각 트리를 "선호 경로(preferred path)" 들로 쪼개고, 경로 하나를 스플레이 트리 하나로 표현한다 (스플레이의 중위 순회 = 경로를 위에서 아래로 훑은 순서).
  경로의 맨 위 정점의 스플레이 트리 루트는 경로 위쪽 정점을 가리키는 "경로 부모(path-parent)" 포인터를 가진다 (같은 parent 배열을 쓰되, 부모가 이 노드를 자식으로 가지지 않으면 경로 부모).
- access(x): 루트에서 x 까지를 하나의 선호 경로로 만든다 (x 아래쪽 선호 경로는 끊는다). 스플레이를 반복해 경로 부모를 따라 올라가며 오른쪽 자식을 갈아 끼운다. 분할 상환 O(log n).
- make_root(x): access(x) 후 그 경로 전체를 뒤집는다(지연 뒤집기) → x 가 트리의 새 루트. 이것으로 "루트가 정해진 트리" 가정이 필요 없어져 link/cut 이 쉬워진다.
- link(u, v): make_root(u) 하고 u 의 경로 부모를 v 로. cut(u, v): make_root(u), access(v) 하면 u 가 v 의 왼쪽 자식이 되어야 간선이 있는 것 → 끊는다.
- path_sum / path_max: make_root(u), access(v) 후 v 의 스플레이 트리 전체가 u–v 경로이므로 집계값을 읽는다. path_add(u, v, d): 같은 서브트리에 지연 덧셈.
- lca(root, u, v): make_root(root) 뒤 access(u) 후 access(v) 의 마지막 스플레이 지점이 LCA.
- 정점 번호는 0 부터 (내부는 1 부터). 모든 연산이 반복문이라 사슬 모양 트리에서도 재귀 깊이 문제가 없다.
- 직접 실행하면 Library Checker "Dynamic Tree Vertex Add Path Sum" 형식 — `N Q`, 정점 값, 간선 N-1 개, 질의 `0 u v w x`(간선 (u,v) 를 끊고 (w,x) 를 잇는다) / `1 p x`(a_p += x) / `2 u v`(경로 합) — 를 처리합니다.
"""
import sys
from typing import Optional, Sequence

NEG_INF = float("-inf")


class LinkCutTree:
    def __init__(self, values: Sequence[int]):
        n = len(values)
        self.n = n
        size = n + 1  # 0 번은 "없음"
        self.left = [0] * size
        self.right = [0] * size
        self.parent = [0] * size
        self.reversed = [False] * size
        self.value = [0] + list(values)
        self.total = [0] + list(values)  # 스플레이 서브트리의 값의 합
        self.high = [NEG_INF] + list(values)  # 스플레이 서브트리의 값의 최댓값
        self.count = [0] + [1] * n  # 서브트리의 정점 수
        self.lazy = [0] * size  # 지연 덧셈 (이 노드 자신에는 이미 반영됨, 자식에게는 아직)

    def _check(self, v: int) -> int:
        if not 0 <= v < self.n:
            raise IndexError("정점 번호가 범위를 벗어났습니다")
        return v + 1

    def _is_root(self, x: int) -> bool:
        p = self.parent[x]
        return p == 0 or (self.left[p] != x and self.right[p] != x)

    def _pull(self, x: int) -> None:
        l, r = self.left[x], self.right[x]
        self.count[x] = self.count[l] + self.count[r] + 1
        self.total[x] = self.total[l] + self.total[r] + self.value[x]
        self.high[x] = max(self.high[l], self.high[r], self.value[x])

    def _apply_add(self, x: int, delta: int) -> None:
        if x:
            self.value[x] += delta
            self.total[x] += delta * self.count[x]
            self.high[x] += delta
            self.lazy[x] += delta

    def _push(self, x: int) -> None:
        if self.reversed[x]:
            l, r = self.left[x], self.right[x]
            self.left[x], self.right[x] = r, l
            if l:
                self.reversed[l] = not self.reversed[l]
            if r:
                self.reversed[r] = not self.reversed[r]
            self.reversed[x] = False
        if self.lazy[x]:
            self._apply_add(self.left[x], self.lazy[x])
            self._apply_add(self.right[x], self.lazy[x])
            self.lazy[x] = 0

    def _rotate(self, x: int) -> None:
        p = self.parent[x]
        g = self.parent[p]
        if not self._is_root(p):  # 조부모의 자식 포인터를 p 에서 x 로 (p 가 스플레이 루트이면 조부모는 경로 부모라 포인터를 건드리지 않는다)
            if self.left[g] == p:
                self.left[g] = x
            else:
                self.right[g] = x
        self.parent[x] = g
        if self.left[p] == x:
            inner = self.right[x]
            self.left[p] = inner
            self.right[x] = p
        else:
            inner = self.left[x]
            self.right[p] = inner
            self.left[x] = p
        if inner:
            self.parent[inner] = p
        self.parent[p] = x
        self._pull(p)
        self._pull(x)

    def _splay(self, x: int) -> None:
        """x 를 자기 스플레이 트리의 루트로. 먼저 루트에서 x 까지 지연 표시를 내려보낸다."""
        path = [x]
        y = x
        while not self._is_root(y):
            y = self.parent[y]
            path.append(y)
        for y in reversed(path):
            self._push(y)
        while not self._is_root(x):
            p = self.parent[x]
            if not self._is_root(p):
                g = self.parent[p]
                same_side = (self.left[g] == p) == (self.left[p] == x)
                self._rotate(p if same_side else x)
            self._rotate(x)

    def _access(self, x: int) -> int:
        """루트에서 x 까지를 선호 경로로 만들고, x 를 그 스플레이 트리의 루트로. 마지막으로 붙인 스플레이 루트(= 두 번째 access 에서는 LCA) 를 돌려준다."""
        last = 0
        y = x
        while y:
            self._splay(y)
            self.right[y] = last
            self._pull(y)
            last = y
            y = self.parent[y]
        self._splay(x)
        return last

    def _make_root(self, x: int) -> None:
        self._access(x)
        self.reversed[x] = not self.reversed[x]

    def _find_root(self, x: int) -> int:
        self._access(x)
        while True:
            self._push(x)
            if not self.left[x]:
                break
            x = self.left[x]
        self._splay(x)
        return x

    # ---- 공개 연산 (정점 번호 0 부터) ----

    def find_root(self, v: int) -> int:
        """v 가 속한 트리의 현재 루트."""
        return self._find_root(self._check(v)) - 1

    def connected(self, u: int, v: int) -> bool:
        return self._find_root(self._check(u)) == self._find_root(self._check(v))

    def link(self, u: int, v: int) -> None:
        """u 와 v 를 잇는다. 이미 같은 트리이면 ValueError (사이클)."""
        x, y = self._check(u), self._check(v)
        if x == y:
            raise ValueError("이미 연결되어 있습니다 (사이클이 생깁니다)")
        self._make_root(x)  # x 가 자기 트리의 루트이자 자기 스플레이 트리의 루트
        if self._find_root(y) == x:  # y 가 x 와 같은 트리면 루트가 x 로 나온다
            raise ValueError("이미 연결되어 있습니다 (사이클이 생깁니다)")
        self.parent[x] = y

    def cut(self, u: int, v: int) -> None:
        """간선 (u, v) 를 끊는다. 그런 간선이 없으면 ValueError."""
        x, y = self._check(u), self._check(v)
        self._make_root(x)
        self._access(y)
        # y 의 스플레이 트리에는 경로 x..y 만 있다. 간선 (x, y) 가 있으면 경로는 정점 두 개: x 가 y 의 왼쪽 자식이고 x 에게 자식이 없다.
        if x == y or self.left[y] != x:
            raise ValueError("그런 간선이 없습니다")
        if self.left[x] or self.right[x]:  # x 에 자식이 하나라도 있으면 경로는 정점 두 개보다 길다 (뒤집기 표시가 남아 있어도 좌우가 바뀔 뿐 자식의 유무는 같다)
            raise ValueError("그런 간선이 없습니다")
        self.left[y] = 0
        self.parent[x] = 0
        self._pull(y)

    def make_root(self, v: int) -> None:
        self._make_root(self._check(v))

    def _path(self, u: int, v: int) -> int:
        x, y = self._check(u), self._check(v)
        self._make_root(x)
        if self._find_root(y) != x:  # x 를 루트로 만들었으니 같은 트리라면 y 의 루트가 x
            raise ValueError("두 정점이 같은 트리에 있지 않습니다")
        self._access(y)
        return y

    def path_sum(self, u: int, v: int) -> int:
        return self.total[self._path(u, v)]

    def path_max(self, u: int, v: int) -> int:
        return self.high[self._path(u, v)]

    def path_length(self, u: int, v: int) -> int:
        """u–v 경로의 정점 수."""
        return self.count[self._path(u, v)]

    def path_add(self, u: int, v: int, delta: int) -> None:
        self._apply_add(self._path(u, v), delta)

    def set_value(self, v: int, value: int) -> None:
        x = self._check(v)
        self._access(x)
        self.value[x] = value
        self._pull(x)

    def add_value(self, v: int, delta: int) -> None:
        x = self._check(v)
        self._access(x)
        self.value[x] += delta
        self._pull(x)

    def get_value(self, v: int) -> int:
        x = self._check(v)
        self._access(x)
        return self.value[x]

    def lca(self, root: int, u: int, v: int) -> int:
        """root 를 루트로 했을 때 u 와 v 의 LCA (세 정점이 같은 트리에 있어야 한다)."""
        r, x, y = self._check(root), self._check(u), self._check(v)
        self._make_root(r)
        if self._find_root(x) != r or self._find_root(y) != r:
            raise ValueError("세 정점이 같은 트리에 있지 않습니다")
        self._access(x)
        return self._access(y) - 1


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    tree = LinkCutTree([int(x) for x in data[2 : 2 + n]])
    pos = 2 + n
    for _ in range(n - 1):
        tree.link(int(data[pos]), int(data[pos + 1]))
        pos += 2
    out = []
    for _ in range(q):
        kind = data[pos]
        if kind == b"0":
            tree.cut(int(data[pos + 1]), int(data[pos + 2]))
            tree.link(int(data[pos + 3]), int(data[pos + 4]))
            pos += 5
        elif kind == b"1":
            tree.add_value(int(data[pos + 1]), int(data[pos + 2]))
            pos += 3
        else:
            out.append(tree.path_sum(int(data[pos + 1]), int(data[pos + 2])))
            pos += 3
    print("\n".join(map(str, out)))


if __name__ == "__main__":
    main()
