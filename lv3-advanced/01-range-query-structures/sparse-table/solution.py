"""희소 배열(Sparse Table) — 값이 바뀌지 않는 배열에서 구간 최솟값·최댓값·gcd 를 O(1) 에 답하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- table[k][i] = 구간 [i, i + 2^k) 의 결과. table[k] 는 table[k-1] 의 두 칸을 합쳐 만들어 O(n log n) 에 전체를 구축합니다.
- 질의 [left, right) 는 길이가 2^k 이하인 가장 큰 k 를 골라, 겹치는 두 구간 [left, left + 2^k) 와 [right - 2^k, right) 의 결과를 합치면 끝입니다.
  겹쳐서 두 번 세어도 결과가 변하지 않는 연산(멱등: min, max, gcd, and, or)에서만 쓸 수 있습니다. 합은 안 됩니다.
- 합이나 곱처럼 멱등이 아닌 연산은 DisjointSparseTable 로 O(1) 에 답합니다 (구간이 겹치지 않게 가운데를 기준으로 쪼갠다).
- 구간은 0 부터 시작하는 반열린 [left, right) 입니다.
- 직접 실행하면 `N M`, N 개의 수, 질의 M 개(`a b`: a 번째부터 b 번째까지, 1 부터)를 받아 각 구간의 최솟값을 출력합니다.
"""
import sys
from math import gcd
from typing import Callable


class SparseTable:
    """멱등 연산 func (기본 min) 의 구간 질의. 구축 O(n log n), 질의 O(1), 갱신은 지원하지 않는다."""

    def __init__(self, values: list, func: Callable = min):
        self.func = func
        self.n = len(values)
        self.table = [list(values)]
        k = 1
        while (1 << k) <= self.n:
            previous = self.table[-1]
            half = 1 << (k - 1)
            self.table.append([func(previous[i], previous[i + half]) for i in range(self.n - (1 << k) + 1)])
            k += 1

    def query(self, left: int, right: int):
        """func(a[left], …, a[right-1]). 비어 있지 않은 구간만 허용한다."""
        if not 0 <= left < right <= self.n:
            raise ValueError("비어 있지 않은 구간 [left, right) 가 필요합니다")
        k = (right - left).bit_length() - 1  # 2^k ≤ 길이 < 2^(k+1)
        return self.func(self.table[k][left], self.table[k][right - (1 << k)])


class RangeArgmin:
    """구간 최솟값의 '위치'. 값이 같으면 가장 왼쪽. (값, 위치) 쌍의 최솟값을 구하는 것과 같다."""

    def __init__(self, values: list):
        self.values = values
        self.table = SparseTable([(v, i) for i, v in enumerate(values)])

    def query(self, left: int, right: int) -> int:
        return self.table.query(left, right)[1]


def range_gcd_table(values: list[int]) -> SparseTable:
    """구간 gcd. gcd 는 멱등이다 (gcd(x, x) = x)."""
    return SparseTable(values, gcd)


class DisjointSparseTable:
    """결합 법칙만 성립하면 되는 연산 op (합, 곱, 문자열 이어 붙이기 …) 의 구간 질의를 O(1) 에 답한다. 구축 O(n log n).

    수준 h 에서는 배열을 길이 2^(h+1) 의 블록으로 나누고, 각 블록의 가운데 mid 에서 왼쪽 절반은 왼쪽으로, 오른쪽 절반은 오른쪽으로 뻗는
    접두사(접미사) 결과를 저장한다. 질의 [l, r] 의 두 끝이 처음으로 갈라지는 비트가 h 이면 l 과 r 은 수준 h 블록의 가운데를 사이에 두고 있으므로
    op(왼쪽 조각, 오른쪽 조각) 한 번이면 된다."""

    def __init__(self, values: list, op: Callable):
        self.op = op
        self.n = len(values)
        self.values = list(values)
        size = 2
        while size < self.n:
            size *= 2
        self.levels = size.bit_length() - 1
        padded = self.values + [self.values[-1]] * (size - self.n) if self.n else []
        self.table: list[list] = []
        for h in range(self.levels if self.n else 0):
            half = 1 << h
            level = list(padded)
            for start in range(0, size, 2 * half):
                mid = start + half
                level[mid - 1] = padded[mid - 1]
                for i in range(mid - 2, start - 1, -1):
                    level[i] = op(padded[i], level[i + 1])  # i 부터 mid - 1 까지
                level[mid] = padded[mid]
                for i in range(mid + 1, start + 2 * half):
                    level[i] = op(level[i - 1], padded[i])  # mid 부터 i 까지
            self.table.append(level)

    def query(self, left: int, right: int):
        """op(a[left], …, a[right-1]). 비어 있지 않은 구간만 허용한다."""
        if not 0 <= left < right <= self.n:
            raise ValueError("비어 있지 않은 구간 [left, right) 가 필요합니다")
        last = right - 1
        if left == last:
            return self.values[left]
        h = (left ^ last).bit_length() - 1
        return self.op(self.table[h][left], self.table[h][last])


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    table = SparseTable([int(x) for x in data[2 : 2 + n]])
    out = []
    pos = 2 + n
    for _ in range(m):
        a, b = int(data[pos]), int(data[pos + 1])
        pos += 2
        out.append(table.query(a - 1, b))
    print("\n".join(map(str, out)))


if __name__ == "__main__":
    main()
