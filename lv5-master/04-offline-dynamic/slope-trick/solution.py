"""기울기 트릭(Slope Trick) — 볼록한 구간선형 함수 f 를 "기울기가 바뀌는 점" 들의 힙 둘로 들고, 함수 전체를 갱신하는 DP 를 힙 연산 O(log n) 으로 옮기기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 볼록 구간선형 함수는 기울기가 1 씩 변하는 지점(변화점) 의 목록과 최솟값으로 정해진다. 최솟값이 되는 구간 [l, r] 을 경계로 왼쪽 변화점 L (최대 힙), 오른쪽 변화점 R (최소 힙) 으로 나눠 든다.
  모든 변화점 l ∈ L 은 모든 r ∈ R 이하이고, f(x) = min_value + Σ_{l∈L} max(0, l - x) + Σ_{r∈R} max(0, x - r).
- add_x_minus_a(a): f += max(0, x - a).  L 의 최댓값이 a 보다 크면 최솟값이 그만큼 올라가고, a 를 L 에 넣고 L 의 최댓값을 R 로 옮긴다.
  add_a_minus_x(a): f += max(0, a - x). 대칭.  add_abs(a): 둘 다 (f += |x - a|).
- prefix_min(): f(x) ← min_{y ≤ x} f(y) (오른쪽의 증가 부분을 평평하게: R 을 비운다).  suffix_min(): L 을 비운다.
- window_min(lo, hi): f(x) ← min_{x+lo ≤ y ≤ x+hi} f(y) (lo ≤ hi). 평평한 구간이 넓어진다: L 은 전체 -hi, R 은 전체 -lo 만큼 평행 이동. 힙을 건드리지 않고 지연 오프셋 두 개로 처리한다.
- shift(d): f(x) ← f(x - d). evaluate(x): f(x) 를 변화점으로부터 O(변화점 수) 에 계산. argmin(): 최솟값이 되는 구간 (l, r).
- 응용: min_cost_non_decreasing, min_cost_strictly_increasing, min_cost_bounded_difference (이웃한 값의 차가 d 이하), narrow_rectangles (조각이 서로 닿도록 가로로 옮기는 최소 이동 거리), max_profit_buy_sell (사고팔기).
- 직접 실행하면 Codeforces 713C 형식 — `n`, 이어서 n 개의 정수 — 를 받아 수열을 (순) 증가하게 만드는 데 필요한 ±1 연산의 최소 횟수를 출력합니다.
"""
import heapq
import sys
from typing import Sequence

INF = float("inf")


class SlopeTrick:
    """f(x) = min_value + Σ_{l∈L} max(0, l-x) + Σ_{r∈R} max(0, x-r). 처음에는 f ≡ 0."""

    def __init__(self):
        self._left: list = []  # 최대 힙(부호 반전). 실제 값 = -저장값 + _add_left
        self._right: list = []  # 최소 힙. 실제 값 = 저장값 + _add_right
        self._add_left = 0
        self._add_right = 0
        self.min_value = 0

    def __len__(self) -> int:
        return len(self._left) + len(self._right)

    def _push_left(self, value) -> None:
        heapq.heappush(self._left, -(value - self._add_left))

    def _pop_left(self):
        return -heapq.heappop(self._left) + self._add_left

    def _push_right(self, value) -> None:
        heapq.heappush(self._right, value - self._add_right)

    def _pop_right(self):
        return heapq.heappop(self._right) + self._add_right

    def left_top(self):
        """L 의 최댓값 (없으면 -∞): 최솟값이 되는 구간의 왼쪽 끝."""
        return -self._left[0] + self._add_left if self._left else -INF

    def right_top(self):
        """R 의 최솟값 (없으면 +∞): 최솟값이 되는 구간의 오른쪽 끝."""
        return self._right[0] + self._add_right if self._right else INF

    def argmin(self):
        return self.left_top(), self.right_top()

    def add_x_minus_a(self, a) -> None:
        """f += max(0, x - a)."""
        self.min_value += max(0, self.left_top() - a)
        self._push_left(a)
        self._push_right(self._pop_left())

    def add_a_minus_x(self, a) -> None:
        """f += max(0, a - x)."""
        self.min_value += max(0, a - self.right_top())
        self._push_right(a)
        self._push_left(self._pop_right())

    def add_abs(self, a) -> None:
        """f += |x - a|."""
        self.add_x_minus_a(a)
        self.add_a_minus_x(a)

    def prefix_min(self) -> None:
        """f(x) ← min_{y ≤ x} f(y)."""
        self._right.clear()

    def suffix_min(self) -> None:
        """f(x) ← min_{y ≥ x} f(y)."""
        self._left.clear()

    def window_min(self, lo, hi) -> None:
        """f(x) ← min_{x+lo ≤ y ≤ x+hi} f(y)  (lo ≤ hi)."""
        if lo > hi:
            raise ValueError("lo 는 hi 이하여야 합니다")
        self._add_left -= hi
        self._add_right -= lo

    def shift(self, d) -> None:
        """f(x) ← f(x - d)."""
        self._add_left += d
        self._add_right += d

    def evaluate(self, x):
        total = self.min_value
        total += sum(max(0, -stored + self._add_left - x) for stored in self._left)
        total += sum(max(0, x - (stored + self._add_right)) for stored in self._right)
        return total


def min_cost_non_decreasing(values: Sequence[int]) -> int:
    """수열을 비감소로 만드는 데 필요한 ±1 연산의 최소 횟수 (= 바꾼 값과의 절대 차의 합의 최소)."""
    st = SlopeTrick()
    for a in values:
        st.add_abs(a)
        st.prefix_min()
    return st.min_value


def min_cost_strictly_increasing(values: Sequence[int]) -> int:
    """수열을 (정수로) 순증가하게 만드는 최소 비용: b_i - i 가 비감소인 문제로 바꾼다."""
    return min_cost_non_decreasing([a - i for i, a in enumerate(values)])


def min_cost_bounded_difference(values: Sequence[int], d: int) -> int:
    """이웃한 값의 차이가 |b_i - b_{i-1}| ≤ d 가 되도록 b 를 정할 때 Σ|a_i - b_i| 의 최솟값."""
    st = SlopeTrick()
    for a in values:
        st.window_min(-d, d)  # 처음의 f ≡ 0 에서는 아무 일도 일어나지 않는다
        st.add_abs(a)
    return st.min_value


def narrow_rectangles(segments: Sequence[Sequence[int]]) -> int:
    """층마다 구간 [l_i, r_i] 하나. 이웃한 층의 구간은 적어도 한 점을 공유해야 하고, i 층을 x_i 만큼 옮기는 비용은 |x_i - l_i|. 총 이동 거리의 최솟값.

    f_i(x) = x 가 i 층의 새 왼쪽 끝일 때까지의 최소 비용. 다음 층의 왼쪽 끝 x' 는 [x - w', x + w] (w = i 층 너비, w' = 다음 층 너비) 에 있어야 한다.
    """
    st = SlopeTrick()
    previous_width = 0
    for left, right in segments:
        width = right - left
        st.window_min(-previous_width, width)  # 처음의 f ≡ 0 에서는 아무 일도 일어나지 않는다
        st.add_abs(left)
        previous_width = width
    return st.min_value


def max_profit_buy_sell(prices: Sequence[int]) -> int:
    """하루에 한 주를 사거나 팔거나 쉬는 것 중 하나를 할 수 있고 처음과 끝에 주식이 없어야 할 때의 최대 이익.

    사려는 값을 힙에 넣고, 더 비싼 날이 오면 가장 싼 값에 산 것을 팔아 이익을 챙긴다. 판 값도 힙에 넣어 '더 비싼 날에 팔 걸 그랬다' 를 되돌릴 수 있게 한다 (기울기 트릭의 L 힙).
    """
    heap: list = []
    profit = 0
    for price in prices:
        heapq.heappush(heap, price)
        if heap[0] < price:
            profit += price - heapq.heappop(heap)
            heapq.heappush(heap, price)
    return profit


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    print(min_cost_strictly_increasing([int(x) for x in data[1:1 + n]]))


if __name__ == "__main__":
    main()
