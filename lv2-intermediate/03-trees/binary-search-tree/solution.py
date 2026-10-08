"""이진 탐색 트리(BST) — 왼쪽 자손은 모두 작고 오른쪽 자손은 모두 큰 이진 트리

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 모든 노드에서 (왼쪽 서브트리의 키) < 키 < (오른쪽 서브트리의 키). 그래서 중위 순회하면 정렬된 순서가 나옵니다.
- 같은 키는 한 번만 저장하는 집합입니다. 노드마다 서브트리의 크기(size)를 관리해 k 번째로 작은 수, 순위를 O(높이) 에 구합니다.
- 균형을 잡지 않으므로 정렬된 순서로 넣으면 높이가 n 인 사슬이 되어 모든 연산이 O(n) 입니다. (균형 트리는 이 저장소의 범위 밖)
- 깊은 트리에서도 재귀 한도에 걸리지 않도록 반복문으로 구현했습니다.
- 직접 실행하면 전위 순회 결과(트리에 키를 넣는 순서)를 받아 후위 순회 결과를 출력합니다. 입력은 한 줄에 키 하나, 빈 줄이나 입력 끝까지.
"""
import sys


class Node:
    __slots__ = ("key", "left", "right", "size")

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.size = 1  # 자기 자신을 포함한 서브트리의 노드 수


class BST:
    def __init__(self):
        self.root = None

    def __len__(self):
        return self.root.size if self.root else 0

    def __contains__(self, key):
        node = self.root
        while node:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def insert(self, key) -> bool:
        """키를 넣는다. 이미 있으면 아무것도 하지 않고 False."""
        if key in self:
            return False
        new = Node(key)
        if self.root is None:
            self.root = new
            return True
        node = self.root
        while True:
            node.size += 1  # 이 서브트리에 노드가 하나 늘어난다
            if key < node.key:
                if node.left is None:
                    node.left = new
                    return True
                node = node.left
            else:
                if node.right is None:
                    node.right = new
                    return True
                node = node.right

    def delete(self, key) -> bool:
        """키를 지운다. 없으면 False.

        ① 자식이 없으면 그냥 떼어 낸다 ② 자식이 하나면 그 자식으로 대체한다
        ③ 자식이 둘이면 오른쪽 서브트리의 최솟값(후속자)의 키를 가져오고, 그 후속자 노드를 지운다."""
        path = []  # 루트에서 지울 노드까지(지울 노드는 제외) 지나온 노드들
        node = self.root
        while node and node.key != key:
            path.append(node)
            node = node.left if key < node.key else node.right
        if node is None:
            return False
        if node.left and node.right:
            path.append(node)  # 이 노드는 남고 키만 바뀐다
            successor = node.right
            while successor.left:
                path.append(successor)
                successor = successor.left
            node.key = successor.key
            node = successor  # 실제로 떼어 낼 노드: 왼쪽 자식이 없다
        child = node.left or node.right
        if not path:
            self.root = child
        else:
            parent = path[-1]
            if parent.left is node:
                parent.left = child
            else:
                parent.right = child
        for p in path:  # 지나온 모든 노드의 서브트리가 하나씩 줄어든다
            p.size -= 1
        return True

    def minimum(self):
        node = self.root
        if node is None:
            return None
        while node.left:
            node = node.left
        return node.key

    def maximum(self):
        node = self.root
        if node is None:
            return None
        while node.right:
            node = node.right
        return node.key

    def inorder(self) -> list:
        """중위 순회 = 키를 오름차순으로. 스택을 직접 써서 재귀를 피한다."""
        result, stack, node = [], [], self.root
        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            result.append(node.key)
            node = node.right
        return result

    def height(self) -> int:
        """루트만 있으면 1, 빈 트리는 0."""
        if self.root is None:
            return 0
        best, stack = 0, [(self.root, 1)]
        while stack:
            node, depth = stack.pop()
            best = max(best, depth)
            if node.left:
                stack.append((node.left, depth + 1))
            if node.right:
                stack.append((node.right, depth + 1))
        return best

    def kth_smallest(self, k: int):
        """k 번째(1 부터)로 작은 키. 범위를 벗어나면 None. 왼쪽 서브트리의 크기와 k 를 비교하며 내려간다."""
        if not 1 <= k <= len(self):
            return None
        node = self.root
        while True:
            left_size = node.left.size if node.left else 0
            if k == left_size + 1:
                return node.key
            if k <= left_size:
                node = node.left
            else:
                k -= left_size + 1
                node = node.right

    def rank(self, key) -> int:
        """key 보다 작은 키의 개수."""
        count, node = 0, self.root
        while node:
            if key <= node.key:
                node = node.left
            else:
                count += (node.left.size if node.left else 0) + 1
                node = node.right
        return count

    def floor(self, x):
        """x 이하인 가장 큰 키 (없으면 None)."""
        best, node = None, self.root
        while node:
            if node.key == x:
                return x
            if node.key < x:
                best = node.key
                node = node.right
            else:
                node = node.left
        return best

    def ceil(self, x):
        """x 이상인 가장 작은 키 (없으면 None)."""
        best, node = None, self.root
        while node:
            if node.key == x:
                return x
            if node.key > x:
                best = node.key
                node = node.left
            else:
                node = node.right
        return best

    def successor(self, x):
        """x 보다 큰 가장 작은 키 (없으면 None). x 가 트리에 없어도 된다."""
        best, node = None, self.root
        while node:
            if node.key > x:
                best = node.key
                node = node.left
            else:
                node = node.right
        return best


def build_balanced(sorted_keys: list) -> BST:
    """정렬된 키로부터 높이가 ⌈log₂(n+1)⌉ 인 BST 를 만든다. 가운데를 루트로 하고 양쪽을 재귀로 만든다."""
    tree = BST()

    def build(lo, hi):
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        node = Node(sorted_keys[mid])
        node.left = build(lo, mid - 1)
        node.right = build(mid + 1, hi)
        node.size = hi - lo + 1
        return node

    tree.root = build(0, len(sorted_keys) - 1)
    return tree


def postorder_from_preorder(preorder: list) -> list:
    """BST 의 전위 순회 결과로부터 후위 순회 결과를 O(n) 에 구한다. (키는 서로 다르다고 가정)

    스택에 "아직 오른쪽 자식이 정해지지 않을 수 있는 노드" 들을 쌓는다. 새 키가 스택 맨 위보다 작으면 맨 위의 왼쪽 자식,
    크면 맨 위가 키보다 작은 동안 pop 하고 마지막으로 pop 한 노드의 오른쪽 자식이 된다."""
    nodes = [Node(k) for k in preorder]
    stack = []
    for node in nodes:
        last = None
        while stack and stack[-1].key < node.key:
            last = stack.pop()
        if last is not None:
            last.right = node
        elif stack:
            stack[-1].left = node
        stack.append(node)
    result = []
    if not nodes:
        return result
    stack2 = [(nodes[0], False)]
    while stack2:
        node, visited = stack2.pop()
        if visited:
            result.append(node.key)
        else:
            stack2.append((node, True))
            if node.right:
                stack2.append((node.right, False))
            if node.left:
                stack2.append((node.left, False))
    return result


def main() -> None:
    preorder = [int(line) for line in sys.stdin.read().split()]
    print("\n".join(map(str, postorder_from_preorder(preorder))))


if __name__ == "__main__":
    main()
