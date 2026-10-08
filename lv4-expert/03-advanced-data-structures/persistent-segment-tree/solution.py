"""퍼시스턴트 세그먼트 트리(Persistent Segment Tree) — 갱신할 때마다 "새 버전" 을 만들고 과거 버전도 질의할 수 있는 구간 트리

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 경로 복사(path copying): 한 점을 갱신하면 바뀌는 노드는 루트에서 그 잎까지의 O(log n) 개뿐이다. 그 노드들만 새로 만들고 나머지 자식은 옛 노드를 그대로 가리키면,
  갱신 한 번에 O(log n) 노드만 늘면서 옛 루트에서는 옛 버전이 그대로 보인다.
- PersistentSegmentTree(n): 구간 [0, n) 위의 합 트리. update(version, index, delta) -> 새 버전 번호. query(version, l, r) 반열린 구간 합.
  노드는 배열(left, right, value) 에 저장하고 0 번 노드는 "값 0 인 빈 트리" (모든 자식이 자기 자신) — 처음 버전 0 은 길이 n 의 영 배열.
- PersistentArray: 버전별 배열. get(version, i), set(version, i, value) -> 새 버전. 과거 버전에서 갈라져 나가는 것(분기) 도 된다.
- KthSmallest(values): 구간 [l, r) 에서 k 번째로 작은 값 (오프라인이 아니라 온라인), count_less(l, r, x).
  값을 압축해 i 번째 버전 = 앞의 i 개 원소를 넣은 트리로 만들고, 두 버전의 차(root[r] - root[l]) 가 구간의 값 분포이므로 트리를 내려가며 k 번째를 찾는다.
- 모든 연산이 반복문이라 깊이 문제가 없다.
- 직접 실행하면 BOJ 7469 형식 — `N M`, 수열, M 개의 `i j k`(1부터) — 를 받아 a[i..j] 에서 k 번째로 작은 값을 출력합니다.
"""
import sys
from bisect import bisect_left, bisect_right
from typing import Sequence


class PersistentSegmentTree:
    def __init__(self, n: int):
        if n < 1:
            raise ValueError("n 은 1 이상이어야 합니다")
        self.n = n
        self.left = [0]  # 0 번 노드: 값 0 인 빈 트리 (자식은 자기 자신)
        self.right = [0]
        self.value = [0]
        self.roots = [0]  # roots[v] = 버전 v 의 루트. 버전 0 = 모두 0

    def _clone(self, node: int, delta: int) -> int:
        self.left.append(self.left[node])
        self.right.append(self.right[node])
        self.value.append(self.value[node] + delta)
        return len(self.value) - 1

    def update(self, version: int, index: int, delta: int) -> int:
        """버전 version 의 a[index] 에 delta 를 더한 새 버전의 번호를 돌려준다. 옛 버전은 그대로 남는다."""
        if not 0 <= index < self.n:
            raise IndexError("index 가 범위를 벗어났습니다")
        old = self.roots[version]
        new_root = self._clone(old, delta)
        node, lo, hi = new_root, 0, self.n
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if index < mid:
                child = self._clone(self.left[old], delta)
                self.left[node] = child
                old = self.left[old]
                hi = mid
            else:
                child = self._clone(self.right[old], delta)
                self.right[node] = child
                old = self.right[old]
                lo = mid
            node = child
        self.roots.append(new_root)
        return len(self.roots) - 1

    def query(self, version: int, left: int, right: int) -> int:
        """버전 version 에서 반열린 구간 [left, right) 의 합."""
        if not 0 <= left <= right <= self.n:
            raise IndexError("구간이 범위를 벗어났습니다")
        total = 0
        stack = [(self.roots[version], 0, self.n)]
        while stack:
            node, lo, hi = stack.pop()
            if node == 0 or right <= lo or hi <= left:
                continue  # 빈 서브트리(합 0) 이거나 구간 밖
            if left <= lo and hi <= right:
                total += self.value[node]
                continue
            mid = (lo + hi) // 2
            stack.append((self.left[node], lo, mid))
            stack.append((self.right[node], mid, hi))
        return total

    def kth_in_difference(self, version_hi: int, version_lo: int, k: int) -> int:
        """두 버전 root[hi] - root[lo] 가 나타내는 다중집합(각 칸의 값 = 개수) 에서 k 번째(1부터) 로 작은 칸의 번호."""
        a, b = self.roots[version_hi], self.roots[version_lo]
        if k < 1 or self.value[a] - self.value[b] < k:
            raise ValueError("k 가 범위를 벗어났습니다")
        lo, hi = 0, self.n
        while hi - lo > 1:
            mid = (lo + hi) // 2
            in_left = self.value[self.left[a]] - self.value[self.left[b]]
            if k <= in_left:
                a, b, hi = self.left[a], self.left[b], mid
            else:
                k -= in_left
                a, b, lo = self.right[a], self.right[b], mid
        return lo

    def node_count(self) -> int:
        return len(self.value)


class PersistentArray:
    """버전이 있는 배열. 모든 과거 버전을 읽을 수 있고 어느 버전에서든 갈라져 나갈 수 있다."""

    def __init__(self, values: Sequence[int]):
        self.tree = PersistentSegmentTree(max(1, len(values)))
        version = 0
        for i, value in enumerate(values):
            if value:
                version = self.tree.update(version, i, value)
        self.initial_version = version
        self.length = len(values)

    def get(self, version: int, index: int) -> int:
        return self.tree.query(version, index, index + 1)

    def set(self, version: int, index: int, value: int) -> int:
        """버전 version 에서 a[index] = value 로 바꾼 새 버전."""
        return self.tree.update(version, index, value - self.get(version, index))


class KthSmallest:
    """정적 배열의 구간 k 번째 작은 수 (온라인). 준비 O(n log n), 질의 O(log n)."""

    def __init__(self, values: Sequence[int]):
        self.n = len(values)
        self.sorted_values = sorted(set(values))
        self.tree = PersistentSegmentTree(max(1, len(self.sorted_values)))
        self.versions = [0]  # versions[i] = 앞의 i 개를 넣은 버전
        for v in values:
            self.versions.append(self.tree.update(self.versions[-1], bisect_left(self.sorted_values, v), 1))

    def kth(self, left: int, right: int, k: int) -> int:
        """반열린 구간 [left, right) 에서 k 번째(1부터) 로 작은 값."""
        if not 0 <= left < right <= self.n:
            raise ValueError("구간이 범위를 벗어났습니다")
        return self.sorted_values[self.tree.kth_in_difference(self.versions[right], self.versions[left], k)]

    def count_less(self, left: int, right: int, x: int) -> int:
        """[left, right) 에서 x 보다 작은 값의 개수."""
        return self._count_below(left, right, bisect_left(self.sorted_values, x))

    def count_at_most(self, left: int, right: int, x: int) -> int:
        """[left, right) 에서 x 이하인 값의 개수."""
        return self._count_below(left, right, bisect_right(self.sorted_values, x))

    def _count_below(self, left: int, right: int, limit: int) -> int:
        """압축된 값의 번호가 limit 미만인 원소의 수."""
        return self.tree.query(self.versions[right], 0, limit) - self.tree.query(self.versions[left], 0, limit)


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    structure = KthSmallest([int(x) for x in data[2 : 2 + n]])
    out = []
    pos = 2 + n
    for _ in range(m):
        i, j, k = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])
        out.append(structure.kth(i - 1, j, k))
        pos += 3
    print("\n".join(map(str, out)))


if __name__ == "__main__":
    main()
