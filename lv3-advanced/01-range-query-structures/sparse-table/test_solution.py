"""solution.py 검증: 모든 구간 [left, right) 를 직접 계산한 값과 비교"""
import functools
import io
import math
import random

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def all_ranges(n):
    return [(left, right) for left in range(n) for right in range(left + 1, n + 1)]


def test_idempotent_operations_match_naive_for_every_range():
    rng = random.Random(0)
    operations = [min, max, math.gcd, lambda a, b: a & b, lambda a, b: a | b]
    for op in operations:
        for _ in range(60):
            n = rng.randint(1, 40)
            values = [rng.randint(0, 60) for _ in range(n)]
            table = solution.SparseTable(values, op)
            for left, right in all_ranges(n):
                assert table.query(left, right) == functools.reduce(op, values[left:right]), (values, left, right)


def test_table_shape():
    table = solution.SparseTable(list(range(10)))
    assert [len(row) for row in table.table] == [10, 9, 7, 3]  # 길이 1, 2, 4, 8 구간의 시작 위치 개수
    assert solution.SparseTable([]).table == [[]]


def test_sum_is_not_idempotent_so_sparse_table_double_counts():
    table = solution.SparseTable([1, 2, 3], lambda a, b: a + b)
    assert table.query(0, 3) == 8  # [0,2) 와 [1,3) 이 겹쳐 가운데 2 가 두 번 더해진다 (진짜 합은 6)
    disjoint = solution.DisjointSparseTable([1, 2, 3], lambda a, b: a + b)
    assert disjoint.query(0, 3) == 6


def test_range_argmin_returns_leftmost_minimum():
    rng = random.Random(1)
    for _ in range(200):
        values = [rng.randint(0, 5) for _ in range(rng.randint(1, 30))]
        argmin = solution.RangeArgmin(values)
        for left, right in all_ranges(len(values)):
            window = values[left:right]
            assert argmin.query(left, right) == left + window.index(min(window)), (values, left, right)


def test_range_gcd_table():
    table = solution.range_gcd_table([12, 18, 24, 36, 5])
    assert table.query(0, 4) == 6 and table.query(1, 3) == 6 and table.query(0, 5) == 1 and table.query(4, 5) == 5


def test_disjoint_sparse_table_matches_naive_for_associative_operations():
    rng = random.Random(2)
    for n in list(range(1, 40)) + [64, 65]:
        values = [rng.randint(1, 9) for _ in range(n)]
        for op in (lambda a, b: a + b, lambda a, b: a * b % 1000003, min):
            table = solution.DisjointSparseTable(values, op)
            for left, right in all_ranges(n):
                assert table.query(left, right) == functools.reduce(op, values[left:right]), (n, left, right)


def test_disjoint_sparse_table_keeps_order_for_non_commutative_operation():
    rng = random.Random(3)
    for n in range(1, 40):
        words = [rng.choice("abcdef") for _ in range(n)]
        table = solution.DisjointSparseTable(words, lambda a, b: a + b)
        for left, right in all_ranges(n):
            assert table.query(left, right) == "".join(words[left:right]), (words, left, right)


def test_empty_and_invalid_ranges_are_rejected():
    for table in (solution.SparseTable([1, 2, 3]), solution.DisjointSparseTable([1, 2, 3], min)):
        for left, right in [(1, 1), (2, 1), (-1, 2), (0, 4)]:
            with pytest.raises(ValueError, match="비어 있지 않은"):
                table.query(left, right)
    assert solution.DisjointSparseTable([], min).n == 0  # 빈 배열도 만들 수는 있다


def test_large_input_is_fast():
    rng = random.Random(4)
    n = 200_000
    values = [rng.randint(0, 10**9) for _ in range(n)]
    table = solution.SparseTable(values)
    for _ in range(200_000):
        left = rng.randrange(n)
        right = rng.randint(left + 1, min(n, left + 50))
        assert table.query(left, right) == min(values[left:right])
    assert table.query(0, n) == min(values)


def test_main(monkeypatch, capsys):
    text = "5 4\n2\n5\n1\n4\n3\n1 2\n2 3\n4 5\n1 5\n"
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(text.encode())))
    solution.main()
    assert capsys.readouterr().out.split() == ["2", "1", "3", "1"]
