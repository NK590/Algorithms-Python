"""solution.py 검증: 질의마다 현재 간선으로 그래프를 처음부터 다시 탐색하는 순진한 방법과 무작위 연산열로 비교"""
import io
import random
import time
from collections import Counter, deque

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def naive(n, operations):
    """간선의 다중집합을 들고 질의마다 BFS 로 처음부터 판정."""
    edges = Counter()
    answers = []

    def adjacency():
        adj = [[] for _ in range(n)]
        for (a, b), count in edges.items():
            for _ in range(count):
                adj[a].append(b)
                adj[b].append(a)
        return adj

    def explore():
        """(성분 번호, 이분 그래프 여부). 자기 루프나 같은 색을 잇는 간선이 있으면 이분 그래프가 아니다."""
        adj = adjacency()
        comp, color, bipartite, count = [-1] * n, [0] * n, True, 0
        for s in range(n):
            if comp[s] != -1:
                continue
            comp[s] = count
            queue = deque([s])
            while queue:
                v = queue.popleft()
                for to in adj[v]:
                    if comp[to] == -1:
                        comp[to], color[to] = count, color[v] ^ 1
                        queue.append(to)
                    elif color[to] == color[v]:
                        bipartite = False
            count += 1
        return comp, bipartite, count

    for op in operations:
        if op[0] == "add":
            edges[(min(op[1], op[2]), max(op[1], op[2]))] += 1
        elif op[0] == "remove":
            key = (min(op[1], op[2]), max(op[1], op[2]))
            assert edges[key] > 0
            edges[key] -= 1
        elif op[0] == "connected":
            comp, _, _ = explore()
            answers.append(comp[op[1]] == comp[op[2]])
        elif op[0] == "components":
            answers.append(explore()[2])
        else:
            answers.append(explore()[1])
    return answers


def random_operations(rng, n, count, allow_self_loops=False):
    operations, present = [], []
    for _ in range(count):
        roll = rng.random()
        if roll < 0.35 or (roll < 0.55 and not present):
            u, v = rng.randrange(n), rng.randrange(n)
            if u == v and not allow_self_loops:
                continue
            operations.append(("add", u, v))
            present.append((u, v))
        elif roll < 0.55:
            u, v = present.pop(rng.randrange(len(present)))
            operations.append(("remove", v, u) if rng.random() < 0.5 else ("remove", u, v))
        else:
            kind = rng.choice(["connected", "connected", "components", "bipartite"])
            if kind == "connected":
                operations.append(("connected", rng.randrange(n), rng.randrange(n)))
            else:
                operations.append((kind,))
    return operations


def test_small_example():
    operations = [
        ("add", 0, 1), ("add", 1, 2), ("connected", 0, 2), ("remove", 1, 2), ("connected", 0, 2),
        ("components",), ("add", 2, 0), ("add", 1, 2), ("bipartite",), ("remove", 0, 1), ("bipartite",), ("components",),
    ]
    assert solution.offline_dynamic_graph(4, operations) == [True, False, 3, False, True, 2]


def test_matches_naive_on_random_operations():
    rng = random.Random(0)
    for _ in range(600):
        n = rng.randint(1, 8)
        operations = random_operations(rng, n, rng.randint(0, 45))
        assert solution.offline_dynamic_graph(n, operations) == naive(n, operations), (n, operations)


def test_matches_naive_with_self_loops_and_multi_edges():
    rng = random.Random(1)
    for _ in range(400):
        n = rng.randint(1, 5)
        operations = random_operations(rng, n, rng.randint(0, 40), allow_self_loops=True)
        assert solution.offline_dynamic_graph(n, operations) == naive(n, operations), (n, operations)


def test_multi_edges_are_counted():
    ops = [("add", 0, 1), ("add", 1, 0), ("remove", 0, 1), ("connected", 0, 1), ("remove", 1, 0), ("connected", 0, 1)]
    assert solution.offline_dynamic_graph(2, ops) == [True, False]


def test_bipartite_toggles_with_odd_cycle():
    ops = [("add", 0, 1), ("add", 1, 2), ("bipartite",), ("add", 2, 0), ("bipartite",), ("remove", 1, 2), ("bipartite",)]
    assert solution.offline_dynamic_graph(3, ops) == [True, False, True]
    assert solution.offline_dynamic_graph(2, [("add", 0, 0), ("bipartite",), ("remove", 0, 0), ("bipartite",)]) == [False, True]


def test_edge_present_for_the_whole_timeline_and_never_removed():
    ops = [("add", 0, 1)] + [("connected", 0, 1)] * 5 + [("components",)]
    assert solution.offline_dynamic_graph(3, ops) == [True] * 5 + [2]


def test_empty_and_query_free_inputs():
    assert solution.offline_dynamic_graph(3, []) == []
    assert solution.offline_dynamic_graph(3, [("add", 0, 1), ("remove", 0, 1)]) == []
    assert solution.offline_dynamic_graph(3, [("components",)]) == [3]


def test_invalid_operations_are_rejected():
    with pytest.raises(ValueError, match="그런 간선"):
        solution.offline_dynamic_graph(3, [("remove", 0, 1)])
    with pytest.raises(ValueError, match="그런 간선"):
        solution.offline_dynamic_graph(3, [("add", 0, 1), ("remove", 0, 1), ("remove", 0, 1)])
    with pytest.raises(ValueError, match="범위"):
        solution.offline_dynamic_graph(3, [("add", 0, 3)])
    with pytest.raises(ValueError, match="범위"):
        solution.offline_dynamic_graph(3, [("connected", -1, 2)])


def test_rollback_dsu_restores_every_state():
    rng = random.Random(2)
    for _ in range(100):
        n = rng.randint(2, 12)
        dsu = solution.RollbackDSU(n)
        stack = []  # (snapshot, 그때의 (뿌리 비교 행렬, 성분 수, 홀수 사이클 수))

        def state():
            roots = [dsu.find(v) for v in range(n)]
            relation = [[(roots[a][0] == roots[b][0], roots[a][1] ^ roots[b][1]) for b in range(n)] for a in range(n)]
            return relation, dsu.components, dsu.odd_cycles

        for _ in range(40):
            action = rng.random()
            if action < 0.55:
                stack.append((dsu.snapshot(), state()))
                dsu.union(rng.randrange(n), rng.randrange(n))
            elif stack:
                snapshot, expected = stack.pop(rng.randrange(len(stack)) if rng.random() < 0.3 else -1)
                # 이후에 쌓인 스냅샷은 모두 무효
                stack = [item for item in stack if item[0] < snapshot]
                dsu.rollback(snapshot)
                assert state() == expected
        dsu.rollback(0)
        assert dsu.components == n and dsu.odd_cycles == 0 and dsu.size == [1] * n
        assert all(dsu.find(v) == (v, 0) for v in range(n))


def test_union_returns_whether_components_merged():
    dsu = solution.RollbackDSU(4)
    assert dsu.union(0, 1) is True
    assert dsu.union(1, 0) is False  # 이미 같은 성분 (색은 맞음)
    assert dsu.union(1, 2) is True
    assert dsu.union(0, 2) is False  # 0 - 1 - 2 사슬에서 0 과 2 는 같은 색 → 홀수 사이클
    assert dsu.odd_cycles == 1 and dsu.components == 2


def test_small_component_is_attached_under_the_large_one():
    n = 1 << 10
    dsu = solution.RollbackDSU(n)
    for v in range(1, n):  # 매번 홀로인 정점 v 를 기존의 큰 성분(0) 과 합친다
        dsu.union(v, 0)
    assert max(len(_path(dsu, v)) for v in range(n)) <= 2
    assert dsu.size[dsu.find(0)[0]] == n


def test_union_by_size_keeps_find_logarithmic():
    dsu = solution.RollbackDSU(1 << 12)
    step = 1
    while step < (1 << 12):  # 같은 크기끼리 합치는 최악의 순서
        for i in range(0, 1 << 12, 2 * step):
            dsu.union(i, i + step)
        step *= 2
    depth = max(len(_path(dsu, v)) for v in range(1 << 12))
    assert depth <= 13


def _path(dsu, v):
    path = [v]
    while dsu.parent[v] != v:
        v = dsu.parent[v]
        path.append(v)
    return path


def test_larger_random_sequence_matches_naive_on_sampled_queries():
    rng = random.Random(3)
    n = 40
    operations = random_operations(rng, n, 1200)
    assert solution.offline_dynamic_graph(n, operations) == naive(n, operations)


def test_speed_for_ten_thousand_operations():
    rng = random.Random(4)
    n = 2000
    operations = random_operations(rng, n, 12000)
    start = time.perf_counter()
    answers = solution.offline_dynamic_graph(n, operations)
    assert time.perf_counter() - start < 30
    assert len(answers) == sum(1 for op in operations if op[0] in ("connected", "components", "bipartite"))


def test_main(monkeypatch, capsys):
    text = "3 6\n1 1 2\n3 1 3\n1 2 3\n3 1 3\n2 1 2\n3 1 3\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(text))
    solution.main()
    assert capsys.readouterr().out.split() == ["0", "1", "0"]
