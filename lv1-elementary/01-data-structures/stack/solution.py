"""스택 — 나중에 넣은 것을 먼저 꺼내는(LIFO) 자료구조

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 파이썬에서는 list 의 append / pop 이 곧 스택의 push / pop 입니다. 여기서는 연산을 분명히 보이려고 감쌌습니다.
- 직접 실행하면 첫 줄에 T, 다음 T줄에 괄호 문자열을 받아 올바른 괄호면 YES, 아니면 NO 를 출력합니다.
"""
import sys


class Stack:
    def __init__(self):
        self._items = []

    def push(self, value) -> None:
        """맨 위에 넣는다. O(1)"""
        self._items.append(value)

    def pop(self):
        """맨 위의 값을 꺼낸다. 비어 있으면 IndexError. O(1)"""
        if not self._items:
            raise IndexError("빈 스택에서 pop 했습니다")
        return self._items.pop()

    def peek(self):
        """맨 위의 값을 꺼내지 않고 본다. O(1)"""
        if not self._items:
            raise IndexError("빈 스택입니다")
        return self._items[-1]

    def is_empty(self) -> bool:
        return not self._items

    def __len__(self) -> int:
        return len(self._items)


def is_balanced(text: str) -> bool:
    """(), [], {} 가 올바르게 짝지어졌는지. 여는 괄호는 쌓고, 닫는 괄호는 가장 최근의 여는 괄호와 맞는지 확인한다."""
    pair = {")": "(", "]": "[", "}": "{"}
    stack = Stack()
    for ch in text:
        if ch in "([{":
            stack.push(ch)
        elif ch in pair:
            if stack.is_empty() or stack.pop() != pair[ch]:
                return False
    return stack.is_empty()  # 끝났는데 여는 괄호가 남아 있으면 짝이 없는 것이다


def evaluate_postfix(tokens: list) -> int:
    """후위 표기식(예: ['3', '4', '+', '2', '*'] = (3+4)*2)을 계산한다. +, -, * 를 지원한다."""
    stack = Stack()
    for token in tokens:
        if token in ("+", "-", "*"):
            right = stack.pop()  # 나중에 쌓인 것이 오른쪽 피연산자다
            left = stack.pop()
            stack.push(left + right if token == "+" else left - right if token == "-" else left * right)
        else:
            stack.push(int(token))
    return stack.pop()


def reverse_with_stack(text: str) -> str:
    """문자열을 스택에 모두 쌓았다가 꺼내면 뒤집힌다."""
    stack = Stack()
    for ch in text:
        stack.push(ch)
    result = []
    while not stack.is_empty():
        result.append(stack.pop())
    return "".join(result)


def main() -> None:
    input = sys.stdin.readline
    t = int(input())
    print("\n".join("YES" if is_balanced(input().strip()) else "NO" for _ in range(t)))


if __name__ == "__main__":
    main()
