"""덱(Deque) — 양쪽 끝에서 넣고 뺄 수 있는 자료구조

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 스택(한쪽 끝)과 큐(넣는 쪽과 빼는 쪽이 다름)를 모두 흉내 낼 수 있습니다. 실전에서는 collections.deque 를 씁니다.
- Deque 는 원형 배열로 직접 만든 덱입니다. 가득 차면 두 배로 키웁니다.
- 직접 실행하면 `N` 과 N 개의 명령(push_front X, push_back X, pop_front, pop_back, size, empty, front, back)을 처리해 출력합니다.
  비어 있을 때 꺼내거나 보면 -1 입니다.
"""
import sys


class Deque:
    def __init__(self, capacity: int = 4):
        self._data = [None] * max(1, capacity)
        self._head = 0  # 맨 앞 원소의 위치
        self._size = 0

    def _grow(self) -> None:
        """가득 차면 두 배 크기의 배열로 옮긴다. 이때 머리를 0 번으로 되돌려 일렬로 펴 준다."""
        old = self._data
        self._data = [old[(self._head + i) % len(old)] for i in range(self._size)] + [None] * len(old)
        self._head = 0

    def push_back(self, value) -> None:
        if self._size == len(self._data):
            self._grow()
        self._data[(self._head + self._size) % len(self._data)] = value
        self._size += 1

    def push_front(self, value) -> None:
        if self._size == len(self._data):
            self._grow()
        self._head = (self._head - 1) % len(self._data)  # 머리를 한 칸 앞으로. 0 보다 작으면 배열 끝으로 돌아간다
        self._data[self._head] = value
        self._size += 1

    def pop_front(self):
        if self._size == 0:
            raise IndexError("빈 덱입니다")
        value = self._data[self._head]
        self._head = (self._head + 1) % len(self._data)
        self._size -= 1
        return value

    def pop_back(self):
        if self._size == 0:
            raise IndexError("빈 덱입니다")
        self._size -= 1
        return self._data[(self._head + self._size) % len(self._data)]

    def front(self):
        if self._size == 0:
            raise IndexError("빈 덱입니다")
        return self._data[self._head]

    def back(self):
        if self._size == 0:
            raise IndexError("빈 덱입니다")
        return self._data[(self._head + self._size - 1) % len(self._data)]

    def is_empty(self) -> bool:
        return self._size == 0

    def __len__(self) -> int:
        return self._size

    def to_list(self) -> list:
        return [self._data[(self._head + i) % len(self._data)] for i in range(self._size)]


def is_palindrome(text: str) -> bool:
    """양 끝에서 하나씩 꺼내 비교한다. 덱이 양쪽 끝 접근을 O(1) 에 해 주기 때문에 가능한 방법이다."""
    deque = Deque()
    for ch in text:
        deque.push_back(ch)
    while len(deque) > 1:
        if deque.pop_front() != deque.pop_back():
            return False
    return True


def process_commands(commands: list) -> list:
    """명령 문자열 리스트를 처리해, 출력해야 하는 값들을 문자열 리스트로 반환한다."""
    deque = Deque()
    output = []
    for command in commands:
        name, *args = command.split()
        if name == "push_front":
            deque.push_front(int(args[0]))
        elif name == "push_back":
            deque.push_back(int(args[0]))
        elif name == "pop_front":
            output.append(str(deque.pop_front() if not deque.is_empty() else -1))
        elif name == "pop_back":
            output.append(str(deque.pop_back() if not deque.is_empty() else -1))
        elif name == "size":
            output.append(str(len(deque)))
        elif name == "empty":
            output.append("1" if deque.is_empty() else "0")
        elif name == "front":
            output.append(str(deque.front() if not deque.is_empty() else -1))
        elif name == "back":
            output.append(str(deque.back() if not deque.is_empty() else -1))
    return output


def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    print("\n".join(process_commands([input() for _ in range(n)])))


if __name__ == "__main__":
    main()
