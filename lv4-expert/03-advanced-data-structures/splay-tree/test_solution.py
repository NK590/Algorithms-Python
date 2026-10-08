"""solution.py 검증: 정렬된 리스트·파이썬 리스트를 쓰는 순진한 방법과 무작위 연산 열로 비교하고, 부모 포인터·크기·합의 불변식과 분할 상환 성질을 확인"""
import io
import random
import time
from bisect import bisect_left, bisect_right, insort

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def check_invariants(tree):
    """모든 지연 표시를 내려보낸 뒤 부모 포인터·크기·합이 맞는지 확인한다."""
    assert tree.parent[tree.root] == 0
    stack = [tree.root] if tree.root else []
    seen = 0
    while stack:
        x = stack.pop()
        tree._push(x)
        seen += 1
        l, r = tree.left[x], tree.right[x]
        for child in (l, r):
            if child:
                assert tree.parent[child] == x
                stack.append(child)
        assert tree.size[x] == tree.size[l] + tree.size[r] + 1
        assert tree.total[x] == tree.total[l] + tree.total[r] + tree.value[x]
    assert seen == tree.size[tree.root]


def height(tree):
    best, stack = 0, [(tree.root, 1)] if tree.root else []
    while stack:
        x, d = stack.pop()
        best = max(best, d)
        tree._push(x)
        for child in (tree.left[x], tree.right[x]):
            if child:
                stack.append((child, d + 1))
    return best


def test_set_matches_a_sorted_list():
    rng = random.Random(0)
    for _ in range(120):
        values = []
        splay = solution.SplaySet()
        for _ in range(90):
            x = rng.randint(-12, 12)
            op = rng.choice(["add", "remove", "query", "pop"])
            if op == "add":
                expected = x not in values
                if expected:
                    insort(values, x)
                assert splay.add(x) is expected
            elif op == "remove":
                expected = x in values
                if expected:
                    values.remove(x)
                assert splay.remove(x) is expected
            elif op == "pop" and values:
                assert splay.pop_min() == values.pop(0)
            assert splay.to_list() == values and len(splay) == len(values)
            assert (x in splay) == (x in values)
            assert splay.rank(x) == bisect_left(values, x)
            assert splay.predecessor(x) == max((v for v in values if v < x), default=None)
            assert splay.floor(x) == max((v for v in values if v <= x), default=None)
            assert splay.successor(x) == min((v for v in values if v > x), default=None)
            assert splay.ceil(x) == min((v for v in values if v >= x), default=None)
            if values:
                k = rng.randint(1, len(values))
                assert splay.kth_smallest(k) == values[k - 1]
                assert splay.min() == values[0] and splay.max() == values[-1]
            check_invariants(splay)


def test_set_errors_and_empty_behaviour():
    splay = solution.SplaySet([5, 1, 3, 3])
    assert splay.to_list() == [1, 3, 5]
    with pytest.raises(IndexError):
        splay.kth_smallest(0)
    with pytest.raises(IndexError):
        splay.kth_smallest(4)
    empty = solution.SplaySet()
    assert 1 not in empty and empty.rank(1) == 0 and empty.floor(1) is None and empty.ceil(1) is None
    assert empty.predecessor(1) is None and empty.successor(1) is None and empty.remove(1) is False
    with pytest.raises(IndexError):
        empty.min()
    with pytest.raises(IndexError):
        empty.max()
    with pytest.raises(IndexError):
        empty.pop_min()


def test_sequence_matches_a_python_list():
    rng = random.Random(1)
    for _ in range(120):
        values = [rng.randint(-20, 20) for _ in range(rng.randint(0, 12))]
        splay = solution.SplaySequence(values)
        for _ in range(70):
            n = len(values)
            op = rng.choice(["insert", "erase", "get", "set", "reverse", "sum"])
            if op == "insert":
                i, v = rng.randint(0, n), rng.randint(-20, 20)
                values.insert(i, v)
                splay.insert(i, v)
            elif op == "erase" and n:
                i = rng.randrange(n)
                assert splay.erase(i) == values.pop(i)
            elif op == "get" and n:
                i = rng.randrange(n)
                assert splay.get(i) == splay[i] == values[i]
            elif op == "set" and n:
                i, v = rng.randrange(n), rng.randint(-20, 20)
                values[i] = v
                splay.set(i, v)
            elif op in ("reverse", "sum"):
                left = rng.randint(0, n)
                right = rng.randint(left, n)
                if op == "reverse":
                    values[left:right] = values[left:right][::-1]
                    splay.reverse(left, right)
                else:
                    assert splay.range_sum(left, right) == sum(values[left:right])
            assert len(splay) == len(values)
            if rng.random() < 0.1:  # 매번 전체를 훑으면 지연 표시가 전부 내려가 버려 읽기 경로의 버그를 가린다
                assert splay.to_list()[1:-1] == values
        assert splay.to_list()[1:-1] == values
        check_invariants(splay)


def test_reversing_the_same_range_twice_restores_it_and_pending_tags_are_honoured():
    splay = solution.SplaySequence(list(range(10)))
    splay.reverse(2, 8)
    splay.reverse(2, 8)  # 같은 서브트리에 표시가 두 번: 뒤집기는 토글이어야 한다
    assert splay.to_list()[1:-1] == list(range(10))
    rng = random.Random(11)
    for trial in range(200):
        n = rng.randint(1, 30)
        values = [rng.randint(-9, 9) for _ in range(n)]
        for reader in ("get", "range_sum", "erase", "insert", "to_list"):
            splay = solution.SplaySequence(values)
            mirror = list(values)
            for _ in range(rng.randint(1, 4)):  # 표시를 남기는 연산만 한 뒤, 읽는 경로 하나만 쓴다
                left = rng.randint(0, n)
                right = rng.randint(left, n)
                splay.reverse(left, right)
                mirror[left:right] = mirror[left:right][::-1]
            i = rng.randrange(n)
            if reader == "get":
                assert [splay.get(j) for j in range(n)] == mirror
            elif reader == "range_sum":
                assert splay.range_sum(i, n) == sum(mirror[i:]) and splay.range_sum(0, i) == sum(mirror[:i])
            elif reader == "erase":
                assert splay.erase(i) == mirror.pop(i) and splay.to_list()[1:-1] == mirror
            elif reader == "insert":
                splay.insert(i, 99)
                mirror.insert(i, 99)
                assert splay.to_list()[1:-1] == mirror
            else:
                assert splay.to_list()[1:-1] == mirror


def test_sequence_errors_and_slot_reuse():
    splay = solution.SplaySequence([5, 6, 7])
    with pytest.raises(IndexError):
        splay.get(3)
    with pytest.raises(IndexError):
        splay.erase(3)
    with pytest.raises(IndexError):
        splay.insert(4, 0)
    with pytest.raises(IndexError):
        splay.reverse(2, 4)
    with pytest.raises(IndexError):
        splay.range_sum(2, 1)
    assert splay.to_list()[1:-1] == [5, 6, 7]
    nodes_before = len(splay.value)
    for _ in range(40):
        splay.erase(1)
        splay.insert(1, 9)
    assert len(splay.value) == nodes_before and splay.to_list()[1:-1] == [5, 9, 7]
    splay.append(2)
    assert splay.to_list()[1:-1] == [5, 9, 7, 2]
    assert len(solution.SplaySequence()) == 0


def test_set_reuses_removed_node_slots():
    splay = solution.SplaySet([1, 2, 3])
    nodes_before = len(splay.value)
    for _ in range(50):
        assert splay.remove(2) and splay.add(2)
    assert len(splay.value) == nodes_before and splay.to_list() == [1, 2, 3]


def test_zig_zig_halves_a_long_chain():
    # 오름차순으로 넣으면 왼쪽으로 기운 사슬(깊이 n)이 된다. 가장 깊은 노드를 접근했을 때
    # 올바른 zig-zig(부모를 먼저 회전) 라면 깊이가 약 절반으로 줄고, x 만 두 번 돌리면 줄지 않는다.
    n = 2000
    splay = solution.SplaySet()
    for key in range(n):
        splay.add(key)
    assert height(splay) == n
    assert 0 in splay
    assert height(splay) <= n // 2 + 2
    check_invariants(splay)


def test_sequential_access_costs_linear_total_rotations():
    # 순차 접근 정리: 키를 오름차순으로 전부 접근하는 전체 비용이 O(n). n 이 4배가 돼도 키당 회전 수는 거의 같다.
    per_key = []
    for n in (1000, 4000):
        splay = solution.SplaySet(range(n))  # 오름차순으로 넣었으므로 깊이 n 의 사슬에서 시작한다 (첫 접근 하나가 n 번 회전)
        before = splay.rotations
        for key in range(n):
            assert key in splay
        per_key.append((splay.rotations - before) / n)
    assert max(per_key) <= 5 and abs(per_key[0] - per_key[1]) < 0.5
    keys = list(range(4000))
    random.Random(7).shuffle(keys)
    splay = solution.SplaySet(keys)  # 무작위 순서로 만든 트리에서 시작
    before = splay.rotations
    for key in range(4000):
        assert key in splay
    assert (splay.rotations - before) / 4000 <= 3.5
    # 같은 키를 반복해 접근하면 처음 한 번 뒤로는 회전이 없다
    assert 123 in splay
    before = splay.rotations
    for _ in range(100):
        assert 123 in splay
    assert splay.rotations == before


def test_deep_chains_do_not_hit_the_recursion_limit_and_stay_fast():
    n = 100000
    started = time.perf_counter()
    splay = solution.SplaySet()
    for key in range(n):
        splay.add(key)
    assert splay.to_list()[:3] == [0, 1, 2] and len(splay) == n
    rng = random.Random(2)
    for _ in range(20000):
        assert rng.randrange(n) in splay
    assert time.perf_counter() - started < 60
    check_invariants(splay)


def test_large_sequence_reversals_are_fast():
    rng = random.Random(3)
    n = 50000
    values = [rng.randint(-10**6, 10**6) for _ in range(n)]
    started = time.perf_counter()
    splay = solution.SplaySequence(values)
    mirror = list(values)
    for _ in range(10000):
        left = rng.randrange(n)
        right = rng.randint(left, n)
        splay.reverse(left, right)
        mirror[left:right] = mirror[left:right][::-1]
    assert time.perf_counter() - started < 60
    assert splay.to_list()[1:-1] == mirror


def test_main_prints_the_sequence_after_the_reversals(monkeypatch, capsys):
    text = "5 3\n1 3\n3 5\n1 4\n"
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(text.encode())))
    solution.main()
    # [1,2,3,4,5] -> [3,2,1,4,5] -> [3,2,5,4,1] -> [4,5,2,3,1]
    assert capsys.readouterr().out == "4 5 2 3 1\n"
