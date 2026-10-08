"""solution.py 검증: 파이썬 리스트·정렬된 리스트를 쓰는 순진한 방법과 무작위 연산 열로 비교하고, 트립의 불변식(힙 순서·크기·합)을 확인"""
import io
import random
import time
from bisect import bisect_left, bisect_right, insort

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def depth(treap):
    best, stack = 0, [(treap.root, 1)] if treap.root else []
    while stack:
        t, d = stack.pop()
        best = max(best, d)
        treap._push(t)
        for child in (treap.left[t], treap.right[t]):
            if child:
                stack.append((child, d + 1))
    return best


def check_invariants(treap):
    """모든 지연 표시를 내려보낸 뒤 힙 순서·크기·합·최솟값이 맞는지 확인한다."""
    stack = [treap.root] if treap.root else []
    seen = 0
    while stack:
        t = stack.pop()
        treap._push(t)
        seen += 1
        l, r = treap.left[t], treap.right[t]
        for child in (l, r):
            if child:
                assert treap.priority[child] <= treap.priority[t]
                stack.append(child)
        assert treap.size[t] == treap.size[l] + treap.size[r] + 1
        assert treap.total[t] == treap.total[l] + treap.total[r] + treap.value[t]
        assert treap.low[t] == min(treap.low[l], treap.low[r], treap.value[t])
    assert seen == len(treap)


def test_build_gives_a_valid_treap_with_the_given_order():
    rng = random.Random(0)
    for n in list(range(0, 12)) + [100, 1000]:
        values = [rng.randint(-50, 50) for _ in range(n)]
        treap = solution.ImplicitTreap(values, seed=n)
        assert treap.to_list() == values and len(treap) == n
        check_invariants(treap)


def test_implicit_treap_matches_a_python_list():
    rng = random.Random(1)
    for trial in range(120):
        values = [rng.randint(-20, 20) for _ in range(rng.randint(0, 12))]
        treap = solution.ImplicitTreap(values, seed=trial)
        for _ in range(60):
            n = len(values)
            op = rng.choice(["insert", "erase", "get", "reverse", "add", "sum", "min", "move"])
            if op == "insert":
                i, v = rng.randint(0, n), rng.randint(-20, 20)
                values.insert(i, v)
                treap.insert(i, v)
            elif op == "erase" and n:
                i = rng.randrange(n)
                assert treap.erase(i) == values.pop(i)
            elif op == "get" and n:
                i = rng.randrange(n)
                assert treap.get(i) == treap[i] == values[i]
            elif op in ("reverse", "add", "sum", "min", "move"):
                left = rng.randint(0, n)
                right = rng.randint(left, n)
                if op == "reverse":
                    values[left:right] = values[left:right][::-1]
                    treap.reverse(left, right)
                elif op == "add":
                    d = rng.randint(-5, 5)
                    values[left:right] = [v + d for v in values[left:right]]
                    treap.add(left, right, d)
                elif op == "sum":
                    assert treap.range_sum(left, right) == sum(values[left:right])
                elif op == "min" and right > left:
                    assert treap.range_min(left, right) == min(values[left:right])
                elif op == "move":
                    to = rng.randint(0, n - (right - left))
                    piece = values[left:right]
                    rest = values[:left] + values[right:]
                    values = rest[:to] + piece + rest[to:]
                    treap.move(left, right, to)
            if rng.random() < 0.1:  # 매번 전체를 훑으면 지연 표시가 전부 내려가 버려 읽기 경로의 버그를 가린다
                assert treap.to_list() == values
        assert treap.to_list() == values
        check_invariants(treap)


def test_pending_tags_are_honoured_by_every_read_path():
    rng = random.Random(11)
    for trial in range(200):
        n = rng.randint(1, 40)
        values = [rng.randint(-9, 9) for _ in range(n)]
        for reader in ("get", "range_sum", "range_min", "erase", "insert", "to_list"):
            treap = solution.ImplicitTreap(values, seed=trial)
            mirror = list(values)
            for _ in range(rng.randint(1, 3)):  # 태그를 남기는 연산만 한 뒤, 읽는 경로 하나만 쓴다
                left = rng.randint(0, n)
                right = rng.randint(left, n)
                if rng.random() < 0.5:
                    treap.reverse(left, right)
                    mirror[left:right] = mirror[left:right][::-1]
                else:
                    delta = rng.randint(-5, 5)
                    treap.add(left, right, delta)
                    mirror[left:right] = [v + delta for v in mirror[left:right]]
            i = rng.randrange(n)
            if reader == "get":
                assert [treap.get(j) for j in range(n)] == mirror
            elif reader == "range_sum":
                assert treap.range_sum(0, n) == sum(mirror) and treap.range_sum(i, n) == sum(mirror[i:])
            elif reader == "range_min":
                assert treap.range_min(0, n) == min(mirror)
            elif reader == "erase":
                assert treap.erase(i) == mirror.pop(i) and treap.to_list() == mirror
            elif reader == "insert":
                treap.insert(i, 99)
                mirror.insert(i, 99)
                assert treap.to_list() == mirror
            else:
                assert treap.to_list() == mirror


def test_reverse_twice_and_nested_lazy_tags_compose():
    treap = solution.ImplicitTreap(list(range(10)))
    treap.reverse(0, 10)
    treap.reverse(0, 10)
    assert treap.to_list() == list(range(10))
    treap.add(2, 8, 100)
    treap.reverse(3, 9)
    treap.add(0, 10, 1)
    treap.reverse(0, 5)
    expected = list(range(10))
    expected[2:8] = [v + 100 for v in expected[2:8]]
    expected[3:9] = expected[3:9][::-1]
    expected = [v + 1 for v in expected]
    expected[0:5] = expected[0:5][::-1]
    assert treap.to_list() == expected
    assert treap.range_sum(0, 10) == sum(expected) and treap.range_min(1, 6) == min(expected[1:6])


def test_implicit_treap_errors_and_slot_reuse():
    treap = solution.ImplicitTreap([5, 6, 7])
    with pytest.raises(IndexError):
        treap.get(3)
    with pytest.raises(IndexError):
        treap.erase(-1)
    with pytest.raises(IndexError):
        treap.insert(4, 0)
    with pytest.raises(IndexError):
        treap.reverse(2, 5)
    with pytest.raises(IndexError):
        treap.reverse(2, 1)
    with pytest.raises(ValueError, match="빈 구간"):
        treap.range_min(1, 1)
    with pytest.raises(IndexError):
        treap.move(0, 2, 2)  # 남은 길이는 1 이므로 to 는 0 또는 1
    assert treap.to_list() == [5, 6, 7]  # 오류 뒤에도 그대로
    nodes_before = len(treap.value)
    for _ in range(50):  # 지운 노드 자리를 다시 쓰므로 노드 풀이 커지지 않는다
        treap.erase(1)
        treap.insert(1, 9)
    assert len(treap.value) == nodes_before and treap.to_list() == [5, 9, 7]
    assert solution.ImplicitTreap().to_list() == [] and len(solution.ImplicitTreap()) == 0
    treap.append(1)
    assert treap.to_list() == [5, 9, 7, 1]


def test_multiset_matches_a_sorted_list():
    rng = random.Random(2)
    for trial in range(120):
        values = sorted(rng.randint(-10, 10) for _ in range(rng.randint(0, 10)))
        multiset = solution.OrderedMultiset(values, seed=trial)
        for _ in range(80):
            x = rng.randint(-12, 12)
            op = rng.choice(["add", "remove", "query", "pop"])
            if op == "add":
                insort(values, x)
                multiset.add(x)
            elif op == "remove":
                expected = x in values
                if expected:
                    values.remove(x)
                assert multiset.remove(x) is expected
            elif op == "pop" and values:
                if rng.random() < 0.5:
                    assert multiset.pop_min() == values.pop(0)
                else:
                    assert multiset.pop_max() == values.pop()
            assert multiset.to_list() == values and len(multiset) == len(values)
            assert multiset.rank(x) == bisect_left(values, x)
            assert multiset.count_at_most(x) == bisect_right(values, x)
            assert multiset.count(x) == values.count(x) and (x in multiset) == (x in values)
            assert multiset.predecessor(x) == max((v for v in values if v < x), default=None)
            assert multiset.floor(x) == max((v for v in values if v <= x), default=None)
            assert multiset.successor(x) == min((v for v in values if v > x), default=None)
            assert multiset.ceil(x) == min((v for v in values if v >= x), default=None)
            if values:
                k = rng.randint(1, len(values))
                assert multiset.kth_smallest(k) == values[k - 1] and multiset[k - 1] == values[k - 1]
        check_invariants(multiset)


def test_multiset_errors():
    multiset = solution.OrderedMultiset([3, 1, 2])
    assert multiset.to_list() == [1, 2, 3]
    with pytest.raises(IndexError):
        multiset.kth_smallest(0)
    with pytest.raises(IndexError):
        multiset.kth_smallest(4)
    empty = solution.OrderedMultiset()
    with pytest.raises(IndexError):
        empty.pop_min()
    with pytest.raises(IndexError):
        empty.pop_max()
    assert empty.remove(1) is False and empty.floor(1) is None and empty.ceil(1) is None


def test_depth_stays_logarithmic_even_for_sorted_insertions():
    treap = solution.ImplicitTreap(seed=5)
    for i in range(20000):
        treap.append(i)  # 정렬된 순서로 넣어도 우선순위가 무작위라 기울지 않는다
    assert treap.to_list()[:3] == [0, 1, 2]
    assert depth(treap) <= 60  # 기대 깊이는 약 2·ln(20000) ≈ 20, 최대도 이 근처
    multiset = solution.OrderedMultiset(seed=6)
    for i in range(20000):
        multiset.add(i)
    assert depth(multiset) <= 60


def test_large_random_sequence_is_fast():
    rng = random.Random(3)
    n = 100000
    values = [rng.randint(-10**6, 10**6) for _ in range(n)]
    started = time.perf_counter()
    treap = solution.ImplicitTreap(values)
    mirror = list(values)
    for _ in range(20000):
        left = rng.randrange(n)
        right = rng.randint(left, n)
        if rng.random() < 0.5:
            treap.reverse(left, right)
            mirror[left:right] = mirror[left:right][::-1]
        else:
            assert treap.range_sum(left, right) == sum(mirror[left:right])
    assert time.perf_counter() - started < 60
    assert treap.to_list() == mirror


def test_main_range_reverse_range_sum_format(monkeypatch, capsys):
    text = "5 4\n1 2 3 4 5\n1 0 5\n0 1 4\n1 0 2\n1 1 4\n"
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(text.encode())))
    solution.main()
    # 합 15, [1,4,3,2,5] 로 뒤집은 뒤 [0,2) 합 5, [1,4) 합 9
    assert capsys.readouterr().out == "15\n5\n9\n"
