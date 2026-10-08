"""solution.py 검증: 구간의 모든 원소를 직접 고치고 더하는 순진한 방법과 무작위 갱신·질의로 비교"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def random_range(rng, n):
    left = rng.randint(0, n)
    return left, rng.randint(left, n)


def test_range_add_range_sum_matches_plain_list():
    rng = random.Random(0)
    for _ in range(300):
        n = rng.randint(0, 20)
        values = [rng.randint(-9, 9) for _ in range(n)]
        tree = solution.range_add_range_sum(values)
        for _ in range(40):
            left, right = random_range(rng, n)
            if rng.random() < 0.5:
                d = rng.randint(-9, 9)
                for i in range(left, right):
                    values[i] += d
                tree.update(left, right, d)
            assert tree.query(left, right) == sum(values[left:right]), (values, left, right)
    # 겹치는 갱신 뒤의 질의
    tree = solution.range_add_range_sum([0] * 8)
    tree.update(0, 8, 1)
    tree.update(2, 6, 10)
    tree.update(4, 5, 100)
    assert [tree.get(i) for i in range(8)] == [1, 1, 11, 11, 111, 11, 1, 1]
    assert tree.query(0, 8) == 148


def test_range_add_range_min_matches_plain_list():
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(1, 20)
        values = [rng.randint(-9, 9) for _ in range(n)]
        tree = solution.range_add_range_min(values)
        for _ in range(40):
            left, right = random_range(rng, n)
            if rng.random() < 0.5:
                d = rng.randint(-9, 9)
                for i in range(left, right):
                    values[i] += d
                tree.update(left, right, d)
            expected = min(values[left:right], default=float("inf"))
            assert tree.query(left, right) == expected, (values, left, right)


def test_range_assign_range_sum_matches_plain_list():
    rng = random.Random(2)
    for _ in range(300):
        n = rng.randint(1, 20)
        values = [rng.randint(-9, 9) for _ in range(n)]
        tree = solution.range_assign_range_sum(values)
        for _ in range(40):
            left, right = random_range(rng, n)
            if rng.random() < 0.5:
                v = rng.randint(-9, 9)
                for i in range(left, right):
                    values[i] = v
                tree.update(left, right, v)
            assert tree.query(left, right) == sum(values[left:right]), (values, left, right)
    # 0 으로 대입하는 것도 '대입' 이다 (None 이 '아무것도 안 함')
    tree = solution.range_assign_range_sum([5, 5, 5, 5])
    tree.update(1, 3, 0)
    assert [tree.get(i) for i in range(4)] == [5, 0, 0, 5]


def test_non_commutative_affine_updates():
    """갱신 (a, b) 는 x → a·x + b. 합성 순서가 틀리면 결과가 달라지는 대표적인 비가환 갱신."""
    tree_factory = lambda values: solution.LazySegmentTree(
        values,
        op=lambda x, y: x + y,
        identity=0,
        apply=lambda f, x, length: f[0] * x + f[1] * length,
        compose=lambda f, g: (f[0] * g[0], f[0] * g[1] + f[1]),
        lazy_identity=(1, 0),
    )
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randint(1, 16)
        values = [rng.randint(-5, 5) for _ in range(n)]
        tree = tree_factory(values)
        for _ in range(30):
            left, right = random_range(rng, n)
            if rng.random() < 0.6:
                a, b = rng.randint(-2, 2), rng.randint(-3, 3)
                for i in range(left, right):
                    values[i] = a * values[i] + b
                tree.update(left, right, (a, b))
            assert tree.query(left, right) == sum(values[left:right]), (values, left, right)


def test_empty_tree_and_empty_ranges():
    empty = solution.range_add_range_sum([])
    empty.update(0, 0, 5)
    assert empty.query(0, 0) == 0
    tree = solution.range_add_range_sum([1, 2, 3])
    tree.update(1, 1, 100)  # 빈 구간 갱신은 아무 일도 하지 않는다
    assert tree.query(0, 3) == 6 and tree.query(2, 2) == 0


def test_large_input_is_fast():
    rng = random.Random(4)
    n = 50_000
    tree = solution.range_add_range_sum([0] * n)
    total_added = 0
    for _ in range(20_000):
        left = rng.randrange(n)
        right = rng.randint(left + 1, n)
        tree.update(left, right, 1)
        total_added += right - left
        assert tree.query(left, right) >= right - left
    assert tree.query(0, n) == total_added


def test_main(monkeypatch, capsys):
    text = "5 1 1\n1\n2\n3\n4\n5\n1 3 4 6\n2 2 5\n"
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(text.encode())))
    solution.main()
    assert capsys.readouterr().out.split() == ["26"]
