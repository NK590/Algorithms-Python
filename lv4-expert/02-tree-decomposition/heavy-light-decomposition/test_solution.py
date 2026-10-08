"""solution.py 검증: 부모를 따라 올라가는 순진한 경로 계산, 모든 정점을 훑는 서브트리 계산과 무작위 트리로 비교"""
import io
import random
import time

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def random_tree(rng, n, shape=None):
    shape = shape or rng.choice(["random", "chain", "star", "binary", "caterpillar"])
    edges = []
    for v in range(1, n):
        if shape == "random":
            p = rng.randrange(v)
        elif shape == "chain":
            p = v - 1
        elif shape == "star":
            p = 0
        elif shape == "binary":
            p = (v - 1) // 2
        else:  # caterpillar: 긴 줄기에 잎이 달린 모양
            p = v - 1 if v % 2 else max(0, v - 2)
        edges.append((p, v) if rng.random() < 0.5 else (v, p))
    return edges


def parents_depths(n, edges, root):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    parent, depth = [-1] * n, [0] * n
    stack, seen = [root], {root}
    while stack:
        v = stack.pop()
        for w in adj[v]:
            if w not in seen:
                seen.add(w)
                parent[w], depth[w] = v, depth[v] + 1
                stack.append(w)
    return parent, depth


def naive_path(parent, depth, u, v):
    left, right = [], []
    while u != v:
        if depth[u] >= depth[v]:
            left.append(u)
            u = parent[u]
        else:
            right.append(v)
            v = parent[v]
    return left + [u] + right[::-1]


def test_structure_invariants():
    rng = random.Random(0)
    for _ in range(200):
        n = rng.randint(1, 40)
        edges = random_tree(rng, n)
        root = rng.randrange(n)
        hld = solution.HLD(n, edges, root)
        assert sorted(hld.pos) == list(range(n))
        assert all(hld.order_by_pos[hld.pos[v]] == v for v in range(n))
        for v in range(n):
            left, right = hld.subtree_range(v)
            members = {hld.order_by_pos[i] for i in range(left, right)}
            expected = {u for u in range(n) if v in naive_path(*parents_depths(n, edges, root), u, root)}
            assert members == expected, (edges, root, v)  # 서브트리 = 연속 구간
            if hld.heavy[v] != -1:
                assert hld.pos[hld.heavy[v]] == hld.pos[v] + 1  # 무거운 자식은 바로 다음 위치
                assert hld.head[hld.heavy[v]] == hld.head[v]
        assert hld.head[root] == root and hld.parent[root] == -1


def test_light_edges_on_any_root_path_are_logarithmic():
    rng = random.Random(1)
    n = 3000
    for shape in ["random", "binary", "caterpillar"]:
        hld = solution.HLD(n, random_tree(rng, n, shape), 0)
        for v in range(n):
            light, u = 0, v
            while hld.head[u] != 0:  # 루트의 사슬에 닿을 때까지 사슬의 머리 위로 한 번씩 올라간다 = 가벼운 간선 한 개
                light += 1
                u = hld.parent[hld.head[u]]
            assert light <= n.bit_length(), (shape, v)


def test_lca_and_distance_match_the_naive_walk():
    rng = random.Random(2)
    for _ in range(150):
        n = rng.randint(1, 40)
        edges = random_tree(rng, n)
        root = rng.randrange(n)
        hld = solution.HLD(n, edges, root)
        parent, depth = parents_depths(n, edges, root)
        for _ in range(30):
            u, v = rng.randrange(n), rng.randrange(n)
            path = naive_path(parent, depth, u, v)
            assert hld.lca(u, v) == min(path, key=lambda x: depth[x]), (edges, root, u, v)
            assert hld.distance(u, v) == len(path) - 1


def test_path_segments_cover_exactly_the_path():
    rng = random.Random(3)
    for _ in range(150):
        n = rng.randint(1, 40)
        edges = random_tree(rng, n)
        root = rng.randrange(n)
        hld = solution.HLD(n, edges, root)
        parent, depth = parents_depths(n, edges, root)
        for _ in range(30):
            u, v = rng.randrange(n), rng.randrange(n)
            path = naive_path(parent, depth, u, v)
            covered = [hld.order_by_pos[i] for l, r in hld.path_segments(u, v) for i in range(l, r)]
            assert sorted(covered) == sorted(path), (edges, root, u, v)
            covered_edges = [hld.order_by_pos[i] for l, r in hld.path_segments(u, v, edge=True) for i in range(l, r)]
            lca = hld.lca(u, v)
            assert sorted(covered_edges) == sorted(x for x in path if x != lca)  # LCA 만 빠진다
            assert len(hld.path_segments(u, v)) <= 2 * n.bit_length() + 1


def test_vertex_path_queries_with_updates_sum_and_max():
    rng = random.Random(4)
    for _ in range(80):
        n = rng.randint(1, 35)
        edges = random_tree(rng, n)
        root = rng.randrange(n)
        hld = solution.HLD(n, edges, root)
        parent, depth = parents_depths(n, edges, root)
        values = [rng.randint(-20, 20) for _ in range(n)]
        total = solution.PathQuery(hld, values)
        best = solution.PathQuery(hld, values, max, -10**9)
        for _ in range(60):
            if rng.random() < 0.4:
                v, value = rng.randrange(n), rng.randint(-20, 20)
                values[v] = value
                total.update(v, value)
                best.update(v, value)
                assert total.value(v) == value
            else:
                u, v = rng.randrange(n), rng.randrange(n)
                path = naive_path(parent, depth, u, v)
                assert total.query(u, v) == sum(values[x] for x in path), (edges, root, u, v)
                assert best.query(u, v) == max(values[x] for x in path)
        for v in range(n):
            members = [u for u in range(n) if v in naive_path(parent, depth, u, root)]
            assert total.query_subtree(v) == sum(values[u] for u in members)


def test_edge_weights_on_paths():
    rng = random.Random(5)
    for _ in range(80):
        n = rng.randint(2, 35)
        edges = random_tree(rng, n)
        root = rng.randrange(n)
        hld = solution.HLD(n, edges, root)
        parent, depth = parents_depths(n, edges, root)
        weight = {}
        values = [0] * n
        for v in range(n):
            if v != root:
                weight[v] = rng.randint(1, 50)  # 간선 (parent[v], v) 의 가중치
                values[v] = weight[v]
        path_max = solution.PathQuery(hld, values, max, 0, edge=True)
        for _ in range(50):
            u, v = rng.randrange(n), rng.randrange(n)
            nodes = naive_path(parent, depth, u, v)
            lca = hld.lca(u, v)
            expected = max([weight[x] for x in nodes if x != lca], default=0)
            assert path_max.query(u, v) == expected, (edges, root, u, v)


def test_path_add_and_subtree_sum_with_fenwick_trees():
    rng = random.Random(6)
    for _ in range(60):
        n = rng.randint(1, 35)
        edges = random_tree(rng, n)
        root = rng.randrange(n)
        hld = solution.HLD(n, edges, root)
        parent, depth = parents_depths(n, edges, root)
        values = [rng.randint(-5, 5) for _ in range(n)]
        structure = solution.PathAddSubtreeSum(hld, values)
        for _ in range(60):
            kind = rng.randrange(4)
            u, v = rng.randrange(n), rng.randrange(n)
            if kind == 0:
                delta = rng.randint(-9, 9)
                structure.add_path(u, v, delta)
                for x in naive_path(parent, depth, u, v):
                    values[x] += delta
            elif kind == 1:
                delta = rng.randint(-9, 9)
                structure.add_subtree(u, delta)
                for x in range(n):
                    if u in naive_path(parent, depth, x, root):
                        values[x] += delta
            elif kind == 2:
                assert structure.sum_path(u, v) == sum(values[x] for x in naive_path(parent, depth, u, v))
            else:
                assert structure.sum_subtree(u) == sum(values[x] for x in range(n) if u in naive_path(parent, depth, x, root))


def test_segment_tree_basics():
    tree = solution.SegmentTree([5, 3, 8, 1, 9], max, -1)
    assert tree.query(0, 5) == 9 and tree.query(1, 4) == 8 and tree.query(2, 2) == -1
    tree.set(2, 0)
    assert tree.query(0, 4) == 5 and tree.get(2) == 0
    assert solution.SegmentTree([], max, -1).query(0, 0) == -1


def test_segment_tree_with_a_non_commutative_combine_for_every_size_and_range():
    # 문자열 이어 붙이기는 순서가 중요하다: 크기가 2 의 거듭제곱이든 아니든, 전체 구간이든 일부든 맞아야 한다
    rng = random.Random(9)
    for n in range(0, 20):
        values = [chr(ord("a") + rng.randrange(26)) for _ in range(n)]
        tree = solution.SegmentTree(values, lambda a, b: a + b, "")
        for left in range(n + 1):
            for right in range(left, n + 1):
                assert tree.query(left, right) == "".join(values[left:right]), (n, left, right)
        for _ in range(10 if n else 0):
            index = rng.randrange(n)
            values[index] = chr(ord("a") + rng.randrange(26))
            tree.set(index, values[index])
            assert tree.query(0, n) == "".join(values)


def test_invalid_input():
    with pytest.raises(ValueError, match="연결된"):
        solution.HLD(4, [(0, 1), (2, 3)])


def test_long_chain_and_big_random_tree_do_not_recurse_and_are_fast():
    n = 100000
    started = time.perf_counter()
    hld = solution.HLD(n, [(i, i + 1) for i in range(n - 1)], 0)
    assert hld.depth[n - 1] == n - 1 and hld.lca(n - 1, n // 2) == n // 2
    assert hld.path_segments(0, n - 1) == [(0, n)]  # 사슬 하나 = 구간 하나
    rng = random.Random(7)
    big = solution.HLD(n, [(rng.randrange(v), v) for v in range(1, n)], 0)
    values = [rng.randint(0, 100) for _ in range(n)]
    path = solution.PathQuery(big, values, max, 0)
    for _ in range(20000):
        path.query(rng.randrange(n), rng.randrange(n))
    assert time.perf_counter() - started < 30


def test_main_edge_weight_max_queries(monkeypatch, capsys):
    text = "5\n1 2 1\n2 3 2\n2 4 3\n4 5 4\n6\n2 3 5\n1 3 8\n2 3 5\n1 1 10\n2 3 4\n2 1 5\n"
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(text.encode())))
    solution.main()
    assert capsys.readouterr().out == "4\n8\n8\n10\n"  # 3-2-4-5 최대 4, 간선 3 을 8 로 바꾸면 8, 3-2-4 는 8, 간선 1 을 10 으로 바꾸면 1-2-4-5 는 10
