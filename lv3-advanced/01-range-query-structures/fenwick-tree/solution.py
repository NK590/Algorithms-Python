"""펜윅 트리(Fenwick Tree, Binary Indexed Tree) — 점 갱신과 접두사 합을 O(log n) 에 처리하는 짧고 빠른 자료구조

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 인덱스의 이진 표현을 이용해 tree[i] 가 "i 에서 끝나는 길이 lowbit(i) 구간의 합" 이 되게 합니다. lowbit(i) = i & -i.
- 이 파일의 모든 클래스는 0 부터 시작하고, 구간은 반열린 [left, right) 입니다. 안쪽의 tree 배열만 1 부터 씁니다.
- 구성: 기본 FenwickTree(점 갱신·구간 합·k 번째 찾기), RangeAddFenwick(구간 더하기·구간 합, 트리 두 개),
  Fenwick2D(2 차원 점 갱신·직사각형 합), 응용(역순쌍 개수, 뒤에 있는 더 작은 수의 개수).
- 직접 실행하면 `N M K`, N 개의 수, 그리고 M + K 개의 질의(`1 b c`: b 번째 수를 c 로 바꾸기, `2 b c`: b 번째부터 c 번째까지의 합)를 받아
  합 질의의 결과를 한 줄씩 출력합니다.
"""
import sys
from bisect import bisect_left


class FenwickTree:
    """크기 size 의 배열에 대한 점 갱신·접두사 합. 값은 0 으로 시작한다."""

    def __init__(self, size: int):
        self.n = size
        self.tree = [0] * (size + 1)

    @classmethod
    def from_list(cls, values: list[int]) -> "FenwickTree":
        """O(n) 에 만든다 (하나씩 add 하면 O(n log n)). 각 칸의 값을 자기를 포함하는 바로 위 칸(i + lowbit(i))에 한 번만 밀어 올린다."""
        fenwick = cls(len(values))
        tree = fenwick.tree
        for i, v in enumerate(values, 1):
            tree[i] += v
            parent = i + (i & -i)
            if parent <= fenwick.n:
                tree[parent] += tree[i]
        return fenwick

    def add(self, index: int, delta: int) -> None:
        """a[index] += delta."""
        i = index + 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def prefix_sum(self, count: int) -> int:
        """앞의 count 개의 합 a[0] + … + a[count-1]."""
        total = 0
        i = count
        while i > 0:
            total += self.tree[i]
            i -= i & -i
        return total

    def range_sum(self, left: int, right: int) -> int:
        """a[left] + … + a[right-1]."""
        return self.prefix_sum(right) - self.prefix_sum(left)

    def point_value(self, index: int) -> int:
        return self.range_sum(index, index + 1)

    def set(self, index: int, value: int) -> None:
        self.add(index, value - self.point_value(index))

    def find_kth(self, k: int) -> int:
        """접두사 합이 처음으로 k 이상이 되는 위치(0 부터). 모든 값이 0 이상일 때만 의미가 있다(개수를 센 트리). 전체 합이 k 보다 작으면 n.

        가장 큰 2 의 거듭제곱 간격부터 '건너뛰어도 아직 k 에 모자란가' 를 확인하며 내려간다. O(log n)."""
        position = 0
        step = 1 << self.n.bit_length()
        while step:
            nxt = position + step
            if nxt <= self.n and self.tree[nxt] < k:
                position = nxt
                k -= self.tree[nxt]
            step >>= 1
        return position


class RangeAddFenwick:
    """구간 더하기 + 구간 합. 차분 배열 d 에 대해 앞의 x 개의 합이 x·Σd[j] − Σ(d[j]·j) 임을 이용해 트리 두 개로 관리한다."""

    def __init__(self, size: int):
        self.n = size
        self.coefficient = FenwickTree(size)  # d[j]
        self.weighted = FenwickTree(size)  # d[j] · j

    def range_add(self, left: int, right: int, delta: int) -> None:
        """a[left .. right-1] 에 delta 를 더한다."""
        self.coefficient.add(left, delta)
        self.weighted.add(left, delta * left)
        if right < self.n:
            self.coefficient.add(right, -delta)
            self.weighted.add(right, -delta * right)

    def prefix_sum(self, count: int) -> int:
        return count * self.coefficient.prefix_sum(count) - self.weighted.prefix_sum(count)

    def range_sum(self, left: int, right: int) -> int:
        return self.prefix_sum(right) - self.prefix_sum(left)


class Fenwick2D:
    """rows × cols 격자의 점 갱신과 직사각형 합. 행과 열에 모두 같은 lowbit 이동을 적용한다. 갱신·질의 O(log rows · log cols)."""

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.tree = [[0] * (cols + 1) for _ in range(rows + 1)]

    def add(self, row: int, col: int, delta: int) -> None:
        i = row + 1
        while i <= self.rows:
            line = self.tree[i]
            j = col + 1
            while j <= self.cols:
                line[j] += delta
                j += j & -j
            i += i & -i

    def prefix_sum(self, rows: int, cols: int) -> int:
        """위쪽 rows 행, 왼쪽 cols 열 직사각형 [0, rows) × [0, cols) 의 합."""
        total = 0
        i = rows
        while i > 0:
            line = self.tree[i]
            j = cols
            while j > 0:
                total += line[j]
                j -= j & -j
            i -= i & -i
        return total

    def rect_sum(self, row1: int, col1: int, row2: int, col2: int) -> int:
        """[row1, row2) × [col1, col2) 의 합 (포함·배제)."""
        return (
            self.prefix_sum(row2, col2)
            - self.prefix_sum(row1, col2)
            - self.prefix_sum(row2, col1)
            + self.prefix_sum(row1, col1)
        )


def count_inversions(numbers: list[int]) -> int:
    """역순쌍의 수: i < j 이고 numbers[i] > numbers[j] 인 쌍. 값을 순위로 압축한 뒤, 앞에서부터 보며 '이미 본 것 중 나보다 큰 것의 수' 를 더한다."""
    ordered = sorted(set(numbers))
    fenwick = FenwickTree(len(ordered))
    total = 0
    for seen, x in enumerate(numbers):
        rank = bisect_left(ordered, x)
        total += seen - fenwick.prefix_sum(rank + 1)  # 지금까지 본 seen 개 중 x 이하인 것을 뺀다
        fenwick.add(rank, 1)
    return total


def count_smaller_after(numbers: list[int]) -> list[int]:
    """result[i] = i 보다 뒤에 있으면서 numbers[i] 보다 작은 원소의 수. 뒤에서부터 보며 센다."""
    ordered = sorted(set(numbers))
    fenwick = FenwickTree(len(ordered))
    result = [0] * len(numbers)
    for i in range(len(numbers) - 1, -1, -1):
        rank = bisect_left(ordered, numbers[i])
        result[i] = fenwick.prefix_sum(rank)  # 순위가 rank 미만인 것의 수
        fenwick.add(rank, 1)
    return result


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m, k = int(data[0]), int(data[1]), int(data[2])
    fenwick = FenwickTree.from_list([int(x) for x in data[3 : 3 + n]])
    out = []
    pos = 3 + n
    for _ in range(m + k):
        a, b, c = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])
        pos += 3
        if a == 1:
            fenwick.set(b - 1, c)
        else:
            out.append(fenwick.range_sum(b - 1, c))
    print("\n".join(map(str, out)))


if __name__ == "__main__":
    main()
