"""트립(Treap) — 이진 탐색 트리 + 힙 우선순위로 균형을 맞추고, split / merge 두 연산으로 구간 뒤집기·잘라 붙이기·순서 통계를 하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 트립: 각 노드에 무작위 우선순위를 주고 "키는 이진 탐색 트리, 우선순위는 최대 힙" 이 되도록 유지한다. 우선순위가 무작위면 트리의 모양은 키를 무작위 순서로 넣은 BST 와 같아 기대 깊이가 O(log n).
- 핵심 연산 두 개: split(t, k) = 앞의 k 개와 나머지로 쪼개기, merge(a, b) = (a 의 모든 원소 ≤ b 의 모든 원소) 인 두 트립을 우선순위가 높은 쪽을 위로 해 합치기. 둘 다 기대 O(log n).
  삽입·삭제·구간 연산이 모두 "쪼개고 → 일부를 고치고 → 합치기" 로 표현된다.
- ImplicitTreap(암시적 트립): 키를 저장하지 않고 "중위 순회에서의 위치" 가 곧 키 (노드의 서브트리 크기로 위치를 계산). 배열처럼 insert(i, x) / erase(i) / get(i) 와
  구간 뒤집기 reverse(l, r), 구간 더하기 add(l, r, d), 구간 합 range_sum, 구간 최솟값 range_min, 구간 잘라 붙이기 move(l, r, to) 를 모두 O(log n).
  뒤집기와 더하기는 지연 전파(lazy): 노드에 표시만 해 두고 내려갈 때 자식에게 밀어 준다.
- OrderedMultiset(순서 있는 다중집합): 값 자체가 키. add / remove(하나) / count / rank(x 보다 작은 원소 수) / kth_smallest / floor·ceil·predecessor·successor / pop_min·pop_max.
- 우선순위는 시드가 있는 난수라서 같은 입력이면 같은 모양이다. 분할·병합이 재귀지만 기대 깊이가 O(log n) 이므로 재귀 한도는 문제가 되지 않는다.
- 직접 실행하면 Library Checker "Range Reverse Range Sum" 형식 — `N Q`, 수열, 질의 `0 l r`(반열린 [l, r) 뒤집기) 또는 `1 l r`(합 출력) — 을 처리합니다.
"""
import random
import sys
from typing import Iterable, Iterator, Optional, Sequence

INF = float("inf")


class _TreapCore:
    """노드 풀(배열 여러 개)과 split / merge. 0 번 노드는 "없음" 이다."""

    def __init__(self, seed: int = 0):
        self.rng = random.Random(seed)
        self.value: list = [0]
        self.priority: list[float] = [0.0]
        self.left: list[int] = [0]
        self.right: list[int] = [0]
        self.size: list[int] = [0]
        self.total: list = [0]  # 서브트리 값의 합
        self.low: list = [INF]  # 서브트리 값의 최솟값
        self.lazy_add: list = [0]
        self.reversed: list[bool] = [False]
        self.free: list[int] = []
        self.root = 0

    def _new_node(self, value) -> int:
        if self.free:
            t = self.free.pop()
            self.value[t], self.priority[t] = value, self.rng.random()
            self.left[t] = self.right[t] = 0
            self.size[t], self.total[t], self.low[t] = 1, value, value
            self.lazy_add[t], self.reversed[t] = 0, False
            return t
        self.value.append(value)
        self.priority.append(self.rng.random())
        self.left.append(0)
        self.right.append(0)
        self.size.append(1)
        self.total.append(value)
        self.low.append(value)
        self.lazy_add.append(0)
        self.reversed.append(False)
        return len(self.value) - 1

    def _pull(self, t: int) -> None:
        l, r = self.left[t], self.right[t]
        self.size[t] = self.size[l] + self.size[r] + 1
        self.total[t] = self.total[l] + self.total[r] + self.value[t]
        self.low[t] = min(self.low[l], self.low[r], self.value[t])

    def _apply_add(self, t: int, delta) -> None:
        if t:
            self.value[t] += delta
            self.total[t] += delta * self.size[t]
            self.low[t] += delta
            self.lazy_add[t] += delta

    def _push(self, t: int) -> None:
        if self.reversed[t]:
            l, r = self.left[t], self.right[t]
            self.left[t], self.right[t] = r, l
            if l:
                self.reversed[l] = not self.reversed[l]
            if r:
                self.reversed[r] = not self.reversed[r]
            self.reversed[t] = False
        if self.lazy_add[t]:
            self._apply_add(self.left[t], self.lazy_add[t])
            self._apply_add(self.right[t], self.lazy_add[t])
            self.lazy_add[t] = 0

    def _split(self, t: int, k: int) -> tuple[int, int]:
        """중위 순회에서 앞의 k 개와 나머지로 쪼갠다."""
        if not t:
            return 0, 0
        self._push(t)
        if self.size[self.left[t]] >= k:
            a, b = self._split(self.left[t], k)
            self.left[t] = b
            self._pull(t)
            return a, t
        a, b = self._split(self.right[t], k - self.size[self.left[t]] - 1)
        self.right[t] = a
        self._pull(t)
        return t, b

    def _merge(self, a: int, b: int) -> int:
        """a 의 모든 원소가 b 의 모든 원소 앞에 오는 두 트립을 합친다."""
        if not a:
            return b
        if not b:
            return a
        if self.priority[a] > self.priority[b]:
            self._push(a)
            self.right[a] = self._merge(self.right[a], b)
            self._pull(a)
            return a
        self._push(b)
        self.left[b] = self._merge(a, self.left[b])
        self._pull(b)
        return b

    def _build(self, values: Sequence) -> int:
        """값들을 순서대로 놓은 트립을 O(n) 에 만든다 (데카르트 트리 구성: 스택으로 오른쪽 척추를 유지)."""
        stack: list[int] = []
        nodes = []
        for v in values:
            t = self._new_node(v)
            nodes.append(t)
            last = 0
            while stack and self.priority[stack[-1]] < self.priority[t]:
                last = stack.pop()
            self.left[t] = last
            if stack:
                self.right[stack[-1]] = t
            stack.append(t)
        for t in sorted(nodes, key=self.priority.__getitem__):  # 우선순위가 낮은 것(= 자식) 부터 크기·합을 채운다
            self._pull(t)
        return stack[0] if stack else 0

    def __len__(self) -> int:
        return self.size[self.root]

    def _inorder(self) -> Iterator[int]:
        stack: list[int] = []
        t = self.root
        while stack or t:
            while t:
                self._push(t)
                stack.append(t)
                t = self.left[t]
            t = stack.pop()
            yield t
            t = self.right[t]

    def to_list(self) -> list:
        return [self.value[t] for t in self._inorder()]

    def _release(self, t: int) -> None:
        self.free.append(t)


class ImplicitTreap(_TreapCore):
    def __init__(self, values: Iterable = (), seed: int = 0):
        super().__init__(seed)
        self.root = self._build(list(values))

    def _check_range(self, left: int, right: int) -> None:
        if not 0 <= left <= right <= len(self):
            raise IndexError("구간이 범위를 벗어났습니다")

    def _cut(self, left: int, right: int) -> tuple[int, int, int]:
        self._check_range(left, right)
        a, rest = self._split(self.root, left)
        b, c = self._split(rest, right - left)
        return a, b, c

    def _join(self, a: int, b: int, c: int) -> None:
        self.root = self._merge(self._merge(a, b), c)

    def insert(self, index: int, value) -> None:
        if not 0 <= index <= len(self):
            raise IndexError("index 가 범위를 벗어났습니다")
        a, b = self._split(self.root, index)
        self.root = self._merge(self._merge(a, self._new_node(value)), b)

    def append(self, value) -> None:
        self.insert(len(self), value)

    def erase(self, index: int):
        """index 번째 원소를 지우고 그 값을 돌려준다."""
        if not 0 <= index < len(self):
            raise IndexError("index 가 범위를 벗어났습니다")
        a, b, c = self._cut(index, index + 1)
        value = self.value[b]
        self._release(b)
        self._join(a, 0, c)
        return value

    def get(self, index: int):
        if not 0 <= index < len(self):
            raise IndexError("index 가 범위를 벗어났습니다")
        t = self.root
        while True:
            self._push(t)
            left_size = self.size[self.left[t]]
            if index < left_size:
                t = self.left[t]
            elif index == left_size:
                return self.value[t]
            else:
                index -= left_size + 1
                t = self.right[t]

    __getitem__ = get

    def reverse(self, left: int, right: int) -> None:
        a, b, c = self._cut(left, right)
        if b:
            self.reversed[b] = not self.reversed[b]
        self._join(a, b, c)

    def add(self, left: int, right: int, delta) -> None:
        a, b, c = self._cut(left, right)
        self._apply_add(b, delta)
        self._join(a, b, c)

    def range_sum(self, left: int, right: int):
        a, b, c = self._cut(left, right)
        result = self.total[b]
        self._join(a, b, c)
        return result

    def range_min(self, left: int, right: int):
        self._check_range(left, right)
        if left == right:
            raise ValueError("빈 구간의 최솟값은 없습니다")
        a, b, c = self._cut(left, right)
        result = self.low[b]
        self._join(a, b, c)
        return result

    def move(self, left: int, right: int, to: int) -> None:
        """[left, right) 를 잘라 내어, 남은 수열의 to 번째 자리 앞에 끼워 넣는다 (to 는 0 ≤ to ≤ 남은 길이)."""
        self._check_range(left, right)
        if not 0 <= to <= len(self) - (right - left):
            raise IndexError("to 가 범위를 벗어났습니다")
        a, b, c = self._cut(left, right)
        x, y = self._split(self._merge(a, c), to)
        self.root = self._merge(self._merge(x, b), y)


class OrderedMultiset(_TreapCore):
    def __init__(self, values: Iterable = (), seed: int = 0):
        super().__init__(seed)
        self.root = self._build(sorted(values))

    def _split_value(self, t: int, x, inclusive: bool) -> tuple[int, int]:
        """왼쪽: x 보다 작은(inclusive 면 x 이하인) 원소들, 오른쪽: 나머지."""
        if not t:
            return 0, 0
        goes_left = self.value[t] <= x if inclusive else self.value[t] < x
        if goes_left:
            a, b = self._split_value(self.right[t], x, inclusive)
            self.right[t] = a
            self._pull(t)
            return t, b
        a, b = self._split_value(self.left[t], x, inclusive)
        self.left[t] = b
        self._pull(t)
        return a, t

    def add(self, x) -> None:
        a, b = self._split_value(self.root, x, False)
        self.root = self._merge(self._merge(a, self._new_node(x)), b)

    def remove(self, x) -> bool:
        """x 하나를 지운다. 없으면 False."""
        a, rest = self._split_value(self.root, x, False)
        b, c = self._split_value(rest, x, True)  # b: x 와 같은 원소들
        if b:
            rest_of_b = self._merge(self.left[b], self.right[b])  # b 의 뿌리 하나만 버린다
            self._release(b)
            b = rest_of_b
            found = True
        else:
            found = False
        self.root = self._merge(self._merge(a, b), c)
        return found

    def rank(self, x) -> int:
        """x 보다 작은 원소의 수."""
        t, count = self.root, 0
        while t:
            if self.value[t] < x:
                count += self.size[self.left[t]] + 1
                t = self.right[t]
            else:
                t = self.left[t]
        return count

    def count_at_most(self, x) -> int:
        t, count = self.root, 0
        while t:
            if self.value[t] <= x:
                count += self.size[self.left[t]] + 1
                t = self.right[t]
            else:
                t = self.left[t]
        return count

    def count(self, x) -> int:
        return self.count_at_most(x) - self.rank(x)

    def __contains__(self, x) -> bool:
        return self.count(x) > 0

    def kth_smallest(self, k: int):
        """k 번째(1 부터) 로 작은 원소."""
        if not 1 <= k <= len(self):
            raise IndexError("k 가 범위를 벗어났습니다")
        t = self.root
        while True:
            left_size = self.size[self.left[t]]
            if k <= left_size:
                t = self.left[t]
            elif k == left_size + 1:
                return self.value[t]
            else:
                k -= left_size + 1
                t = self.right[t]

    def __getitem__(self, index: int):
        """정렬했을 때 index 번째(0 부터) 원소."""
        return self.kth_smallest(index + 1)

    def _largest(self, x, inclusive: bool):
        t, best = self.root, None
        while t:
            if self.value[t] < x or (inclusive and self.value[t] == x):
                best = self.value[t]
                t = self.right[t]
            else:
                t = self.left[t]
        return best

    def _smallest(self, x, inclusive: bool):
        t, best = self.root, None
        while t:
            if self.value[t] > x or (inclusive and self.value[t] == x):
                best = self.value[t]
                t = self.left[t]
            else:
                t = self.right[t]
        return best

    def predecessor(self, x) -> Optional[int]:
        """x 보다 작은 원소 중 가장 큰 것 (없으면 None)."""
        return self._largest(x, False)

    def floor(self, x) -> Optional[int]:
        """x 이하인 원소 중 가장 큰 것."""
        return self._largest(x, True)

    def successor(self, x) -> Optional[int]:
        """x 보다 큰 원소 중 가장 작은 것."""
        return self._smallest(x, False)

    def ceil(self, x) -> Optional[int]:
        """x 이상인 원소 중 가장 작은 것."""
        return self._smallest(x, True)

    def pop_min(self):
        if not self.root:
            raise IndexError("비어 있습니다")
        a, rest = self._split(self.root, 1)
        value = self.value[a]
        self._release(a)
        self.root = rest
        return value

    def pop_max(self):
        if not self.root:
            raise IndexError("비어 있습니다")
        rest, b = self._split(self.root, len(self) - 1)
        value = self.value[b]
        self._release(b)
        self.root = rest
        return value


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    treap = ImplicitTreap([int(x) for x in data[2 : 2 + n]])
    out = []
    pos = 2 + n
    for _ in range(q):
        kind, left, right = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])
        pos += 3
        if kind == 0:
            treap.reverse(left, right)
        else:
            out.append(treap.range_sum(left, right))
    print("\n".join(map(str, out)))


if __name__ == "__main__":
    main()
