"""연결 리스트 — 노드들이 "다음 노드를 가리키는 링크"로 줄줄이 이어진 자료구조

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 노드마다 값(value)과 다음 노드(next)를 가집니다. 중간 삽입·삭제는 링크만 바꾸면 되지만, i 번째를 찾으려면 처음부터 따라가야 합니다.
- 직접 실행하면 `N` 과 N 개의 정수를 받아 순서를 뒤집어 한 줄에 출력합니다.
"""
import sys


class Node:
    __slots__ = ("value", "next")

    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class LinkedList:
    def __init__(self, values=()):
        self.head = None
        self._size = 0
        for value in values:
            self.append(value)

    def prepend(self, value) -> None:
        """맨 앞에 넣는다. O(1)"""
        self.head = Node(value, self.head)
        self._size += 1

    def append(self, value) -> None:
        """맨 뒤에 넣는다. 끝을 찾으러 처음부터 따라가야 하므로 O(n). (꼬리 포인터를 두면 O(1))"""
        node = Node(value)
        if self.head is None:
            self.head = node
        else:
            tail = self.head
            while tail.next is not None:
                tail = tail.next
            tail.next = node
        self._size += 1

    def find(self, value):
        """값이 같은 첫 노드. 없으면 None. O(n)"""
        node = self.head
        while node is not None and node.value != value:
            node = node.next
        return node

    def insert_after(self, node: Node, value) -> None:
        """이미 찾아 둔 node 바로 뒤에 넣는다. 링크 두 개만 바꾸므로 O(1)."""
        node.next = Node(value, node.next)
        self._size += 1

    def remove(self, value) -> bool:
        """값이 같은 첫 노드를 지운다. 지웠으면 True. 앞 노드의 링크를 건너뛰게 바꾼다."""
        previous, node = None, self.head
        while node is not None and node.value != value:
            previous, node = node, node.next
        if node is None:
            return False
        if previous is None:
            self.head = node.next  # 맨 앞 노드를 지우는 경우
        else:
            previous.next = node.next
        self._size -= 1
        return True

    def reverse(self) -> None:
        """링크의 방향을 모두 뒤집는다. 노드를 하나씩 따라가며 next 를 앞 노드로 바꾼다. O(n)"""
        previous, node = None, self.head
        while node is not None:
            node.next, previous, node = previous, node, node.next  # 오른쪽 식이 모두 계산된 뒤에 한꺼번에 대입된다
        self.head = previous

    def middle(self):
        """가운데 노드의 값 (짝수 개이면 뒤쪽 가운데). 한 칸씩 가는 포인터와 두 칸씩 가는 포인터를 함께 쓴다."""
        if self.head is None:
            raise IndexError("빈 리스트입니다")
        slow = fast = self.head
        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next
        return slow.value

    def to_list(self) -> list:
        result = []
        node = self.head
        while node is not None:
            result.append(node.value)
            node = node.next
        return result

    def __len__(self) -> int:
        return self._size


def has_cycle(head) -> bool:
    """플로이드의 토끼와 거북이: 한 칸씩/두 칸씩 가는 포인터가 만나면 사이클이 있다. 추가 메모리 O(1)."""
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


def merge_sorted(a: LinkedList, b: LinkedList) -> LinkedList:
    """정렬된 두 연결 리스트를 합친 새 연결 리스트. 앞에서부터 작은 쪽을 이어 붙인다."""
    merged = LinkedList()
    x, y = a.head, b.head
    values = []
    while x is not None and y is not None:
        if x.value <= y.value:
            values.append(x.value)
            x = x.next
        else:
            values.append(y.value)
            y = y.next
    while x is not None:
        values.append(x.value)
        x = x.next
    while y is not None:
        values.append(y.value)
        y = y.next
    for value in values:
        merged.append(value)
    return merged


def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    values = list(map(int, input().split()))[:n]
    linked = LinkedList(values)
    linked.reverse()
    print(*linked.to_list())


if __name__ == "__main__":
    main()
