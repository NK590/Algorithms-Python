"""solution.py 검증: 버전마다 배열을 통째로 복사해 두는 순진한 방법, 정렬한 구간과 무작위 연산으로 비교"""
import io
import random
import time

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def test_versions_match_full_copies_including_branching_from_old_versions():
    rng = random.Random(0)
    for _ in range(80):
        n = rng.randint(1, 20)
        tree = solution.PersistentSegmentTree(n)
        snapshots = {0: [0] * n}
        for _ in range(50):
            version = rng.choice(list(snapshots))  # 어느 과거 버전에서든 갈라져 나갈 수 있다
            if rng.random() < 0.6:
                index, delta = rng.randrange(n), rng.randint(-5, 5)
                new_version = tree.update(version, index, delta)
                copy = list(snapshots[version])
                copy[index] += delta
                snapshots[new_version] = copy
            else:
                left = rng.randint(0, n)
                right = rng.randint(left, n)
                assert tree.query(version, left, right) == sum(snapshots[version][left:right]), (n, version, left, right)
        for version, copy in snapshots.items():  # 옛 버전은 하나도 변하지 않았다
            assert [tree.query(version, i, i + 1) for i in range(n)] == copy


def test_each_update_adds_only_a_logarithmic_number_of_nodes():
    for n in (1, 2, 3, 7, 8, 100, 1024):
        tree = solution.PersistentSegmentTree(n)
        before = tree.node_count()
        tree.update(0, n // 2, 1)
        added = tree.node_count() - before
        assert added <= (n - 1).bit_length() + 1, (n, added)
        assert added >= 1
    tree = solution.PersistentSegmentTree(1024)
    version = 0
    for i in range(1000):
        version = tree.update(version, i % 1024, 1)
    assert tree.node_count() <= 1 + 1000 * 11  # 갱신 1000 번 × (깊이 10 + 1)


def test_range_errors():
    tree = solution.PersistentSegmentTree(5)
    with pytest.raises(IndexError, match="index 가"):
        tree.update(0, 5, 1)
    with pytest.raises(IndexError, match="index 가"):
        tree.update(0, -1, 1)
    with pytest.raises(IndexError, match="구간"):
        tree.query(0, 3, 6)
    with pytest.raises(IndexError, match="구간"):
        tree.query(0, 4, 3)
    with pytest.raises(ValueError, match="n 은"):
        solution.PersistentSegmentTree(0)
    assert tree.query(0, 2, 2) == 0


def test_persistent_array_gets_sets_and_branches():
    rng = random.Random(1)
    for _ in range(60):
        n = rng.randint(1, 15)
        values = [rng.randint(-9, 9) for _ in range(n)]
        array = solution.PersistentArray(values)
        snapshots = {array.initial_version: list(values)}
        assert all(array.get(array.initial_version, i) == values[i] for i in range(n))
        for _ in range(40):
            version = rng.choice(list(snapshots))
            index, value = rng.randrange(n), rng.randint(-9, 9)
            new_version = array.set(version, index, value)
            copy = list(snapshots[version])
            copy[index] = value
            snapshots[new_version] = copy
        for version, copy in snapshots.items():
            assert [array.get(version, i) for i in range(n)] == copy
    empty = solution.PersistentArray([])
    assert empty.length == 0


def test_kth_smallest_matches_sorting_the_slice():
    rng = random.Random(2)
    for _ in range(150):
        n = rng.randint(1, 30)
        values = [rng.randint(-10, 10) for _ in range(n)]  # 중복과 음수를 포함
        structure = solution.KthSmallest(values)
        for _ in range(40):
            left = rng.randrange(n)
            right = rng.randint(left + 1, n)
            k = rng.randint(1, right - left)
            assert structure.kth(left, right, k) == sorted(values[left:right])[k - 1], (values, left, right, k)
            x = rng.randint(-12, 12)
            assert structure.count_less(left, right, x) == sum(1 for v in values[left:right] if v < x)
            assert structure.count_at_most(left, right, x) == sum(1 for v in values[left:right] if v <= x)
    with pytest.raises(ValueError, match="k 가"):
        solution.KthSmallest([1, 2, 3]).kth(0, 3, 4)
    with pytest.raises(ValueError, match="구간"):
        solution.KthSmallest([1, 2, 3]).kth(2, 2, 1)  # 빈 구간
    with pytest.raises(ValueError, match="k 가"):
        solution.KthSmallest([1, 2, 3]).kth(0, 3, 0)
    with pytest.raises(ValueError, match="구간"):
        solution.KthSmallest([1, 2, 3]).kth(0, 4, 1)


def test_kth_in_difference_error():
    tree = solution.PersistentSegmentTree(4)
    version = tree.update(0, 2, 3)
    assert tree.kth_in_difference(version, 0, 1) == 2 and tree.kth_in_difference(version, 0, 3) == 2
    with pytest.raises(ValueError, match="k 가"):
        tree.kth_in_difference(version, 0, 4)


def test_large_input_is_fast():
    rng = random.Random(3)
    n = 100000
    values = [rng.randint(-10**9, 10**9) for _ in range(n)]
    started = time.perf_counter()
    structure = solution.KthSmallest(values)
    for _ in range(20000):
        left = rng.randrange(n)
        right = rng.randint(left + 1, n)
        structure.kth(left, right, rng.randint(1, right - left))
    assert time.perf_counter() - started < 30
    for _ in range(20):  # 일부는 정렬해서 직접 확인
        left = rng.randrange(n - 1000)
        right = left + rng.randint(1, 1000)
        k = rng.randint(1, right - left)
        assert structure.kth(left, right, k) == sorted(values[left:right])[k - 1]


def test_main_matches_the_boj_7469_sample(monkeypatch, capsys):
    text = "7 3\n1 5 2 6 3 7 4\n2 5 3\n4 4 1\n1 7 3\n"
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(text.encode())))
    solution.main()
    assert capsys.readouterr().out == "5\n6\n3\n"
