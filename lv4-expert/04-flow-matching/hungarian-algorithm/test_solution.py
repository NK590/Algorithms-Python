"""solution.py 검증: 모든 배정을 나열하는 전수 탐색과 무작위 행렬(정사각·직사각·음수·최대화·None)로 비교하고 쌍대 해의 최적성 조건을 확인"""
import io
import itertools
import random
import time
from fractions import Fraction

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def brute(cost, maximize=False):
    """행마다 서로 다른 열 (n ≤ m) 을 고르는 모든 배정에서의 최적 합. None 칸을 쓰는 배정은 제외, 없으면 None."""
    n, m = len(cost), len(cost[0])
    best = None
    for columns in itertools.permutations(range(m), n):
        values = [cost[i][columns[i]] for i in range(n)]
        if any(x is None for x in values):
            continue
        total = sum(values)
        if best is None or (total > best if maximize else total < best):
            best = total
    return best


def assert_valid_assignment(cost, assignment, total):
    n, m = len(cost), len(cost[0])
    chosen = [j for j in assignment if j >= 0]
    assert len(chosen) == len(set(chosen)) == min(n, m)
    assert all(-1 <= j < m for j in assignment)
    assert sum(cost[i][j] for i, j in enumerate(assignment) if j >= 0) == total


def test_square_and_wide_matrices_match_permutations():
    rng = random.Random(0)
    for _ in range(600):
        n = rng.randint(1, 6)
        m = rng.randint(n, 7)
        cost = [[rng.randint(-8, 20) for _ in range(m)] for _ in range(n)]
        for maximize in (False, True):
            total, assignment = solution.hungarian(cost, maximize)
            assert total == brute(cost, maximize), (cost, maximize)
            assert_valid_assignment(cost, assignment, total)


def test_tall_matrices_leave_extra_rows_unassigned():
    rng = random.Random(1)
    for _ in range(300):
        m = rng.randint(1, 5)
        n = rng.randint(m + 1, 7)
        cost = [[rng.randint(-8, 20) for _ in range(m)] for _ in range(n)]
        transposed = [[cost[i][j] for i in range(n)] for j in range(m)]
        for maximize in (False, True):
            total, assignment = solution.hungarian(cost, maximize)
            assert total == brute(transposed, maximize), (cost, maximize)
            assert_valid_assignment(cost, assignment, total)
            assert assignment.count(-1) == n - m


def test_dual_certificate_proves_optimality():
    rng = random.Random(2)
    for _ in range(300):
        n = rng.randint(1, 6)
        m = rng.randint(1, 7)
        cost = [[rng.randint(-9, 25) for _ in range(m)] for _ in range(n)]
        for maximize in (False, True):
            total, assignment, u, v = solution.hungarian_duals(cost, maximize)
            sign = -1 if maximize else 1
            for i in range(n):
                for j in range(m):
                    assert sign * (u[i] + v[j]) <= sign * cost[i][j], (cost, maximize)  # 쌍대 가능성
            for i, j in enumerate(assignment):
                if j >= 0:
                    assert u[i] + v[j] == cost[i][j]  # 배정된 칸에서 등호 (여유 없음)
            used = {j for j in assignment if j >= 0}
            if n <= m:
                assert all(v[j] == 0 for j in range(m) if j not in used)
            else:
                assert all(u[i] == 0 for i in range(n) if assignment[i] < 0)
            assert sum(u) + sum(v) == total  # 쌍대 목적값 = 원 문제의 최적값 (약 쌍대성)


def test_forbidden_entries():
    cost = [[None, 3, 5], [2, None, 4], [7, 1, None]]
    total, assignment = solution.hungarian(cost)
    assert total == brute(cost) == 5 + 2 + 1 and all(cost[i][j] is not None for i, j in enumerate(assignment))
    assert solution.hungarian(cost, maximize=True)[0] == brute(cost, maximize=True)
    with pytest.raises(ValueError, match="배정"):
        solution.hungarian([[None, None], [1, 2]])
    with pytest.raises(ValueError, match="배정"):
        solution.hungarian([[1, None], [2, None]])
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randint(1, 5)
        m = rng.randint(n, 6)
        cost = [[None if rng.random() < 0.35 else rng.randint(-5, 15) for _ in range(m)] for _ in range(n)]
        expected = brute(cost)
        if expected is None:
            with pytest.raises(ValueError):
                solution.hungarian(cost)
        else:
            assert solution.hungarian(cost)[0] == expected, cost


def test_ties_and_degenerate_shapes():
    assert solution.hungarian([]) == (0, [])
    assert solution.hungarian([[5]]) == (5, [0])
    assert solution.hungarian([[3, 1, 2]]) == (1, [1])
    total, assignment = solution.hungarian([[4], [2], [9]])
    assert total == 2 and assignment == [-1, 0, -1]
    total, assignment = solution.hungarian([[1] * 4 for _ in range(4)])
    assert total == 4 and sorted(assignment) == [0, 1, 2, 3]
    assert solution.hungarian([[], []]) == (0, [-1, -1])
    with pytest.raises(ValueError, match="열의 수"):
        solution.hungarian([[1, 2], [3]])


def test_fractions_and_floats_work():
    cost = [[Fraction(1, 2), Fraction(3, 4)], [Fraction(2, 3), Fraction(1, 6)]]
    total, assignment = solution.hungarian(cost)
    assert total == Fraction(2, 3) and assignment == [0, 1]  # 1/2 + 1/6
    total, _ = solution.hungarian([[0.5, 1.5], [2.5, 0.25]])
    assert total == 0.75


def test_bottleneck_assignment_matches_permutations():
    rng = random.Random(4)
    for _ in range(400):
        n = rng.randint(1, 6)
        m = rng.randint(n, 7)
        cost = [[rng.randint(0, 12) for _ in range(m)] for _ in range(n)]
        expected = min(max(cost[i][columns[i]] for i in range(n)) for columns in itertools.permutations(range(m), n))
        value, assignment = solution.bottleneck_assignment(cost)
        assert value == expected and len(set(assignment)) == n
        assert max(cost[i][assignment[i]] for i in range(n)) == value
    assert solution.bottleneck_assignment([]) == (0, [])
    with pytest.raises(ValueError, match="행 수"):
        solution.bottleneck_assignment([[1], [2]])


def test_large_matrix_is_fast():
    rng = random.Random(5)
    n = 150
    cost = [[rng.randint(0, 10**6) for _ in range(n)] for _ in range(n)]
    started = time.perf_counter()
    total, assignment, u, v = solution.hungarian_duals(cost)
    assert time.perf_counter() - started < 30
    assert sorted(assignment) == list(range(n)) and sum(u) + sum(v) == total
    assert all(u[i] + v[j] <= cost[i][j] for i in range(n) for j in range(n))


def test_main_assignment_problem_format(monkeypatch, capsys):
    text = "3\n4 2 8\n2 3 7\n3 1 6\n"
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(text.encode())))
    solution.main()
    out = capsys.readouterr().out.split("\n")
    total, assignment = int(out[0]), list(map(int, out[1].split()))
    cost = [[4, 2, 8], [2, 3, 7], [3, 1, 6]]
    assert total == brute(cost) == 10 and sum(cost[i][j] for i, j in enumerate(assignment)) == total
