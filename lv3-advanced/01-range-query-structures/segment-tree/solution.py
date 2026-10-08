"""세그먼트 트리(Segment Tree) — 결합 법칙이 성립하는 연산(합·최솟값·최댓값·gcd·…)의 구간 질의와 점 갱신을 O(log n) 에 처리하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 이진 트리의 각 노드가 "자기 구간의 연산 결과" 를 저장합니다. 리프는 원소, 부모는 두 자식의 연산 결과입니다.
- 아래에서 위로 올라가는 반복문 구현(bottom-up)이라 재귀보다 파이썬에서 훨씬 빠릅니다. 크기를 2 의 거듭제곱으로 맞춰
  연산이 교환 법칙을 만족하지 않아도(행렬 곱, 문자열 이어 붙이기, 최대 연속 부분 합 노드) 올바르게 동작합니다.
- 구간은 0 부터 시작하는 반열린 [left, right) 입니다. 연산 op 는 결합 법칙을 만족해야 하고 항등원 identity 가 있어야 합니다.
- 구성: SegmentTree(update, query, get, max_right), 응용(최대 연속 부분 합, 구간 gcd).
- 직접 실행하면 `N M`, N 개의 수, 구간 질의 M 개(`a b`: a 번째부터 b 번째까지, 1 부터)를 받아 각 구간의 최솟값과 최댓값을 출력합니다.
"""
import math
import sys
from typing import Callable


class SegmentTree:
    """values 의 구간 질의를 op 로 처리한다. 점 갱신 O(log n), 구간 질의 O(log n), 구축 O(n)."""

    def __init__(self, values: list, op: Callable, identity):
        self.n = len(values)
        self.op = op
        self.identity = identity
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.tree = [identity] * (2 * self.size)
        self.tree[self.size : self.size + self.n] = values  # 리프
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = op(self.tree[2 * i], self.tree[2 * i + 1])

    def get(self, index: int):
        return self.tree[self.size + index]

    def update(self, index: int, value) -> None:
        """a[index] = value 로 바꾸고 루트까지 올라가며 다시 계산한다."""
        i = self.size + index
        self.tree[i] = value
        i >>= 1
        while i:
            self.tree[i] = self.op(self.tree[2 * i], self.tree[2 * i + 1])
            i >>= 1

    def query(self, left: int, right: int):
        """op(a[left], …, a[right-1]). 빈 구간이면 항등원.

        두 경계를 위로 올리며, 경계가 '오른쪽 자식' 일 때만 그 노드를 결과에 포함한다. 왼쪽 경계에서 모은 것은 왼쪽 결과,
        오른쪽 경계에서 모은 것은 오른쪽 결과에 붙여 나중에 합치므로 교환 법칙이 필요 없다."""
        l = left + self.size
        r = right + self.size
        left_result = self.identity
        right_result = self.identity
        while l < r:
            if l & 1:
                left_result = self.op(left_result, self.tree[l])
                l += 1
            if r & 1:
                r -= 1
                right_result = self.op(self.tree[r], right_result)
            l >>= 1
            r >>= 1
        return self.op(left_result, right_result)

    def max_right(self, left: int, predicate: Callable[[object], bool]) -> int:
        """predicate(op(a[left .. r-1])) 가 참인 가장 큰 r (left ≤ r ≤ n). predicate(identity) 가 참이고, 구간이 길어질수록 참→거짓으로만 바뀌어야 한다.

        예: 최댓값 트리에서 predicate = (v < x) 이면 left 이후 처음으로 값이 x 이상인 위치(없으면 n)를 O(log n) 에 찾는다."""
        if left == self.n:
            return self.n
        l = left + self.size
        accumulated = self.identity
        while True:
            while l % 2 == 0:  # 왼쪽 자식이면 부모로 올라가 더 큰 구간을 한 번에 본다
                l >>= 1
            if not predicate(self.op(accumulated, self.tree[l])):
                while l < self.size:  # 이 노드 안에서 처음 거짓이 되는 곳까지 내려간다
                    l *= 2
                    if predicate(self.op(accumulated, self.tree[l])):
                        accumulated = self.op(accumulated, self.tree[l])
                        l += 1
                return l - self.size
            accumulated = self.op(accumulated, self.tree[l])
            l += 1
            if l & -l == l:  # 오른쪽 끝까지 다 봤다
                break
        return self.n


NEG_INF = float("-inf")


def _merge_max_subarray(a: tuple, b: tuple) -> tuple:
    """(합, 최대 접두사 합, 최대 접미사 합, 최대 연속 부분 합) 노드 두 개를 합친다. 교환 법칙이 성립하지 않는 연산의 대표 예."""
    total = a[0] + b[0]
    prefix = max(a[1], a[0] + b[1])
    suffix = max(b[2], b[0] + a[2])
    best = max(a[3], b[3], a[2] + b[1])
    return total, prefix, suffix, best


MAX_SUBARRAY_IDENTITY = (0, NEG_INF, NEG_INF, NEG_INF)


def max_subarray_tree(numbers: list[int]) -> SegmentTree:
    """구간의 최대 연속 부분 합(비어 있지 않은 연속 구간)을 query(l, r)[3] 으로 구하는 트리."""
    return SegmentTree([(x, x, x, x) for x in numbers], _merge_max_subarray, MAX_SUBARRAY_IDENTITY)


def range_gcd_tree(numbers: list[int]) -> SegmentTree:
    """구간 gcd 트리. gcd(0, x) = x 라서 항등원이 0 이다."""
    return SegmentTree(numbers, math.gcd, 0)


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    numbers = [int(x) for x in data[2 : 2 + n]]
    smallest = SegmentTree(numbers, min, float("inf"))
    largest = SegmentTree(numbers, max, float("-inf"))
    out = []
    pos = 2 + n
    for _ in range(m):
        a, b = int(data[pos]), int(data[pos + 1])
        pos += 2
        out.append(f"{smallest.query(a - 1, b)} {largest.query(a - 1, b)}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
