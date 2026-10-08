"""느리게 갱신되는 세그먼트 트리(Lazy Propagation) — 구간 전체에 대한 갱신(더하기, 대입)과 구간 질의를 모두 O(log n) 에 처리하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 구간 갱신을 모든 리프에 적용하면 O(n) 입니다. 대신 구간을 완전히 덮는 노드에만 "이 구간 전체에 f 를 적용하라" 는 표시(lazy)를 남기고
  노드의 값만 즉시 고칩니다. 표시는 그 노드의 자식을 방문해야 할 때 비로소 아래로 내려보냅니다(push).
- 일반화한 클래스 LazySegmentTree 는 네 가지를 받습니다.
    op(x, y)            두 구간 값을 합치는 결합 연산 (합, 최솟값, …)  / identity   그 항등원
    apply(f, x, length) 길이 length 인 구간의 값 x 에 갱신 f 를 적용한 결과 (구간 더하기+합이면 x + f·length)
    compose(f, g)       갱신 g 를 먼저, 그다음 f 를 했을 때의 합성 갱신              / lazy_identity   아무것도 하지 않는 갱신
- 구간은 0 부터 시작하는 반열린 [left, right) 입니다. 재귀 구현이라 읽기 쉽지만 파이썬에서는 느린 편입니다(README 참고).
- 만들어 둔 세 가지: range_add_range_sum, range_add_range_min, range_assign_range_sum.
- 직접 실행하면 `N M K`, N 개의 수, 그리고 M + K 개의 질의(`1 b c d`: b..c 번째에 d 더하기, `2 b c`: b..c 번째의 합)를 받아 합 질의의 결과를 출력합니다.
"""
import sys
from typing import Callable


class LazySegmentTree:
    def __init__(
        self,
        values: list,
        op: Callable,
        identity,
        apply: Callable,
        compose: Callable,
        lazy_identity,
    ):
        self.n = len(values)
        self.op = op
        self.identity = identity
        self.apply = apply
        self.compose = compose
        self.lazy_identity = lazy_identity
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.tree = [identity] * (2 * self.size)
        self.lazy = [lazy_identity] * (2 * self.size)
        self.tree[self.size : self.size + self.n] = values
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = op(self.tree[2 * i], self.tree[2 * i + 1])

    def _apply_to_node(self, node: int, f, length: int) -> None:
        """노드의 값을 즉시 고치고, 자식이 있다면 f 를 lazy 에 쌓아 둔다."""
        self.tree[node] = self.apply(f, self.tree[node], length)
        if node < self.size:
            self.lazy[node] = self.compose(f, self.lazy[node])

    def _push(self, node: int, length: int) -> None:
        """node 에 쌓인 표시를 두 자식에게 내려보낸다. length 는 node 가 맡은 구간의 길이."""
        f = self.lazy[node]
        if f != self.lazy_identity:
            half = length // 2
            self._apply_to_node(2 * node, f, half)
            self._apply_to_node(2 * node + 1, f, half)
            self.lazy[node] = self.lazy_identity

    def update(self, left: int, right: int, f) -> None:
        """a[left .. right-1] 전체에 갱신 f 를 적용한다."""
        self._update(1, 0, self.size, left, right, f)

    def _update(self, node: int, node_left: int, node_right: int, left: int, right: int, f) -> None:
        if right <= node_left or node_right <= left:
            return  # 겹치지 않는다
        if left <= node_left and node_right <= right:
            self._apply_to_node(node, f, node_right - node_left)  # 완전히 덮는다: 표시만 남기고 끝
            return
        self._push(node, node_right - node_left)  # 일부만 겹친다: 자식을 보기 전에 밀린 갱신을 내려보낸다
        mid = (node_left + node_right) // 2
        self._update(2 * node, node_left, mid, left, right, f)
        self._update(2 * node + 1, mid, node_right, left, right, f)
        self.tree[node] = self.op(self.tree[2 * node], self.tree[2 * node + 1])

    def query(self, left: int, right: int):
        """op(a[left], …, a[right-1]). 빈 구간이면 항등원."""
        return self._query(1, 0, self.size, left, right)

    def _query(self, node: int, node_left: int, node_right: int, left: int, right: int):
        if right <= node_left or node_right <= left:
            return self.identity
        if left <= node_left and node_right <= right:
            return self.tree[node]
        self._push(node, node_right - node_left)
        mid = (node_left + node_right) // 2
        return self.op(
            self._query(2 * node, node_left, mid, left, right),
            self._query(2 * node + 1, mid, node_right, left, right),
        )

    def get(self, index: int):
        return self.query(index, index + 1)


def range_add_range_sum(values: list[int]) -> LazySegmentTree:
    """구간에 d 를 더하고 구간 합을 구한다. 갱신 f = d(더할 값), 길이 length 인 구간의 합은 f · length 만큼 늘어난다."""
    return LazySegmentTree(
        values,
        op=lambda x, y: x + y,
        identity=0,
        apply=lambda f, x, length: x + f * length,
        compose=lambda f, g: f + g,
        lazy_identity=0,
    )


def range_add_range_min(values: list[int]) -> LazySegmentTree:
    """구간에 d 를 더하고 구간 최솟값을 구한다. 구간의 모든 값이 d 만큼 늘면 최솟값도 d 만큼 늘 뿐이다."""
    return LazySegmentTree(
        values,
        op=min,
        identity=float("inf"),
        apply=lambda f, x, length: x + f,
        compose=lambda f, g: f + g,
        lazy_identity=0,
    )


def range_assign_range_sum(values: list[int]) -> LazySegmentTree:
    """구간을 전부 v 로 바꾸고 구간 합을 구한다. 갱신 None 은 '아무것도 안 함', 합성은 나중 갱신이 이긴다."""
    return LazySegmentTree(
        values,
        op=lambda x, y: x + y,
        identity=0,
        apply=lambda f, x, length: x if f is None else f * length,
        compose=lambda f, g: g if f is None else f,
        lazy_identity=None,
    )


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m, k = int(data[0]), int(data[1]), int(data[2])
    tree = range_add_range_sum([int(x) for x in data[3 : 3 + n]])
    out = []
    pos = 3 + n
    for _ in range(m + k):
        if data[pos] == b"1":
            b, c, d = int(data[pos + 1]), int(data[pos + 2]), int(data[pos + 3])
            pos += 4
            tree.update(b - 1, c, d)
        else:
            b, c = int(data[pos + 1]), int(data[pos + 2])
            pos += 3
            out.append(tree.query(b - 1, c))
    print("\n".join(map(str, out)))


if __name__ == "__main__":
    main()
