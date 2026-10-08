"""스플레이 트리(Splay Tree) — 접근한 노드를 회전으로 루트까지 끌어올려, 균형 정보 없이도 분할 상환 O(log n) 을 얻는 이진 탐색 트리

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 스플레이(splay): 노드 x 를 루트로 올리는 연산. 부모 p, 조부모 g 와의 모양에 따라 세 가지 회전을 한다:
  zig (p 가 루트: x 를 한 번 회전), zig-zig (x 와 p 가 같은 방향 자식: p 를 먼저 회전하고 x 를 회전), zig-zag (방향이 다름: x 를 두 번 회전).
  zig-zig 에서 "p 를 먼저" 돌리는 것이 중요하다 — x 만 두 번 돌리면 긴 사슬이 절반으로 줄지 않고 분할 상환 O(log n) 이 깨진다.
- 접근할 때마다 splay 를 하므로 "최근에 쓴 것이 위에 있다". 분할 상환 O(log n), 순차 접근 정리(키를 순서대로 접근하면 전체 O(n)), 작업 집합 성질 등이 성립한다. 한 번의 연산은 O(n) 일 수 있다.
- 모든 코드는 반복문(부모 포인터 사용)이라 사슬 모양으로 깊어진 트리에서도 재귀 한도 문제가 없다.
- SplaySet: 서로 다른 키의 순서 집합. add / remove / in / rank(x 보다 작은 키 수) / kth_smallest(1 부터) / floor·ceil·predecessor·successor / min / max / pop_min. rotations 로 회전 횟수를 센다.
- SplaySequence: 암시적 키(위치) 스플레이 트리. 양 끝에 보초 노드를 두어 구간 [l, r) 을 "l 바로 앞 노드를 루트로, r 바로 뒤 노드를 그 자식으로" 올리면 사이의 서브트리가 정확히 구간이 된다.
  insert / erase / get / set / reverse(지연 뒤집기) / range_sum, 모두 분할 상환 O(log n).
- 직접 실행하면 Luogu P3391 "文艺平衡树" 형식 — `n m`, 이어서 m 줄의 `l r`(1 부터, 양끝 포함 뒤집기) — 를 처리해 1..n 의 최종 배열을 출력합니다.
"""
import sys
from typing import Iterable, Optional, Sequence


class _SplayCore:
    """부모 포인터를 가진 노드 풀과 회전·스플레이. 0 번 노드는 "없음" 이다."""

    def __init__(self) -> None:
        self.value: list[int] = [0]
        self.left: list[int] = [0]
        self.right: list[int] = [0]
        self.parent: list[int] = [0]
        self.size: list[int] = [0]
        self.total: list[int] = [0]
        self.reversed: list[bool] = [False]
        self.free: list[int] = []
        self.root = 0
        self.rotations = 0

    def _new_node(self, value: int) -> int:
        if self.free:
            x = self.free.pop()
            self.value[x], self.left[x], self.right[x], self.parent[x] = value, 0, 0, 0
            self.size[x], self.total[x], self.reversed[x] = 1, value, False
            return x
        self.value.append(value)
        self.left.append(0)
        self.right.append(0)
        self.parent.append(0)
        self.size.append(1)
        self.total.append(value)
        self.reversed.append(False)
        return len(self.value) - 1

    def _pull(self, x: int) -> None:
        l, r = self.left[x], self.right[x]
        self.size[x] = self.size[l] + self.size[r] + 1
        self.total[x] = self.total[l] + self.total[r] + self.value[x]

    def _push(self, x: int) -> None:
        if self.reversed[x]:
            l, r = self.left[x], self.right[x]
            self.left[x], self.right[x] = r, l
            if l:
                self.reversed[l] = not self.reversed[l]
            if r:
                self.reversed[r] = not self.reversed[r]
            self.reversed[x] = False

    def _rotate(self, x: int) -> None:
        """x 를 부모 p 의 자리로 올린다 (p 는 x 의 자식이 된다)."""
        p = self.parent[x]
        g = self.parent[p]
        if self.left[p] == x:
            inner = self.right[x]
            self.left[p] = inner
            self.right[x] = p
        else:
            inner = self.left[x]
            self.right[p] = inner
            self.left[x] = p
        if inner:
            self.parent[inner] = p
        self.parent[p] = x
        self.parent[x] = g
        if g:
            if self.left[g] == p:
                self.left[g] = x
            else:
                self.right[g] = x
        self._pull(p)
        self._pull(x)
        self.rotations += 1

    def _splay(self, x: int, goal: int = 0) -> None:
        """x 를 goal 의 자식 자리(goal = 0 이면 루트) 로 올린다. 루트에서 x 까지의 경로는 지연 표시가 모두 내려가 있어야 한다 (_locate 가 내려가며 push 한다)."""
        while self.parent[x] != goal:
            p = self.parent[x]
            g = self.parent[p]
            if g != goal:
                same_side = (self.left[g] == p) == (self.left[p] == x)
                self._rotate(p if same_side else x)  # zig-zig 는 부모를 먼저, zig-zag 는 x 를 먼저
            self._rotate(x)
        if goal == 0:
            self.root = x

    def _locate(self, k: int) -> int:
        """중위 순회에서 k 번째(1 부터) 노드. 내려가며 지연 표시를 처리하고, 스플레이는 하지 않는다."""
        x = self.root
        while True:
            self._push(x)
            left_size = self.size[self.left[x]]
            if k <= left_size:
                x = self.left[x]
            elif k == left_size + 1:
                return x
            else:
                k -= left_size + 1
                x = self.right[x]

    def _build_balanced(self, ids: Sequence[int], lo: int, hi: int, parent: int) -> int:
        if lo > hi:
            return 0
        mid = (lo + hi) // 2
        x = ids[mid]
        self.parent[x] = parent
        self.left[x] = self._build_balanced(ids, lo, mid - 1, x)  # 깊이 log n 이라 재귀 한도 걱정이 없다
        self.right[x] = self._build_balanced(ids, mid + 1, hi, x)
        self._pull(x)
        return x

    def _inorder(self) -> list[int]:
        order: list[int] = []
        stack: list[int] = []
        x = self.root
        while stack or x:
            while x:
                self._push(x)
                stack.append(x)
                x = self.left[x]
            x = stack.pop()
            order.append(x)
            x = self.right[x]
        return order

    def to_list(self) -> list[int]:
        return [self.value[x] for x in self._inorder()]


class SplaySet(_SplayCore):
    def __init__(self, keys: Iterable[int] = ()):
        super().__init__()
        for key in keys:
            self.add(key)

    def __len__(self) -> int:
        return self.size[self.root]

    def _find(self, key: int) -> int:
        """key 를 찾아 내려가다 마지막으로 방문한 노드를 루트로 올린다 (키가 있으면 그 노드). 비어 있으면 0."""
        x, last = self.root, 0
        while x:
            last = x
            if key == self.value[x]:
                break
            x = self.left[x] if key < self.value[x] else self.right[x]
        if last:
            self._splay(last)
        return last

    def __contains__(self, key: int) -> bool:
        x = self._find(key)
        return bool(x) and self.value[x] == key

    def add(self, key: int) -> bool:
        """키를 넣는다. 이미 있으면 False."""
        x = self._find(key)
        if not x:
            self.root = self._new_node(key)
            return True
        if self.value[x] == key:
            return False
        new = self._new_node(key)
        if key < self.value[x]:  # x 가 루트이므로 x 의 왼쪽 서브트리 전체가 new 의 왼쪽이 된다
            moved = self.left[x]
            self.left[new], self.right[new] = moved, x
            self.left[x] = 0
        else:
            moved = self.right[x]
            self.right[new], self.left[new] = moved, x
            self.right[x] = 0
        if moved:
            self.parent[moved] = new
        self.parent[x] = new
        self._pull(x)
        self._pull(new)
        self.root = new
        return True

    def remove(self, key: int) -> bool:
        """키를 지운다. 없으면 False."""
        x = self._find(key)
        if not x or self.value[x] != key:
            return False
        left, right = self.left[x], self.right[x]
        self.free.append(x)
        if not left:
            self.root = right
            self.parent[right] = 0
            return True
        self.parent[left] = 0
        self.root = left
        biggest = left
        while self.right[biggest]:
            biggest = self.right[biggest]
        self._splay(biggest)  # 왼쪽 서브트리의 최댓값을 루트로: 오른쪽 자식이 없다
        self.right[biggest] = right
        if right:
            self.parent[right] = biggest
        self._pull(biggest)
        return True

    def rank(self, key: int) -> int:
        """key 보다 작은 키의 수."""
        x = self._find(key)
        if not x:
            return 0
        return self.size[self.left[x]] + (1 if self.value[x] < key else 0)

    def kth_smallest(self, k: int) -> int:
        """k 번째(1 부터) 로 작은 키."""
        if not 1 <= k <= len(self):
            raise IndexError("k 가 범위를 벗어났습니다")
        x = self._locate(k)
        self._splay(x)
        return self.value[x]

    def _neighbor(self, x: int, direction: int) -> Optional[int]:
        """루트 x 의 중위 순회에서의 이전(direction = 0) / 다음(1) 노드의 키."""
        y = self.left[x] if direction == 0 else self.right[x]
        if not y:
            return None
        while (self.right[y] if direction == 0 else self.left[y]):
            y = self.right[y] if direction == 0 else self.left[y]
        self._splay(y)
        return self.value[y]

    def predecessor(self, key: int) -> Optional[int]:
        """key 보다 작은 키 중 가장 큰 것."""
        x = self._find(key)
        if not x:
            return None
        return self.value[x] if self.value[x] < key else self._neighbor(x, 0)

    def floor(self, key: int) -> Optional[int]:
        """key 이하인 키 중 가장 큰 것."""
        x = self._find(key)
        if not x:
            return None
        return self.value[x] if self.value[x] <= key else self._neighbor(x, 0)

    def successor(self, key: int) -> Optional[int]:
        """key 보다 큰 키 중 가장 작은 것."""
        x = self._find(key)
        if not x:
            return None
        return self.value[x] if self.value[x] > key else self._neighbor(x, 1)

    def ceil(self, key: int) -> Optional[int]:
        """key 이상인 키 중 가장 작은 것."""
        x = self._find(key)
        if not x:
            return None
        return self.value[x] if self.value[x] >= key else self._neighbor(x, 1)

    def min(self) -> int:
        if not self.root:
            raise IndexError("비어 있습니다")
        return self.kth_smallest(1)

    def max(self) -> int:
        if not self.root:
            raise IndexError("비어 있습니다")
        return self.kth_smallest(len(self))

    def pop_min(self) -> int:
        key = self.min()
        self.remove(key)
        return key


class SplaySequence(_SplayCore):
    def __init__(self, values: Iterable[int] = ()):
        super().__init__()
        ids = [self._new_node(0)] + [self._new_node(v) for v in values] + [self._new_node(0)]  # 양 끝의 보초 노드
        self.root = self._build_balanced(ids, 0, len(ids) - 1, 0)

    def __len__(self) -> int:
        return self.size[self.root] - 2

    def _middle(self, left: int, right: int) -> tuple[int, int]:
        """[left, right) 를 정확히 담는 서브트리를 만든다: left 바로 앞 노드 a 가 루트, right 바로 뒤 노드 b 가 a 의 자식. 구간은 b 의 왼쪽 서브트리."""
        if not 0 <= left <= right <= len(self):
            raise IndexError("구간이 범위를 벗어났습니다")
        a = self._locate(left + 1)  # 보초가 맨 앞이라 위치 left 의 바로 앞 노드는 순위 left + 1
        self._splay(a)
        b = self._locate(right + 2)
        self._splay(b, a)
        return a, b

    def insert(self, index: int, value: int) -> None:
        a, b = self._middle(index, index)
        new = self._new_node(value)
        self.left[b] = new
        self.parent[new] = b
        self._pull(b)
        self._pull(a)

    def append(self, value: int) -> None:
        self.insert(len(self), value)

    def erase(self, index: int) -> int:
        if not 0 <= index < len(self):
            raise IndexError("index 가 범위를 벗어났습니다")
        a, b = self._middle(index, index + 1)
        x = self.left[b]
        value = self.value[x]
        self.left[b] = 0
        self.parent[x] = 0
        self.free.append(x)
        self._pull(b)
        self._pull(a)
        return value

    def get(self, index: int) -> int:
        if not 0 <= index < len(self):
            raise IndexError("index 가 범위를 벗어났습니다")
        x = self._locate(index + 2)
        self._splay(x)
        return self.value[x]

    __getitem__ = get

    def set(self, index: int, value: int) -> None:
        self.get(index)  # 대상 노드가 루트가 된다
        self.value[self.root] = value
        self._pull(self.root)

    def reverse(self, left: int, right: int) -> None:
        a, b = self._middle(left, right)
        middle = self.left[b]
        if middle:
            self.reversed[middle] = not self.reversed[middle]

    def range_sum(self, left: int, right: int) -> int:
        a, b = self._middle(left, right)
        return self.total[self.left[b]]


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    sequence = SplaySequence(range(1, n + 1))
    for i in range(m):
        sequence.reverse(int(data[2 + 2 * i]) - 1, int(data[3 + 2 * i]))
    print(" ".join(map(str, sequence.to_list()[1:-1])))


if __name__ == "__main__":
    main()
