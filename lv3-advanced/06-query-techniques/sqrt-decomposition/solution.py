"""제곱근 분할(Sqrt Decomposition) — 배열을 크기 √n 정도의 블록으로 나눠, 질의를 "온전한 블록들 + 양 끝의 조각" 으로 처리하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 온전히 덮이는 블록은 블록마다 미리 계산해 둔 값(합, 정렬된 복사본, …) 으로 O(1) 또는 O(log B) 에, 양 끝에 걸친 조각은 원소를 하나씩 O(B) 에 처리합니다.
  블록이 n/B 개, 한 블록이 B 개이므로 B = √n 이면 질의당 O(√n).
- SqrtSum: 구간에 값 더하기 + 구간 합. 블록마다 "블록 전체에 더해진 값(lazy)" 과 블록 합을 따로 둡니다.
  (세그먼트 트리의 지연 전파와 같은 생각이지만 구현이 훨씬 단순하고, 합 대신 "정렬된 복사본" 처럼 세그먼트 트리로 합치기 어려운 정보도 블록에 담을 수 있습니다.)
- SqrtCountGreater: 한 원소 바꾸기 + 구간에서 k 보다 큰 원소의 수. 블록마다 정렬된 복사본을 두고 이진 탐색으로 셉니다.
- 구간은 반열린 [l, r) (0 부터).
- 직접 실행하면 구간 빈도 갱신 예제 형식 — `N`, 수열, `M`, 질의(`1 i v`: A[i] = v, `2 l r k`: A[l..r] 중 k 보다 큰 원소의 수, 모두 1 부터·양 끝 포함) — 을 처리해 2 번 질의의 답을 출력합니다.
"""
import sys
from bisect import bisect_left, bisect_right, insort
from math import isqrt
from typing import Sequence


def default_block_size(n: int) -> int:
    return max(1, isqrt(n))


class SqrtSum:
    """구간 더하기·구간 합. 모든 연산 O(√n)."""

    def __init__(self, a: Sequence[int], block: int | None = None):
        self.n = len(a)
        self.block = block or default_block_size(self.n)
        self.a = list(a)  # 블록의 lazy 는 반영되지 않은 원래 값
        count = (self.n + self.block - 1) // self.block
        self.lazy = [0] * count  # 블록의 모든 원소에 (아직 a 에 안 더하고) 더해 둔 값
        self.total = [sum(self.a[b * self.block : (b + 1) * self.block]) for b in range(count)]  # lazy 까지 반영한 블록 합

    def _check(self, left: int, right: int) -> None:
        if not 0 <= left <= right <= self.n:
            raise ValueError("구간이 범위를 벗어났습니다")

    def add(self, left: int, right: int, value: int) -> None:
        """a[left:right] 의 모든 원소에 value 를 더한다."""
        self._check(left, right)
        if left == right:
            return
        block = self.block
        first, last = left // block, (right - 1) // block
        if first == last:
            for i in range(left, right):
                self.a[i] += value
            self.total[first] += value * (right - left)
            return
        for i in range(left, (first + 1) * block):  # 왼쪽 조각
            self.a[i] += value
        self.total[first] += value * ((first + 1) * block - left)
        for b in range(first + 1, last):  # 온전한 블록들: lazy 만 갱신
            self.lazy[b] += value
            self.total[b] += value * block
        for i in range(last * block, right):  # 오른쪽 조각
            self.a[i] += value
        self.total[last] += value * (right - last * block)

    def sum(self, left: int, right: int) -> int:
        """a[left:right] 의 합."""
        self._check(left, right)
        if left == right:
            return 0
        block = self.block
        first, last = left // block, (right - 1) // block
        if first == last:
            return sum(self.a[left:right]) + self.lazy[first] * (right - left)
        result = sum(self.a[left : (first + 1) * block]) + self.lazy[first] * ((first + 1) * block - left)
        result += sum(self.total[first + 1 : last])
        result += sum(self.a[last * block : right]) + self.lazy[last] * (right - last * block)
        return result

    def get(self, i: int) -> int:
        return self.a[i] + self.lazy[i // self.block]


class SqrtCountGreater:
    """한 원소 바꾸기·구간에서 k 보다 큰 원소 세기. 갱신 O(√n), 질의 O(√n + (n/B)·log B)."""

    def __init__(self, a: Sequence[int], block: int | None = None):
        self.n = len(a)
        self.block = block or default_block_size(self.n)
        self.a = list(a)
        count = (self.n + self.block - 1) // self.block
        self.sorted_blocks = [sorted(self.a[b * self.block : (b + 1) * self.block]) for b in range(count)]

    def update(self, i: int, value: int) -> None:
        """a[i] = value."""
        blk = self.sorted_blocks[i // self.block]
        del blk[bisect_left(blk, self.a[i])]  # 옛 값을 정렬된 복사본에서 지우고
        insort(blk, value)  # 새 값을 제자리에 넣는다
        self.a[i] = value

    def count_greater(self, left: int, right: int, k: int) -> int:
        """a[left:right] 중 k 보다 큰 원소의 수."""
        if not 0 <= left <= right <= self.n:
            raise ValueError("구간이 범위를 벗어났습니다")
        if left == right:
            return 0
        block = self.block
        first, last = left // block, (right - 1) // block
        if first == last:
            return sum(1 for i in range(left, right) if self.a[i] > k)
        result = sum(1 for i in range(left, (first + 1) * block) if self.a[i] > k)
        for b in range(first + 1, last):
            blk = self.sorted_blocks[b]
            result += len(blk) - bisect_right(blk, k)
        result += sum(1 for i in range(last * block, right) if self.a[i] > k)
        return result


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    structure = SqrtCountGreater([int(x) for x in data[1 : 1 + n]])
    m = int(data[1 + n])
    pos = 2 + n
    out = []
    for _ in range(m):
        if data[pos] == b"1":
            structure.update(int(data[pos + 1]) - 1, int(data[pos + 2]))
            pos += 3
        else:
            out.append(structure.count_greater(int(data[pos + 1]) - 1, int(data[pos + 2]), int(data[pos + 3])))
            pos += 4
    print("\n".join(map(str, out)))


if __name__ == "__main__":
    main()
