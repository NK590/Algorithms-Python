"""solution.py 검증: 배열을 직접 고치고 잘라 세는 순진한 방법과 무작위 연산 열로 비교"""
import io
import random
import time

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def random_range(rng, n):
    left = rng.randint(0, n)
    return left, rng.randint(left, n)


def test_sqrt_sum_matches_naive_for_every_block_size():
    rng = random.Random(0)
    for _ in range(400):
        n = rng.randint(0, 30)
        a = [rng.randint(-9, 9) for _ in range(n)]
        block = rng.choice([None, 1, 2, 3, 5, 7, 40])
        tree, naive = solution.SqrtSum(a, block), list(a)
        for _ in range(40):
            left, right = random_range(rng, n)
            if rng.random() < 0.5:
                value = rng.randint(-5, 5)
                tree.add(left, right, value)
                for i in range(left, right):
                    naive[i] += value
            else:
                assert tree.sum(left, right) == sum(naive[left:right]), (a, block, left, right)
        assert [tree.get(i) for i in range(n)] == naive


def test_sqrt_sum_boundaries_and_errors():
    tree = solution.SqrtSum([1, 2, 3, 4, 5, 6, 7, 8, 9], block=3)
    assert tree.sum(0, 9) == 45 and tree.sum(3, 6) == 15 and tree.sum(2, 7) == 25 and tree.sum(4, 4) == 0
    tree.add(2, 7, 10)  # 블록 경계를 넘는 구간 (조각 + 온전한 블록 + 조각)
    assert tree.sum(0, 9) == 95 and tree.sum(3, 6) == 45 and tree.get(2) == 13 and tree.get(7) == 8
    tree.add(3, 6, 1)  # 정확히 블록 하나
    assert tree.sum(3, 6) == 48 and tree.sum(0, 9) == 98
    tree.add(5, 5, 100)  # 빈 구간은 아무것도 바꾸지 않는다
    assert tree.sum(0, 9) == 98
    for bad in [(-1, 3), (3, 2), (0, 10)]:
        with pytest.raises(ValueError, match="벗어났습니다"):
            tree.sum(*bad)
        with pytest.raises(ValueError, match="벗어났습니다"):
            tree.add(bad[0], bad[1], 1)
    empty = solution.SqrtSum([])
    assert empty.sum(0, 0) == 0


def test_sqrt_count_greater_matches_naive():
    rng = random.Random(1)
    for _ in range(400):
        n = rng.randint(0, 30)
        a = [rng.randint(0, 9) for _ in range(n)]
        block = rng.choice([None, 1, 2, 3, 5, 7, 40])
        structure, naive = solution.SqrtCountGreater(a, block), list(a)
        for _ in range(40):
            if n and rng.random() < 0.4:
                i, value = rng.randrange(n), rng.randint(0, 9)
                structure.update(i, value)
                naive[i] = value
            else:
                left, right = random_range(rng, n)
                k = rng.randint(-1, 10)
                assert structure.count_greater(left, right, k) == sum(1 for x in naive[left:right] if x > k), (a, block, left, right, k)


def test_sqrt_count_greater_equal_values_and_errors():
    structure = solution.SqrtCountGreater([5, 5, 5, 5, 5, 5], block=2)
    assert structure.count_greater(0, 6, 5) == 0 and structure.count_greater(0, 6, 4) == 6
    structure.update(3, 9)
    structure.update(3, 9)  # 같은 값으로 두 번 바꿔도 정렬된 복사본이 어긋나지 않는다
    assert structure.count_greater(0, 6, 5) == 1 and structure.count_greater(3, 4, 8) == 1 and structure.count_greater(0, 3, 0) == 3
    with pytest.raises(ValueError, match="벗어났습니다"):
        structure.count_greater(0, 7, 0)
    with pytest.raises(ValueError, match="벗어났습니다"):
        structure.count_greater(4, 3, 0)


def test_default_block_size():
    assert solution.default_block_size(0) == 1 and solution.default_block_size(1) == 1
    assert solution.default_block_size(99) == 9 and solution.default_block_size(100) == 10


def test_large_inputs_run_fast():
    rng = random.Random(2)
    n = q = 100000
    a = [rng.randint(0, 10**9) for _ in range(n)]
    sums, greater = solution.SqrtSum(a), solution.SqrtCountGreater(a)
    started = time.perf_counter()
    for _ in range(q // 2):
        left, right = random_range(rng, n)
        sums.add(left, right, rng.randint(-5, 5))
        left, right = random_range(rng, n)
        sums.sum(left, right)
    assert time.perf_counter() - started < 20
    started = time.perf_counter()
    for _ in range(q // 2):
        greater.update(rng.randrange(n), rng.randint(0, 10**9))
        left, right = random_range(rng, n)
        greater.count_greater(left, right, rng.randint(0, 10**9))
    assert time.perf_counter() - started < 20


def test_main_handles_updates_and_queries(monkeypatch, capsys):
    text = "5\n1 2 3 4 5\n6\n2 1 5 2\n1 3 10\n2 1 5 5\n2 2 3 9\n2 4 4 5\n2 1 1 0\n"
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(text.encode())))
    solution.main()
    assert capsys.readouterr().out == "3\n1\n1\n0\n1\n"
