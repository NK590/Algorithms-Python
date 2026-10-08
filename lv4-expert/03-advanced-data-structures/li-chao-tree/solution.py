"""리 차오 트리(Li Chao Tree) 심화 — 선분 추가, 최대/최소, 되돌리기, 직선이 살아 있는 시간 구간이 있는 오프라인 문제

README.md 의 설명과 짝을 이루는 참고 구현입니다. (Lv3 convex-hull-trick 의 리 차오 트리는 정의역 전체에 직선을 넣는 기본형이었고, 여기서는 그것을 넓힙니다.)
- 기본: 정의역 [lo, hi] 를 구간 트리로 쪼개고 노드마다 직선 하나를 둔다. 새 직선을 넣을 때 "노드 구간의 가운데에서 더 낮은 쪽" 을 노드에 남기고,
  진 직선은 한쪽 끝에서 이기는 쪽 자식으로 내려보낸다 (두 직선은 한 번만 만나므로 한쪽에서만 이긴다). 질의는 루트에서 x 의 잎까지 내려가며 만난 직선들의 최솟값. 둘 다 O(log C) (C = 정의역 크기).
- 선분 추가 add_segment(m, b, l, r): 직선이 x ∈ [l, r] 에서만 존재한다. [l, r] 을 구간 트리의 O(log C) 개 노드로 쪼개고, 각 노드에서 그 노드 구간만 다루는 삽입을 한다. O(log² C).
  (노드에 저장된 직선은 그 노드 구간 전체에서 유효해야 질의가 맞다 — 쪼갠 노드는 선분이 구간 전체를 덮으므로 만족한다.)
- 최대/최소: maximize=True 면 기울기·절편의 부호를 뒤집어 최솟값 구조로 처리하고 답의 부호를 되돌린다.
- 되돌리기: 삽입이 바꾼 (노드, 이전 직선) 을 기록해 두고 snapshot() / rollback(snapshot) 으로 되돌린다.
- min_over_time: 직선마다 "살아 있는 시간 구간 [start, end)" 이 있고 질의가 (시각, x) 인 오프라인 문제. 시간에 대한 구간 트리의 노드마다 직선을 걸어 두고, DFS 로 내려가며 삽입, 올라오며 되돌린다. O((L + Q) log Q · log C).
- 직접 실행하면 Library Checker "Segment Add Get Min" 형식 — `N Q`, 선분 N 개 `l r a b` (직선 y = a·x + b, 반열린 [l, r)), 질의 Q 개 `0 l r a b`(선분 추가) 또는 `1 p`(x = p 에서의 최솟값, 없으면 INFINITY) — 를 처리합니다.
"""
import sys
from bisect import bisect_left, bisect_right
from typing import Optional, Sequence

Line = tuple[int, int]


class LiChaoTree:
    def __init__(self, lo: int, hi: int, maximize: bool = False):
        if lo > hi:
            raise ValueError("lo ≤ hi 여야 합니다")
        self.lo, self.hi = lo, hi
        self.sign = -1 if maximize else 1  # 최댓값은 부호를 뒤집어 최솟값으로 처리
        self.lines: dict[int, Line] = {}  # 힙 번호 -> 그 노드 구간에 저장된 직선 (m, b)
        self._undo: list[tuple[int, Optional[Line]]] = []  # (노드, 바뀌기 전 직선) 기록

    @staticmethod
    def _at(line: Line, x: int) -> int:
        return line[0] * x + line[1]

    def _set(self, node: int, line: Line) -> None:
        self._undo.append((node, self.lines.get(node)))
        self.lines[node] = line

    def _insert(self, node: int, lo: int, hi: int, line: Line) -> None:
        """노드 구간 [lo, hi] 안에서만 직선을 삽입한다 (직선은 이 구간 전체에서 유효하다고 가정)."""
        while True:
            current = self.lines.get(node)
            if current is None:
                self._set(node, line)
                return
            mid = (lo + hi) // 2
            if self._at(line, mid) < self._at(current, mid):  # 가운데에서 더 낮은 직선을 이 노드에 남긴다
                self._set(node, line)
                line, current = current, line
            if lo == hi:
                return
            if self._at(line, lo) < self._at(current, lo):  # 진 직선이 왼쪽 끝에서 이기면 왼쪽으로
                node, hi = 2 * node, mid
            elif self._at(line, hi) < self._at(current, hi):  # 오른쪽 끝에서 이기면 오른쪽으로
                node, lo = 2 * node + 1, mid + 1
            else:
                return

    def add_line(self, slope: int, intercept: int) -> None:
        """y = slope·x + intercept 를 정의역 전체에 추가."""
        self._insert(1, self.lo, self.hi, (self.sign * slope, self.sign * intercept))

    def add_segment(self, slope: int, intercept: int, left: int, right: int) -> None:
        """y = slope·x + intercept 를 x ∈ [left, right] 에서만 추가. 정의역 밖이거나 비어 있는 부분(left > right) 은 노드 분해가 알아서 걸러낸다."""
        line = (self.sign * slope, self.sign * intercept)
        stack = [(1, self.lo, self.hi)]
        while stack:
            node, lo, hi = stack.pop()
            if right < lo or hi < left:
                continue
            if left <= lo and hi <= right:  # 이 노드 구간은 선분이 통째로 덮는다
                self._insert(node, lo, hi, line)
                continue
            mid = (lo + hi) // 2
            stack.append((2 * node + 1, mid + 1, hi))
            stack.append((2 * node, lo, mid))

    def query(self, x: int) -> Optional[int]:
        """x 에서의 최솟값(maximize 면 최댓값). 그 x 를 덮는 직선이 하나도 없으면 None."""
        if not self.lo <= x <= self.hi:
            raise ValueError("x 가 정의역을 벗어났습니다")
        node, lo, hi = 1, self.lo, self.hi
        best = None
        while True:
            line = self.lines.get(node)
            if line is not None:  # 선분 삽입 때문에 윗 노드가 비어 있어도 아래 노드에 선분이 있을 수 있다 (전체 구간 직선만 있을 때와 다르다)
                value = self._at(line, x)
                if best is None or value < best:
                    best = value
            if lo == hi:
                break
            mid = (lo + hi) // 2
            if x <= mid:
                node, hi = 2 * node, mid
            else:
                node, lo = 2 * node + 1, mid + 1
        return None if best is None else self.sign * best

    def snapshot(self) -> int:
        """지금 상태를 가리키는 표지. rollback 에 넘기면 이후의 삽입이 모두 취소된다."""
        return len(self._undo)

    def rollback(self, snapshot: int) -> None:
        while len(self._undo) > snapshot:
            node, previous = self._undo.pop()
            if previous is None:
                del self.lines[node]
            else:
                self.lines[node] = previous


def min_over_time(
    lo: int,
    hi: int,
    lines: Sequence[tuple[int, int, int, int]],
    queries: Sequence[tuple[int, int]],
    maximize: bool = False,
) -> list[Optional[int]]:
    """오프라인: 직선 (slope, intercept, start, end) 는 시각 start ≤ t < end 에만 존재한다. 질의 (t, x) 는 시각 t 에 살아 있는 직선들의 x 에서의 최솟값(없으면 None).
    질의를 시각 순서로 놓고, 직선의 생존 구간을 질의 번호 구간으로 바꿔 시간 구간 트리의 노드에 건다. DFS 로 내려가며 삽입하고 올라올 때 되돌린다."""
    count = len(queries)
    if count == 0:
        return []
    order = sorted(range(count), key=lambda i: queries[i][0])
    times = [queries[i][0] for i in order]
    size = 1
    while size < count:
        size *= 2
    attached: list[list[tuple[int, int]]] = [[] for _ in range(2 * size)]
    for slope, intercept, start, end in lines:
        left = bisect_left(times, start)  # start 이상인 첫 질의
        right = bisect_left(times, end)  # end 이상인 첫 질의 (end 시각의 질의는 제외)
        left += size
        right += size
        while left < right:
            if left & 1:
                attached[left].append((slope, intercept))
                left += 1
            if right & 1:
                right -= 1
                attached[right].append((slope, intercept))
            left //= 2
            right //= 2
    tree = LiChaoTree(lo, hi, maximize)
    answers: list[Optional[int]] = [None] * count
    stack: list[tuple[int, Optional[int]]] = [(1, None)]  # (노드, 되돌릴 표지 또는 None = 아직 들어가지 않음)
    while stack:
        node, mark = stack.pop()
        if mark is not None:
            tree.rollback(mark)
            continue
        snap = tree.snapshot()
        for slope, intercept in attached[node]:
            tree.add_line(slope, intercept)
        if node >= size:
            index = node - size
            if index < count:
                x = queries[order[index]][1]
                answers[order[index]] = tree.query(x)
            tree.rollback(snap)
            continue
        stack.append((node, snap))
        stack.append((2 * node + 1, None))
        stack.append((2 * node, None))
    return answers


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    tree = LiChaoTree(-10**9, 10**9)
    pos = 2
    for _ in range(n):
        left, right, a, b = (int(v) for v in data[pos : pos + 4])
        tree.add_segment(a, b, left, right - 1)
        pos += 4
    out = []
    for _ in range(q):
        if data[pos] == b"0":
            left, right, a, b = (int(v) for v in data[pos + 1 : pos + 5])
            tree.add_segment(a, b, left, right - 1)
            pos += 5
        else:
            answer = tree.query(int(data[pos + 1]))
            out.append("INFINITY" if answer is None else str(answer))
            pos += 2
    print("\n".join(out))


if __name__ == "__main__":
    main()
