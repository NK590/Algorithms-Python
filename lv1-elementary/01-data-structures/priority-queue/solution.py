"""우선순위 큐와 힙 — 가장 우선순위가 높은(가장 작은) 값을 빠르게 꺼내는 자료구조

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- MinHeap 은 배열로 만든 이진 힙입니다. 0번 시작에서 i 번의 부모는 (i-1)//2, 자식은 2i+1, 2i+2 입니다.
- 실전에서는 heapq (최소 힙) 를 쓰고, 최대 힙은 값에 - 를 붙여 넣습니다.
- 직접 실행하면 `N` 과 N 개의 연산을 받아, 양수 x 는 넣고 0 은 가장 작은 값을 꺼내 출력합니다. (비어 있으면 0)
"""
import heapq
import sys


class MinHeap:
    def __init__(self, values=()):
        self._a = list(values)
        for i in range(len(self._a) // 2 - 1, -1, -1):  # 마지막 부모부터 내려 보내며 만들면 O(n)
            self._sift_down(i)

    def push(self, value) -> None:
        """맨 뒤에 넣고 부모보다 작으면 위로 올린다. O(log n)"""
        self._a.append(value)
        i = len(self._a) - 1
        while i > 0 and self._a[i] < self._a[(i - 1) // 2]:
            parent = (i - 1) // 2
            self._a[i], self._a[parent] = self._a[parent], self._a[i]
            i = parent

    def pop(self):
        """가장 작은 값(루트)을 꺼낸다. 맨 뒤 값을 루트로 옮기고 아래로 내려 보낸다. O(log n)"""
        if not self._a:
            raise IndexError("빈 힙입니다")
        top = self._a[0]
        last = self._a.pop()
        if self._a:
            self._a[0] = last
            self._sift_down(0)
        return top

    def peek(self):
        if not self._a:
            raise IndexError("빈 힙입니다")
        return self._a[0]

    def _sift_down(self, i: int) -> None:
        n = len(self._a)
        while True:
            child = 2 * i + 1
            if child >= n:
                return
            if child + 1 < n and self._a[child + 1] < self._a[child]:
                child += 1  # 두 자식 중 더 작은 쪽
            if self._a[i] <= self._a[child]:
                return
            self._a[i], self._a[child] = self._a[child], self._a[i]
            i = child

    def __len__(self) -> int:
        return len(self._a)


def heap_sorted(values) -> list:
    """힙에 모두 넣고 하나씩 꺼내면 오름차순이다. O(n log n)"""
    heap = MinHeap(values)
    return [heap.pop() for _ in range(len(heap))]


def kth_largest(values, k: int):
    """k번째로 큰 값. 크기 k 의 최소 힙만 유지한다. O(n log k)"""
    heap = MinHeap()
    for x in values:
        heap.push(x)
        if len(heap) > k:
            heap.pop()  # 가장 작은 값을 버리면 큰 k 개만 남는다
    return heap.peek()


def merge_sorted_lists(lists: list) -> list:
    """정렬된 리스트 K 개를 합친다. 각 리스트의 맨 앞 값만 힙에 두면 O(N log K)."""
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]
    heapq.heapify(heap)
    merged = []
    while heap:
        value, i, j = heapq.heappop(heap)
        merged.append(value)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    return merged


class RunningMedian:
    """값이 하나씩 들어올 때마다 중앙값(개수가 짝수이면 작은 쪽 가운데)을 O(log n) 에 구한다.

    작은 절반은 최대 힙(값에 - 를 붙인 최소 힙), 큰 절반은 최소 힙에 둔다. 두 힙의 크기 차이를 최대 1 로 유지한다.
    """

    def __init__(self):
        self._low = []   # 최대 힙 (음수로 저장)
        self._high = []  # 최소 힙

    def add(self, value) -> None:
        if not self._low or value <= -self._low[0]:
            heapq.heappush(self._low, -value)
        else:
            heapq.heappush(self._high, value)
        if len(self._low) > len(self._high) + 1:
            heapq.heappush(self._high, -heapq.heappop(self._low))
        elif len(self._high) > len(self._low):
            heapq.heappush(self._low, -heapq.heappop(self._high))

    def median(self):
        if not self._low:
            raise IndexError("값이 없습니다")
        return -self._low[0]


def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    heap = MinHeap()
    out = []
    for _ in range(n):
        x = int(input())
        if x > 0:
            heap.push(x)
        else:
            out.append(heap.pop() if len(heap) else 0)
    print("\n".join(map(str, out)))


if __name__ == "__main__":
    main()
