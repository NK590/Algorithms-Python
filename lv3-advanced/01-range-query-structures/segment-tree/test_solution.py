"""solution.py 검증: 구간을 직접 훑는 순진한 방법과 무작위 갱신·질의로 비교"""
import functools
import io
import math
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def naive(values, op, identity, left, right):
    return functools.reduce(op, values[left:right], identity)


def test_sum_min_max_match_naive_under_random_operations():
    rng = random.Random(0)
    cases = [(lambda a, b: a + b, 0), (min, float("inf")), (max, float("-inf"))]
    for op, identity in cases:
        for _ in range(150):
            n = rng.randint(0, 20)
            values = [rng.randint(-9, 9) for _ in range(n)]
            tree = solution.SegmentTree(values, op, identity)
            for _ in range(40):
                if n and rng.random() < 0.5:
                    i, v = rng.randrange(n), rng.randint(-9, 9)
                    values[i] = v
                    tree.update(i, v)
                    assert tree.get(i) == v
                left = rng.randint(0, n)
                right = rng.randint(left, n)
                assert tree.query(left, right) == naive(values, op, identity, left, right), (values, left, right)


def test_empty_and_single_element_trees():
    tree = solution.SegmentTree([], max, float("-inf"))
    assert tree.query(0, 0) == float("-inf")
    one = solution.SegmentTree([7], max, float("-inf"))
    assert one.query(0, 1) == 7 and one.query(0, 0) == float("-inf")
    one.update(0, 3)
    assert one.query(0, 1) == 3


def test_non_commutative_operation_keeps_order():
    rng = random.Random(1)
    for _ in range(200):
        n = rng.randint(1, 20)
        words = [rng.choice("abcdef") for _ in range(n)]
        tree = solution.SegmentTree(words, lambda a, b: a + b, "")
        for _ in range(30):
            if rng.random() < 0.4:
                i, ch = rng.randrange(n), rng.choice("abcdef")
                words[i] = ch
                tree.update(i, ch)
            left = rng.randint(0, n)
            right = rng.randint(left, n)
            assert tree.query(left, right) == "".join(words[left:right]), (words, left, right)


def test_non_commutative_matrix_product():
    def mul(a, b):
        return (
            (a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]),
            (a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]),
        )

    identity = ((1, 0), (0, 1))
    rng = random.Random(2)
    for _ in range(100):
        n = rng.randint(1, 10)
        mats = [((rng.randint(0, 2), rng.randint(0, 2)), (rng.randint(0, 2), rng.randint(0, 2))) for _ in range(n)]
        tree = solution.SegmentTree(mats, mul, identity)
        for left in range(n + 1):
            for right in range(left, n + 1):
                assert tree.query(left, right) == naive(mats, mul, identity, left, right)


def kadane_in_range(values, left, right):
    best = float("-inf")
    for i in range(left, right):
        total = 0
        for j in range(i, right):
            total += values[j]
            best = max(best, total)
    return best


def test_max_subarray_tree_matches_brute_force():
    rng = random.Random(3)
    for _ in range(200):
        n = rng.randint(1, 15)
        values = [rng.randint(-9, 9) for _ in range(n)]
        tree = solution.max_subarray_tree(values)
        for _ in range(20):
            if rng.random() < 0.4:
                i, v = rng.randrange(n), rng.randint(-9, 9)
                values[i] = v
                tree.update(i, (v, v, v, v))
            left = rng.randint(0, n - 1)
            right = rng.randint(left + 1, n)
            assert tree.query(left, right)[3] == kadane_in_range(values, left, right), (values, left, right)
    # 전부 음수여도 비어 있지 않은 구간만 인정한다
    assert solution.max_subarray_tree([-5, -2, -7]).query(0, 3)[3] == -2


def test_range_gcd_tree():
    rng = random.Random(4)
    for _ in range(200):
        values = [rng.randint(0, 60) for _ in range(rng.randint(1, 15))]
        tree = solution.range_gcd_tree(values)
        for left in range(len(values) + 1):
            for right in range(left, len(values) + 1):
                assert tree.query(left, right) == functools.reduce(math.gcd, values[left:right], 0)


def test_max_right_finds_first_value_at_least_x():
    rng = random.Random(5)
    for _ in range(300):
        n = rng.randint(0, 25)
        values = [rng.randint(0, 20) for _ in range(n)]
        tree = solution.SegmentTree(values, max, -1)
        for _ in range(20):
            left = rng.randint(0, n)
            x = rng.randint(0, 22)
            expected = next((i for i in range(left, n) if values[i] >= x), n)
            assert tree.max_right(left, lambda v: v < x) == expected, (values, left, x)


def test_max_right_with_prefix_sum_limit():
    rng = random.Random(6)
    for _ in range(300):
        n = rng.randint(0, 25)
        values = [rng.randint(0, 5) for _ in range(n)]
        tree = solution.SegmentTree(values, lambda a, b: a + b, 0)
        for _ in range(20):
            left = rng.randint(0, n)
            limit = rng.randint(0, 40)
            expected = left
            total = 0
            while expected < n and total + values[expected] <= limit:
                total += values[expected]
                expected += 1
            assert tree.max_right(left, lambda s: s <= limit) == expected, (values, left, limit)


def test_large_input_is_fast():
    rng = random.Random(7)
    n = 100_000
    values = [rng.randint(0, 10**9) for _ in range(n)]
    tree = solution.SegmentTree(values, min, float("inf"))
    for _ in range(50_000):
        left = rng.randrange(n)
        right = rng.randint(left + 1, n)
        assert tree.query(left, right) <= values[left]
        i, v = rng.randrange(n), rng.randint(0, 10**9)
        values[i] = v
        tree.update(i, v)
        assert tree.query(i, i + 1) == v


def test_main(monkeypatch, capsys):
    text = "10 4\n75\n30\n100\n38\n50\n51\n52\n20\n81\n5\n1 10\n3 5\n6 9\n8 10\n"
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(text.encode())))
    solution.main()
    assert capsys.readouterr().out.strip().splitlines() == ["5 100", "38 100", "20 81", "5 81"]
    # 첫 칸이 구간에 들어가는지(1 부터 세는지)까지 확인한다
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(b"5 3\n1\n5\n4\n3\n2\n1 1\n1 5\n5 5\n")))
    solution.main()
    assert capsys.readouterr().out.strip().splitlines() == ["1 1", "1 5", "2 2"]
