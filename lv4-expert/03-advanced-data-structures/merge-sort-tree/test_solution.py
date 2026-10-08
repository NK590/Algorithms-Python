"""solution.py 검증: 구간을 직접 잘라 세고 정렬하는 순진한 방법과 무작위 배열·질의·갱신으로 비교"""
import io
import random
import time

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def random_range(rng, n):
    left = rng.randint(0, n)
    return left, rng.randint(left, n)


def test_counts_predecessor_successor_and_sums_match_brute_force():
    rng = random.Random(0)
    for _ in range(150):
        n = rng.randint(0, 30)
        values = [rng.randint(-8, 8) for _ in range(n)]
        tree = solution.MergeSortTree(values)
        for _ in range(40):
            left, right = random_range(rng, n)
            piece = values[left:right]
            x = rng.randint(-10, 10)
            assert tree.count_less(left, right, x) == sum(1 for v in piece if v < x)
            assert tree.count_at_most(left, right, x) == sum(1 for v in piece if v <= x)
            low, high = sorted((rng.randint(-10, 10), rng.randint(-10, 10)))
            assert tree.count_in_value_range(left, right, low, high) == sum(1 for v in piece if low <= v <= high)
            assert tree.count_in_value_range(left, right, high + 1, low) == 0  # low > high 인 범위는 비어 있다
            assert tree.predecessor(left, right, x) == max((v for v in piece if v < x), default=None)
            assert tree.successor(left, right, x) == min((v for v in piece if v > x), default=None)
            assert tree.sum_less(left, right, x) == sum(v for v in piece if v < x)


def test_kth_smallest_matches_sorting():
    rng = random.Random(1)
    for _ in range(120):
        n = rng.randint(1, 30)
        values = [rng.randint(-8, 8) for _ in range(n)]
        tree = solution.MergeSortTree(values)
        for _ in range(30):
            left = rng.randrange(n)
            right = rng.randint(left + 1, n)
            k = rng.randint(1, right - left)
            assert tree.kth_smallest(left, right, k) == sorted(values[left:right])[k - 1], (values, left, right, k)
    with pytest.raises(ValueError, match="k 가"):
        solution.MergeSortTree([1, 2, 3]).kth_smallest(0, 3, 4)
    with pytest.raises(ValueError, match="k 가"):
        solution.MergeSortTree([1, 2, 3]).kth_smallest(0, 3, 0)


def test_updates_keep_every_query_correct():
    rng = random.Random(2)
    for _ in range(80):
        n = rng.randint(1, 25)
        values = [rng.randint(-8, 8) for _ in range(n)]
        tree = solution.MergeSortTree(values)
        for _ in range(60):
            if rng.random() < 0.4:
                index, value = rng.randrange(n), rng.randint(-8, 8)
                values[index] = value
                tree.update(index, value)
                assert tree.sorted_values == sorted(values)  # 전체 정렬 목록도 갱신된다 (kth_smallest 의 이분 탐색이 쓴다)
            else:
                left, right = random_range(rng, n)
                x = rng.randint(-10, 10)
                piece = values[left:right]
                assert tree.count_less(left, right, x) == sum(1 for v in piece if v < x), (values, left, right, x)
                assert tree.sum_less(left, right, x) == sum(v for v in piece if v < x)
                if right > left:
                    k = rng.randint(1, right - left)
                    assert tree.kth_smallest(left, right, k) == sorted(piece)[k - 1]


def test_bounds_and_empty_ranges():
    tree = solution.MergeSortTree([3, 1, 2])
    assert tree.count_less(1, 1, 100) == 0 and tree.predecessor(2, 2, 5) is None and tree.sum_less(0, 0, 5) == 0
    with pytest.raises(IndexError, match="구간"):
        tree.count_less(0, 4, 1)
    with pytest.raises(IndexError, match="구간"):
        tree.count_less(2, 1, 1)
    with pytest.raises(IndexError, match="index 가"):
        tree.update(3, 0)
    with pytest.raises(IndexError, match="index 가"):
        tree.update(-1, 0)
    empty = solution.MergeSortTree([])
    assert empty.count_less(0, 0, 1) == 0


def test_node_lists_are_sorted_and_cover_exactly_their_range():
    rng = random.Random(3)
    values = [rng.randint(0, 50) for _ in range(37)]
    tree = solution.MergeSortTree(values)
    assert tree.tree[1] == sorted(values)
    for node in range(1, 2 * tree.size):
        assert tree.tree[node] == sorted(tree.tree[node])


def test_large_input_is_fast():
    rng = random.Random(4)
    n = 100000
    values = [rng.randint(-10**9, 10**9) for _ in range(n)]
    started = time.perf_counter()
    tree = solution.MergeSortTree(values)
    for _ in range(20000):
        left = rng.randrange(n)
        right = rng.randint(left + 1, n)
        tree.count_less(left, right, rng.randint(-10**9, 10**9))
    assert time.perf_counter() - started < 30
    left, right = 100, 40000
    x = 12345
    assert tree.count_less(left, right, x) == sum(1 for v in values[left:right] if v < x)


def test_main_decodes_the_xor_with_the_previous_answer(monkeypatch, capsys):
    text = "5\n5 1 2 3 4\n3\n1 5 0\n7 1 7\n0 0 5\n"
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(text.encode())))
    solution.main()
    assert capsys.readouterr().out == "5\n1\n1\n"
