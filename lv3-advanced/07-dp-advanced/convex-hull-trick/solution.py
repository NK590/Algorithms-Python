"""볼록 껍질 트릭(Convex Hull Trick, CHT) — dp[i] = min_j (dp[j] + b_j·x_i) 꼴의 점화식을 직선들의 아래 껍질로 O(n log n) 또는 O(n) 에

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 점화식이 dp[i] = min_j ( m_j · x_i + c_j ) 처럼 j 쪽 값 두 개(기울기 m_j, 절편 c_j) 와 i 쪽 값 x_i 의 곱으로 쓰이면, 각 j 는 직선 y = m_j·x + c_j 이고
  dp[i] 는 "x = x_i 에서 직선들 중 가장 낮은 값" 입니다. 쓸모없는 직선(어느 x 에서도 최소가 아닌)을 버리고 남은 직선들의 아래 껍질에서 답을 찾습니다.
- MonotoneCHT: 기울기가 정렬된 순서로 들어오는 직선들(최소: 내림차순, 최대: 오름차순)에 대한 껍질. 스택으로 쓸모없는 직선을 지우고, 질의는
  이진 탐색(임의의 x, O(log n)) 또는 포인터(x 가 줄지 않을 때, 상각 O(1)).  외적을 곱셈으로 비교하므로 정수에서 정확합니다.
- LiChaoTree: 정의역 [lo, hi] 의 정수 x 에서, 기울기 순서 없이 직선을 넣고 최솟값을 묻는 트리. 구간의 가운데에서 더 낮은 직선을 남기고 진 직선은 한쪽으로 내려보낸다. O(log(hi - lo)).
- land_purchase_cost: 땅 사기 — (w, h) 땅들을 묶어 사고, 묶음의 값은 (최대 w) × (최대 h).  min_cost_batches: 나눈 묶음마다 (합)² + c.
- 직접 실행하면 직사각형 묶음 구매 예제 형식 — `N` 과 N 개의 `w h` — 을 받아 땅을 사는 최소 비용을 출력합니다.
"""
import sys
from typing import Iterable, Optional, Sequence


class MonotoneCHT:
    """기울기가 정렬되어 들어오는 직선들의 최솟값(maximize=True 면 최댓값) 껍질.
    최소: 기울기를 내림차순(같은 값 허용) 으로, 최대: 오름차순으로 add 한다."""

    def __init__(self, maximize: bool = False):
        self.maximize = maximize
        self.slopes: list[int] = []  # 내부는 항상 "최솟값" 으로 통일 (최대면 부호를 뒤집어 저장)
        self.intercepts: list[int] = []
        self.pointer = 0

    def __len__(self) -> int:
        return len(self.slopes)

    def add(self, slope: int, intercept: int) -> None:
        if self.maximize:
            slope, intercept = -slope, -intercept
        if self.slopes and slope > self.slopes[-1]:
            raise ValueError("기울기가 정렬된 순서(최소: 내림차순, 최대: 오름차순)로 들어와야 합니다")
        if self.slopes and slope == self.slopes[-1]:
            if intercept >= self.intercepts[-1]:  # 기울기가 같으면 절편이 작은 쪽만 쓸모 있다
                return
            self.slopes.pop()
            self.intercepts.pop()
        while len(self.slopes) >= 2 and self._useless(len(self.slopes) - 2, len(self.slopes) - 1, slope, intercept):
            self.slopes.pop()
            self.intercepts.pop()
        self.slopes.append(slope)
        self.intercepts.append(intercept)
        self.pointer = min(self.pointer, len(self.slopes) - 1)

    def _useless(self, i1: int, i2: int, m3: int, b3: int) -> bool:
        """직선 i2 가 직선 i1 과 새 직선 (m3, b3) 사이에서 어느 x 에서도 최소가 아닌가. (m1 > m2 > m3)
        i1, i3 의 교점이 i1, i2 의 교점보다 왼쪽(또는 같음) 이면 i2 는 쓸모없다:  (b3 - b1)(m1 - m2) ≤ (b2 - b1)(m1 - m3)."""
        m1, b1 = self.slopes[i1], self.intercepts[i1]
        m2, b2 = self.slopes[i2], self.intercepts[i2]
        return (b3 - b1) * (m1 - m2) <= (b2 - b1) * (m1 - m3)

    def _value(self, index: int, x: int) -> int:
        return self.slopes[index] * x + self.intercepts[index]

    def query(self, x: int) -> int:
        """x 에서의 최솟값(최대 모드면 최댓값). 임의의 x, 이진 탐색 O(log n)."""
        if not self.slopes:
            raise ValueError("직선이 없습니다")
        low, high = 0, len(self.slopes) - 1
        while low < high:  # 껍질 위의 직선들의 값은 x 에서 (줄어들다가 늘어나는) 모양이다
            mid = (low + high) // 2
            if self._value(mid, x) > self._value(mid + 1, x):
                low = mid + 1
            else:
                high = mid
        value = self._value(low, x)
        return -value if self.maximize else value

    def query_monotone(self, x: int) -> int:
        """x 가 줄어들지 않는 순서로만 부르는 질의. 포인터를 앞으로만 밀어 상각 O(1). 추가와 섞어 써도 된다."""
        if not self.slopes:
            raise ValueError("직선이 없습니다")
        while self.pointer + 1 < len(self.slopes) and self._value(self.pointer + 1, x) <= self._value(self.pointer, x):
            self.pointer += 1
        value = self._value(self.pointer, x)
        return -value if self.maximize else value


class LiChaoTree:
    """정수 x ∈ [lo, hi] 에서 직선들의 최솟값을 묻는 리차오 트리. 직선은 어떤 순서로든 추가한다."""

    def __init__(self, lo: int, hi: int):
        if lo > hi:
            raise ValueError("lo ≤ hi 여야 합니다")
        self.lo, self.hi = lo, hi
        self.lines: dict[int, tuple[int, int]] = {}  # 힙 번호 -> 그 구간에 저장된 직선 (m, b)

    @staticmethod
    def _at(line: tuple[int, int], x: int) -> int:
        return line[0] * x + line[1]

    def add_line(self, slope: int, intercept: int) -> None:
        line = (slope, intercept)
        node, lo, hi = 1, self.lo, self.hi
        while True:
            current = self.lines.get(node)
            if current is None:
                self.lines[node] = line
                return
            mid = (lo + hi) // 2
            if self._at(line, mid) < self._at(current, mid):  # 가운데에서 더 낮은 직선을 이 노드에 남긴다
                self.lines[node], line = line, current
                current = self.lines[node]
            if lo == hi:
                return
            if self._at(line, lo) < self._at(current, lo):  # 진 직선이 왼쪽 끝에서 이기면 왼쪽으로
                node, hi = 2 * node, mid
            elif self._at(line, hi) < self._at(current, hi):  # 오른쪽 끝에서 이기면 오른쪽으로
                node, lo = 2 * node + 1, mid + 1
            else:
                return

    def query(self, x: int) -> Optional[int]:
        """x 에서의 최솟값. 직선이 하나도 없으면 None."""
        if not self.lo <= x <= self.hi:
            raise ValueError("x 가 정의역을 벗어났습니다")
        node, lo, hi = 1, self.lo, self.hi
        best = None
        while True:
            line = self.lines.get(node)
            if line is None:
                return best
            value = self._at(line, x)
            if best is None or value < best:
                best = value
            if lo == hi:
                return best
            mid = (lo + hi) // 2
            if x <= mid:
                node, hi = 2 * node, mid
            else:
                node, lo = 2 * node + 1, mid + 1


def land_purchase_cost(lands: Iterable[tuple[int, int]]) -> int:
    """땅 (w, h) 들을 여러 묶음으로 사고, 묶음의 값은 (최대 w)·(최대 h). 총 값의 최솟값.
    다른 땅에 덮이는(w, h 가 모두 이하인) 땅은 버리고, 남은 땅을 w 오름차순(h 내림차순) 으로 놓으면 묶음은 연속한 구간이다."""
    ordered = sorted(lands, key=lambda land: (-land[0], -land[1]))
    kept: list[tuple[int, int]] = []
    tallest = 0
    for w, h in ordered:
        if h > tallest:  # 지금까지 본 (더 넓은) 땅들보다 높은 것만 쓸모 있다
            kept.append((w, h))
            tallest = h
    kept.reverse()  # w 오름차순, h 내림차순
    m = len(kept)
    if m == 0:
        return 0
    # dp[i] = 앞 i 개를 산 최소 비용 = min_j dp[j] + h[j]·w[i-1]  (j..i-1 번째를 한 묶음으로)
    hull = MonotoneCHT()
    dp = [0] * (m + 1)
    hull.add(kept[0][1], 0)
    for i in range(1, m + 1):
        dp[i] = hull.query_monotone(kept[i - 1][0])
        if i < m:
            hull.add(kept[i][1], dp[i])
    return dp[m]


def min_cost_batches(values: Sequence[int], fixed_cost: int) -> int:
    """값 values 를 앞에서부터 연속한 묶음으로 나눈다. 묶음마다 (합)² + fixed_cost. 총 비용의 최솟값.
    dp[i] = min_j dp[j] + (S_i - S_j)² + c  =  S_i² + c + min_j ( -2·S_j·S_i + (dp[j] + S_j²) ).  값이 음이 아니면 기울기(-2·S_j) 는 내림차순, S_i 는 오름차순."""
    prefix = [0]
    for v in values:
        prefix.append(prefix[-1] + v)
    if any(b < a for a, b in zip(prefix, prefix[1:])):
        raise ValueError("값은 음이 아니어야 합니다")
    hull = MonotoneCHT()
    hull.add(0, 0)  # j = 0: dp[0] = 0, S_0 = 0
    dp = 0
    for i in range(1, len(prefix)):
        dp = prefix[i] ** 2 + fixed_cost + hull.query_monotone(prefix[i])
        hull.add(-2 * prefix[i], dp + prefix[i] ** 2)
    return dp


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    lands = [(int(data[1 + 2 * i]), int(data[2 + 2 * i])) for i in range(n)]
    print(land_purchase_cost(lands))


if __name__ == "__main__":
    main()
