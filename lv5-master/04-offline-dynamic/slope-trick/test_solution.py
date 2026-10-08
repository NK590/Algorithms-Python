"""solution.py 검증: 정수 격자 위에 함수 값을 직접 들고 같은 연산을 적용하는 참조 구현, 그리고 정의 그대로의 DP 와 비교"""
import io
import random
import time

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)
LOW, HIGH = -200, 200  # 격자의 범위. 안쪽 [-30, 30] 에서만 비교한다 (경계에서 잘리는 영향을 피함)
INNER = range(-30, 31)


class Grid:
    """f 를 [LOW, HIGH] 의 정수마다 값으로 들고 연산을 정의 그대로 적용하는 참조 구현."""

    def __init__(self):
        self.values = {x: 0 for x in range(LOW, HIGH + 1)}

    def add_x_minus_a(self, a):
        for x in self.values:
            self.values[x] += max(0, x - a)

    def add_a_minus_x(self, a):
        for x in self.values:
            self.values[x] += max(0, a - x)

    def add_abs(self, a):
        for x in self.values:
            self.values[x] += abs(x - a)

    def prefix_min(self):
        best = None
        for x in range(LOW, HIGH + 1):
            best = self.values[x] if best is None else min(best, self.values[x])
            self.values[x] = best

    def suffix_min(self):
        best = None
        for x in range(HIGH, LOW - 1, -1):
            best = self.values[x] if best is None else min(best, self.values[x])
            self.values[x] = best

    def window_min(self, lo, hi):
        old = dict(self.values)
        for x in self.values:
            first = min(max(LOW, x + lo), HIGH)
            last = max(first, min(HIGH, x + hi))
            self.values[x] = min(old[y] for y in range(first, last + 1))

    def shift(self, d):
        old = dict(self.values)
        for x in self.values:
            self.values[x] = old.get(x - d, 10**9)


def apply_random_operation(rng, trick, grid):
    kind = rng.choice(["x_minus_a", "a_minus_x", "abs", "abs", "prefix", "suffix", "window", "shift"])
    a = rng.randint(-8, 8)
    if kind == "x_minus_a":
        trick.add_x_minus_a(a), grid.add_x_minus_a(a)
    elif kind == "a_minus_x":
        trick.add_a_minus_x(a), grid.add_a_minus_x(a)
    elif kind == "abs":
        trick.add_abs(a), grid.add_abs(a)
    elif kind == "prefix":
        trick.prefix_min(), grid.prefix_min()
    elif kind == "suffix":
        trick.suffix_min(), grid.suffix_min()
    elif kind == "window":
        lo = rng.randint(-3, 2)
        hi = lo + rng.randint(0, 3)
        trick.window_min(lo, hi), grid.window_min(lo, hi)
    else:
        d = rng.randint(-3, 3)
        trick.shift(d), grid.shift(d)
    return kind


def test_initial_function_is_zero():
    st = solution.SlopeTrick()
    assert st.min_value == 0 and len(st) == 0
    assert st.argmin() == (-float("inf"), float("inf"))
    assert st.evaluate(123) == 0


def test_matches_grid_reference_on_random_operation_sequences():
    rng = random.Random(0)
    for _ in range(400):
        st, grid = solution.SlopeTrick(), Grid()
        for _ in range(rng.randint(1, 10)):
            apply_random_operation(rng, st, grid)
        for x in INNER:
            assert st.evaluate(x) == grid.values[x], x
        inner_values = [grid.values[x] for x in INNER]
        assert st.min_value == min(inner_values)
        left, right = st.argmin()
        minimizers = [x for x in INNER if grid.values[x] == min(inner_values)]
        assert minimizers == [x for x in INNER if left <= x <= right]


def test_each_operation_in_isolation():
    for kind, op in [("x_minus_a", "add_x_minus_a"), ("a_minus_x", "add_a_minus_x"), ("abs", "add_abs")]:
        for a in (-5, 0, 7):
            st, grid = solution.SlopeTrick(), Grid()
            getattr(st, op)(a)
            getattr(grid, op)(a)
            assert all(st.evaluate(x) == grid.values[x] for x in INNER), (kind, a)


def test_breakpoint_count_and_prefix_suffix():
    st = solution.SlopeTrick()
    for a in (3, 1, 4, 1, 5):
        st.add_abs(a)
    assert len(st) == 10
    st.prefix_min()
    assert len(st) == 5 and st.argmin()[1] == float("inf")
    st.suffix_min()
    assert len(st) == 0 and st.argmin() == (-float("inf"), float("inf"))


def test_window_min_requires_ordered_bounds():
    with pytest.raises(ValueError, match="lo"):
        solution.SlopeTrick().window_min(3, 2)


def test_window_and_shift_offsets_apply_to_later_insertions():
    """오프셋이 쌓인 뒤에 넣은 변화점도 올바른 위치에 있어야 한다."""
    rng = random.Random(1)
    for _ in range(200):
        st, grid = solution.SlopeTrick(), Grid()
        for _ in range(rng.randint(3, 9)):
            apply_random_operation(rng, st, grid)
            apply_random_operation(rng, st, grid)
        st.add_abs(0), grid.add_abs(0)
        assert all(st.evaluate(x) == grid.values[x] for x in INNER)


def dp_non_decreasing(values):
    lo, hi = min(values) - 2, max(values) + 2
    cost = {x: abs(values[0] - x) for x in range(lo, hi + 1)}
    for a in values[1:]:
        running, new = None, {}
        for x in range(lo, hi + 1):
            running = cost[x] if running is None else min(running, cost[x])
            new[x] = running + abs(a - x)
        cost = new
    return min(cost.values())


def dp_strictly_increasing(values):
    n = len(values)
    lo, hi = min(values) - n - 2, max(values) + n + 2
    cost = {x: abs(values[0] - x) for x in range(lo, hi + 1)}
    for a in values[1:]:
        running, new = None, {}
        for x in range(lo, hi + 1):
            if x - 1 >= lo:
                running = cost[x - 1] if running is None else min(running, cost[x - 1])
            new[x] = (running if running is not None else 10**9) + abs(a - x)
        cost = new
    return min(cost.values())


def dp_bounded_difference(values, d):
    lo, hi = min(values) - 2, max(values) + 2
    cost = {x: abs(values[0] - x) for x in range(lo, hi + 1)}
    for a in values[1:]:
        cost = {x: min(cost[y] for y in range(max(lo, x - d), min(hi, x + d) + 1)) + abs(a - x) for x in range(lo, hi + 1)}
    return min(cost.values())


def dp_narrow_rectangles(segments):
    lows = [l for l, _ in segments]
    widths = [r - l for l, r in segments]
    lo, hi = min(lows) - max(widths) - 2, max(lows) + max(widths) + 2
    cost = {x: abs(segments[0][0] - x) for x in range(lo, hi + 1)}
    for i in range(1, len(segments)):
        w_prev, w = widths[i - 1], widths[i]
        cost = {
            x: min(cost[y] for y in range(lo, hi + 1) if x <= y + w_prev and y <= x + w) + abs(segments[i][0] - x)
            for x in range(lo, hi + 1)
        }
    return min(cost.values())


def dp_buy_sell(prices):
    n = len(prices)
    best = {0: 0}
    for p in prices:
        new = dict(best)
        for k, value in best.items():
            if k + 1 <= n:
                new[k + 1] = max(new.get(k + 1, -10**9), value - p)
            if k >= 1:
                new[k - 1] = max(new.get(k - 1, -10**9), value + p)
        best = new
    return best[0]


def test_non_decreasing_matches_dp():
    rng = random.Random(2)
    for _ in range(400):
        values = [rng.randint(-8, 8) for _ in range(rng.randint(1, 9))]
        assert solution.min_cost_non_decreasing(values) == dp_non_decreasing(values), values


def test_strictly_increasing_matches_dp_and_samples():
    rng = random.Random(3)
    for _ in range(300):
        values = [rng.randint(-8, 8) for _ in range(rng.randint(1, 8))]
        assert solution.min_cost_strictly_increasing(values) == dp_strictly_increasing(values), values
    assert solution.min_cost_strictly_increasing([2, 1, 5, 11, 5, 9, 11]) == 9
    assert solution.min_cost_strictly_increasing([5, 4, 3, 2, 1]) == 12
    assert solution.min_cost_strictly_increasing([]) == 0
    assert solution.min_cost_non_decreasing([]) == 0


def test_bounded_difference_matches_dp():
    rng = random.Random(4)
    for _ in range(250):
        values = [rng.randint(-10, 10) for _ in range(rng.randint(1, 8))]
        d = rng.randint(0, 4)
        assert solution.min_cost_bounded_difference(values, d) == dp_bounded_difference(values, d), (values, d)


def test_narrow_rectangles_matches_dp():
    rng = random.Random(5)
    for _ in range(200):
        segments = []
        for _ in range(rng.randint(1, 6)):
            left = rng.randint(-6, 10)
            segments.append((left, left + rng.randint(0, 4)))
        assert solution.narrow_rectangles(segments) == dp_narrow_rectangles(segments), segments
    assert solution.narrow_rectangles([(1, 3), (10, 12), (1, 3)]) == 7


def test_buy_sell_matches_dp_and_sample():
    rng = random.Random(6)
    for _ in range(300):
        prices = [rng.randint(1, 12) for _ in range(rng.randint(1, 10))]
        assert solution.max_profit_buy_sell(prices) == dp_buy_sell(prices), prices
    assert solution.max_profit_buy_sell([10, 5, 4, 7, 9, 12, 6, 2, 10]) == 20
    assert solution.max_profit_buy_sell([]) == 0


def test_speed_for_two_hundred_thousand_values():
    rng = random.Random(7)
    values = [rng.randint(0, 10**9) for _ in range(200000)]
    start = time.perf_counter()
    cost = solution.min_cost_non_decreasing(values)
    assert time.perf_counter() - start < 30
    assert cost > 0


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("7\n2 1 5 11 5 9 11\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "9"


def test_main_reads_every_number(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("5\n5 4 3 2 1\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "12"
