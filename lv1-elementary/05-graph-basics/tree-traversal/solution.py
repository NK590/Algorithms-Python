"""트리 순회 — 이진 트리의 모든 노드를 정해진 순서로 한 번씩 방문하기 (전위, 중위, 후위, 레벨 순서)

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 트리는 딕셔너리 `tree[노드] = (왼쪽 자식, 오른쪽 자식)` 이고, 자식이 없으면 None 입니다.
- 직접 실행하면 `N` 과 N 줄의 `노드 왼쪽 오른쪽` (없으면 `.`) 을 받아 전위·중위·후위 순회 결과를 한 줄씩 출력합니다. 루트는 `A` 입니다.
"""
import sys
from collections import deque


def preorder(tree: dict, root) -> list:
    """루트 → 왼쪽 → 오른쪽. 부모를 자식보다 먼저 방문한다."""
    if root is None:
        return []
    left, right = tree[root]
    return [root] + preorder(tree, left) + preorder(tree, right)


def inorder(tree: dict, root) -> list:
    """왼쪽 → 루트 → 오른쪽. 이진 탐색 트리에서는 값이 오름차순으로 나온다."""
    if root is None:
        return []
    left, right = tree[root]
    return inorder(tree, left) + [root] + inorder(tree, right)


def postorder(tree: dict, root) -> list:
    """왼쪽 → 오른쪽 → 루트. 자식을 모두 방문한 뒤에 부모를 방문한다."""
    if root is None:
        return []
    left, right = tree[root]
    return postorder(tree, left) + postorder(tree, right) + [root]


def inorder_iterative(tree: dict, root) -> list:
    """재귀 없이 스택으로 하는 중위 순회: 왼쪽 끝까지 내려가며 쌓고, 꺼내면서 오른쪽으로 간다."""
    result = []
    stack = []
    node = root
    while node is not None or stack:
        while node is not None:
            stack.append(node)
            node = tree[node][0]
        node = stack.pop()
        result.append(node)
        node = tree[node][1]
    return result


def level_order(tree: dict, root) -> list:
    """위에서 아래로, 같은 깊이에서는 왼쪽에서 오른쪽으로 (BFS)."""
    if root is None:
        return []
    result = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        result.append(node)
        for child in tree[node]:
            if child is not None:
                queue.append(child)
    return result


def build_from_preorder_inorder(pre: list, ino: list) -> tuple:
    """전위 순회와 중위 순회로 트리를 복원한다. 값은 모두 서로 달라야 한다. (tree, root) 반환."""
    position = {value: i for i, value in enumerate(ino)}
    tree = {}
    next_root = 0  # pre 에서 다음으로 루트가 될 값의 위치

    def build(lo: int, hi: int):
        nonlocal next_root
        if lo > hi:
            return None
        root = pre[next_root]
        next_root += 1
        mid = position[root]  # 중위 순회에서 루트의 위치 = 왼쪽/오른쪽 서브트리의 경계
        left = build(lo, mid - 1)
        right = build(mid + 1, hi)
        tree[root] = (left, right)
        return root

    root = build(0, len(ino) - 1)
    return tree, root


def build_from_postorder_inorder(post: list, ino: list) -> tuple:
    """후위 순회와 중위 순회로 트리를 복원한다. 후위의 마지막이 루트이므로 뒤에서부터 오른쪽 서브트리를 먼저 만든다."""
    position = {value: i for i, value in enumerate(ino)}
    tree = {}
    next_root = len(post) - 1

    def build(lo: int, hi: int):
        nonlocal next_root
        if lo > hi:
            return None
        root = post[next_root]
        next_root -= 1
        mid = position[root]
        right = build(mid + 1, hi)  # 후위를 뒤에서 읽으니 오른쪽이 먼저 나온다
        left = build(lo, mid - 1)
        tree[root] = (left, right)
        return root

    root = build(0, len(ino) - 1)
    return tree, root


def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    tree = {}
    for _ in range(n):
        node, left, right = input().split()
        tree[node] = (None if left == "." else left, None if right == "." else right)
    for order in (preorder, inorder, postorder):
        print("".join(order(tree, "A")))


if __name__ == "__main__":
    main()
