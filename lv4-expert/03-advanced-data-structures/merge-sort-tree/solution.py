"""머지 소트 트리(Merge Sort Tree) — 세그먼트 트리의 각 노드가 "자기 구간을 정렬한 목록" 을 가진다: 구간에서 x 보다 작은 원소 수·k 번째 수

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 일반 세그먼트 트리는 구간 "합" 처럼 합칠 수 있는 값만 담지만, 정렬된 목록은 두 자식의 목록을 병합해서 만든다 (병합 정렬의 병합 단계, 그래서 이름이 머지 소트 트리).
  구간 [l, r) 은 O(log n) 개의 노드로 쪼개지고, 각 노드의 정렬된 목록에서 bisect 로 "x 보다 작은 원소 수" 를 O(log n) 에 구하므로 질의 하나가 O(log² n).
- MergeSortTree: count_less / count_at_most / count_in_value_range / predecessor / successor / sum_less(노드마다 접두사 합을 둔다) / kth_smallest(값에 대한 이분 탐색 + 개수 세기, O(log³ n)).
  준비 O(n log n) 시간·메모리. update(i, value): 조상 O(log n) 개의 목록에서 옛 값을 지우고 새 값을 끼워 넣는다 (목록 이동이 필요해 O(n) 이지만 C 속도).
- 정적인 배열에서 온라인 질의가 많을 때 퍼시스턴트 세그먼트 트리·웨이블릿 트리가 더 빠르지만(O(log n)), 구현이 가장 단순하고 갱신도 된다.
- 직접 실행하면 BOJ 13544 형식 — `N`, 수열, `M`, 질의 `a b c` (직전 답 `last` 로 i = a xor last, j = b xor last, k = c xor last 를 복원; 1부터) — 를 받아 a[i..j] 에서 k 보다 큰 원소의 수를 출력합니다.
"""
import sys
from bisect import bisect_left, bisect_right, insort
from itertools import accumulate
from typing import Optional, Sequence


class MergeSortTree:
    def __init__(self, values: Sequence[int]):
        self.n = len(values)
        size = 1
        while size < max(1, self.n):
            size *= 2
        self.size = size
        self.tree: list[list[int]] = [[] for _ in range(2 * size)]
        for i, v in enumerate(values):
            self.tree[size + i] = [v]
        for i in range(size - 1, 0, -1):
            self.tree[i] = sorted(self.tree[2 * i] + self.tree[2 * i + 1])  # 이미 정렬된 두 목록의 병합 (Timsort 가 선형에 합친다)
        self.sorted_values = sorted(values)
        self._prefix: Optional[list[list[int]]] = None  # sum_less 를 처음 쓸 때 만든다

    def _nodes(self, left: int, right: int):
        """반열린 [left, right) 를 덮는 노드 번호들."""
        if not 0 <= left <= right <= self.n:
            raise IndexError("구간이 범위를 벗어났습니다")
        left += self.size
        right += self.size
        while left < right:
            if left & 1:
                yield left
                left += 1
            if right & 1:
                right -= 1
                yield right
            left //= 2
            right //= 2

    def count_less(self, left: int, right: int, x: int) -> int:
        """[left, right) 에서 x 보다 작은 원소의 수."""
        return sum(bisect_left(self.tree[node], x) for node in self._nodes(left, right))

    def count_at_most(self, left: int, right: int, x: int) -> int:
        return sum(bisect_right(self.tree[node], x) for node in self._nodes(left, right))

    def count_in_value_range(self, left: int, right: int, low: int, high: int) -> int:
        """[left, right) 에서 low ≤ 값 ≤ high 인 원소의 수 (low > high 면 0)."""
        if low > high:
            return 0
        return self.count_at_most(left, right, high) - self.count_less(left, right, low)

    def predecessor(self, left: int, right: int, x: int) -> Optional[int]:
        """[left, right) 에서 x 보다 작은 값 중 가장 큰 것 (없으면 None)."""
        best = None
        for node in self._nodes(left, right):
            index = bisect_left(self.tree[node], x)
            if index and (best is None or self.tree[node][index - 1] > best):
                best = self.tree[node][index - 1]
        return best

    def successor(self, left: int, right: int, x: int) -> Optional[int]:
        """[left, right) 에서 x 보다 큰 값 중 가장 작은 것 (없으면 None)."""
        best = None
        for node in self._nodes(left, right):
            index = bisect_right(self.tree[node], x)
            if index < len(self.tree[node]) and (best is None or self.tree[node][index] < best):
                best = self.tree[node][index]
        return best

    def kth_smallest(self, left: int, right: int, k: int) -> int:
        """[left, right) 에서 k 번째(1부터) 로 작은 값. 전체 값에 대한 이분 탐색."""
        if not 1 <= k <= right - left:
            raise ValueError("k 가 범위를 벗어났습니다")
        low, high = 0, len(self.sorted_values) - 1
        while low < high:  # count_at_most(값) ≥ k 인 가장 작은 값을 찾는다
            mid = (low + high) // 2
            if self.count_at_most(left, right, self.sorted_values[mid]) >= k:
                high = mid
            else:
                low = mid + 1
        return self.sorted_values[low]

    def sum_less(self, left: int, right: int, x: int) -> int:
        """[left, right) 에서 x 보다 작은 원소들의 합."""
        if self._prefix is None:
            self._prefix = [[0] + list(accumulate(lst)) for lst in self.tree]
        return sum(self._prefix[node][bisect_left(self.tree[node], x)] for node in self._nodes(left, right))

    def update(self, index: int, value: int) -> None:
        """a[index] = value. 조상의 정렬된 목록에서 옛 값을 지우고 새 값을 끼워 넣는다."""
        if not 0 <= index < self.n:
            raise IndexError("index 가 범위를 벗어났습니다")
        old = self.tree[self.size + index][0]
        node = self.size + index
        while node:
            lst = self.tree[node]
            del lst[bisect_left(lst, old)]
            insort(lst, value)
            node //= 2
        self._prefix = None
        position = bisect_left(self.sorted_values, old)
        del self.sorted_values[position]
        insort(self.sorted_values, value)


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    tree = MergeSortTree([int(x) for x in data[1 : 1 + n]])
    m = int(data[1 + n])
    last = 0
    out = []
    pos = 2 + n
    for _ in range(m):
        i = int(data[pos]) ^ last
        j = int(data[pos + 1]) ^ last
        k = int(data[pos + 2]) ^ last
        pos += 3
        last = (j - i + 1) - tree.count_at_most(i - 1, j, k)
        out.append(last)
    print("\n".join(map(str, out)))


if __name__ == "__main__":
    main()
