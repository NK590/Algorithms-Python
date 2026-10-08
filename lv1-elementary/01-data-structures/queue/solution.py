"""큐 — 먼저 넣은 것을 먼저 꺼내는(FIFO) 자료구조

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 실전에서는 collections.deque 를 큐로 씁니다. (list.pop(0) 은 O(n) 이라 쓰면 안 됩니다)
- Queue 는 deque 로, TwoStackQueue 는 스택 두 개로, CircularQueue 는 고정 크기 배열로 만든 큐입니다.
- 직접 실행하면 N 을 받아, 1..N 카드에서 "맨 위 카드를 버리고 그다음 카드를 맨 아래로" 를 반복해 마지막에 남는 카드를 출력합니다.
"""
import sys
from collections import deque


class Queue:
    def __init__(self):
        self._items = deque()

    def enqueue(self, value) -> None:
        """뒤에 넣는다. O(1)"""
        self._items.append(value)

    def dequeue(self):
        """앞에서 꺼낸다. 비어 있으면 IndexError. O(1)"""
        if not self._items:
            raise IndexError("빈 큐에서 꺼냈습니다")
        return self._items.popleft()

    def front(self):
        if not self._items:
            raise IndexError("빈 큐입니다")
        return self._items[0]

    def is_empty(self) -> bool:
        return not self._items

    def __len__(self) -> int:
        return len(self._items)


class TwoStackQueue:
    """스택(리스트) 두 개로 만든 큐. 넣을 때는 in 스택에, 꺼낼 때는 out 스택에서. out 이 비면 in 을 통째로 옮겨 뒤집는다.

    한 원소는 많아야 한 번 옮겨지므로 연산당 평균(분할 상환) O(1) 이다.
    """

    def __init__(self):
        self._in = []
        self._out = []

    def enqueue(self, value) -> None:
        self._in.append(value)

    def _refill(self) -> None:
        if not self._out:
            while self._in:
                self._out.append(self._in.pop())  # in 의 가장 위(가장 최근)가 out 의 가장 아래로 간다

    def dequeue(self):
        self._refill()
        if not self._out:
            raise IndexError("빈 큐에서 꺼냈습니다")
        return self._out.pop()

    def front(self):
        self._refill()
        if not self._out:
            raise IndexError("빈 큐입니다")
        return self._out[-1]

    def __len__(self) -> int:
        return len(self._in) + len(self._out)


class CircularQueue:
    """크기가 고정된 배열을 원형으로 쓰는 큐. 머리(head)와 크기만 기억하면 꼬리 위치는 (head + size) % capacity 이다."""

    def __init__(self, capacity: int):
        self._data = [None] * capacity
        self._head = 0
        self._size = 0

    def enqueue(self, value) -> bool:
        """가득 찼으면 False, 아니면 넣고 True."""
        if self._size == len(self._data):
            return False
        self._data[(self._head + self._size) % len(self._data)] = value
        self._size += 1
        return True

    def dequeue(self):
        if self._size == 0:
            raise IndexError("빈 큐에서 꺼냈습니다")
        value = self._data[self._head]
        self._head = (self._head + 1) % len(self._data)  # 머리를 한 칸 옮기고, 배열 끝을 넘으면 처음으로 돌아간다
        self._size -= 1
        return value

    def __len__(self) -> int:
        return self._size


def last_card(n: int) -> int:
    """1..n 카드에서 '맨 위를 버리고, 그다음 카드를 맨 아래로'를 한 장 남을 때까지 반복했을 때 남는 카드."""
    queue = Queue()
    for card in range(1, n + 1):
        queue.enqueue(card)
    while len(queue) > 1:
        queue.dequeue()
        queue.enqueue(queue.dequeue())
    return queue.front()


def last_card_formula(n: int) -> int:
    """n 이 2 의 거듭제곱이면 n, 아니면 2 × (n − 가장 큰 2 의 거듭제곱 ≤ n)."""
    power = 1 << (n.bit_length() - 1)
    return n if n == power else 2 * (n - power)


def main() -> None:
    print(last_card(int(sys.stdin.readline())))


if __name__ == "__main__":
    main()
