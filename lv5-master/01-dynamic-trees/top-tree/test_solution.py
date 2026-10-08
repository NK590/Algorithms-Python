"""solution.py 검증: 트리 DP 를 처음부터 다시 계산하는 순진한 방법, 기호 대수(어떤 정점이 어떤 순서로 묶였는지) 와 비교하고 클러스터 트리의 구조를 확인"""
import io
import math
import random
import time

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def random_tree(rng, n, shape):
    if shape == "path":
        return [(i, i + 1) for i in range(n - 1)]
    if shape == "star":
        return [(0, i) for i in range(1, n)]
    if shape == "caterpillar":
        spine = max(1, n // 2)
        return [(i, i + 1) for i in range(spine - 1)] + [(rng.randrange(spine), i) for i in range(spine, n)]
    if shape == "binary":
        return [((i - 1) // 2, i) for i in range(1, n)]
    return [(rng.randrange(i), i) for i in range(1, n)]  # 무작위


SHAPES = ["path", "star", "caterpillar", "binary", "random"]


def children_lists(n, edges, root):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    parent = [-1] * n
    order = [root]
    for v in order:
        for w in adj[v]:
            if w != parent[v]:
                parent[w] = v
                order.append(w)
    return parent, order


def naive_max_independent_set(n, edges, weights, root):
    parent, order = children_lists(n, edges, root)
    dp0, dp1 = [0] * n, list(weights)
    for v in reversed(order):
        if parent[v] != -1:
            dp0[parent[v]] += max(dp0[v], dp1[v])
            dp1[parent[v]] += dp0[v]
    return max(dp0[root], dp1[root], 0)


def naive_linear(n, edges, a, b, mod, root):
    parent, order = children_lists(n, edges, root)
    total = [0] * n
    val = [0] * n
    for v in reversed(order):
        val[v] = (a[v] + b[v] * total[v]) % mod
        if parent[v] != -1:
            total[parent[v]] += val[v]
    return val[root]


def test_max_independent_set_with_updates_matches_recomputation():
    rng = random.Random(0)
    for trial in range(200):
        n = rng.randint(1, 30)
        shape = SHAPES[trial % len(SHAPES)]
        edges = random_tree(rng, n, shape)
        root = rng.randrange(n)
        weights = [rng.randint(-6, 12) for _ in range(n)]
        solver = solution.TreeMaxIndependentSet(n, edges, weights, root)
        assert solver.best() == naive_max_independent_set(n, edges, weights, root), (n, shape)
        for _ in range(40):
            v, w = rng.randrange(n), rng.randint(-6, 12)
            weights[v] = w
            solver.set_weight(v, w)
            assert solver.best() == naive_max_independent_set(n, edges, weights, root), (n, shape, v, w)


def test_linear_tree_dp_with_updates_matches_recomputation():
    rng = random.Random(1)
    mod = 998244353
    for trial in range(200):
        n = rng.randint(1, 30)
        edges = random_tree(rng, n, SHAPES[trial % len(SHAPES)])
        root = rng.randrange(n)
        a = [rng.randrange(mod) for _ in range(n)]
        b = [rng.randrange(mod) for _ in range(n)]
        solver = solution.LinearTreeDP(n, edges, a, b, mod, root)
        assert solver.root_val() == naive_linear(n, edges, a, b, mod, root)
        for _ in range(30):
            v = rng.randrange(n)
            if rng.random() < 0.5:
                a[v] = rng.randrange(mod)
                solver.set_values(v, a=a[v])
            else:
                b[v] = rng.randrange(mod)
                solver.set_values(v, b=b[v])
            assert solver.root_val() == naive_linear(n, edges, a, b, mod, root)


def symbolic_tree(n, edges, root):
    """클러스터가 덮는 정점 집합과 경로의 정점 순서를 기록하는 기호 대수. 구조가 맞는지 확인한다."""

    def add_vertex(v, light):
        covered = {v} | (light if light is not None else set())
        return ((v,), frozenset(covered))

    def compress(upper, lower):
        assert not (upper[1] & lower[1]), "두 클러스터가 같은 정점을 덮는다"
        return (upper[0] + lower[0], upper[1] | lower[1])

    def add_edge(path):
        return set(path[1])

    def rake(a, b):
        assert not (a & b), "두 가벼운 서브트리가 같은 정점을 덮는다"
        return a | b

    return solution.StaticTopTree(n, edges, add_vertex, compress, add_edge, rake, root)


def test_cluster_tree_covers_every_vertex_once_and_keeps_path_order():
    rng = random.Random(2)
    for trial in range(300):
        n = rng.randint(1, 40)
        edges = random_tree(rng, n, SHAPES[trial % len(SHAPES)])
        root = rng.randrange(n)
        tree = symbolic_tree(n, edges, root)
        path, covered = tree.root_value()
        assert covered == frozenset(range(n))  # 모든 정점을 한 번씩
        parent, order = children_lists(n, edges, root)
        assert path[0] == root and all(parent[b] == a for a, b in zip(path, path[1:]))  # 루트에서 아래로 내려가는 경로 (무거운 경로) 의 순서가 유지된다
        # 정점마다 갱신 경로의 길이는 클러스터 트리의 깊이
        assert all(tree.depth_of(v) >= 1 for v in range(n))


def test_cluster_tree_depth_is_logarithmic():
    rng = random.Random(3)
    for shape in SHAPES:
        for n in (1000, 8191):
            edges = random_tree(rng, n, shape)
            tree = symbolic_tree(n, edges, 0)
            deepest = max(tree.depth_of(v) for v in range(n))
            assert deepest <= 4 * math.log2(n) + 8, (shape, n, deepest)
            assert len(tree.kind) <= 4 * n  # 노드 수: 정점마다 최대 (정점 + compress/rake + add_edge) 몇 개


def test_incremental_updates_equal_a_fresh_build():
    rng = random.Random(4)
    n = 200
    edges = random_tree(rng, n, "random")
    weights = [rng.randint(-5, 9) for _ in range(n)]
    solver = solution.TreeMaxIndependentSet(n, edges, weights)
    for _ in range(300):
        v, w = rng.randrange(n), rng.randint(-5, 9)
        weights[v] = w
        solver.set_weight(v, w)
    fresh = solution.TreeMaxIndependentSet(n, edges, weights)
    assert solver.tree.value == fresh.tree.value  # 클러스터 값이 전부 같다 (갱신이 경로 위의 클러스터를 빠뜨리지 않았다)


def test_balanced_grouping_puts_the_heaviest_item_next_to_the_root():
    union = lambda *args: frozenset().union(*[a for a in args if a is not None])  # noqa: E731  (값이 중요하지 않은 대수)
    star = solution.StaticTopTree(5, [(0, 1), (0, 2), (0, 3), (0, 4)], lambda v, light: frozenset({v}), union, lambda p: p, union)
    leaves = [star.vertex_node[v] for v in (1, 2, 3, 4)]
    for weights in ([1000, 1, 1, 1], [1, 1, 1, 1000]):  # 지배적인 항목이 양 끝에 있으면 루트의 직접 자식
        root = star._balanced(leaves, weights, solution.RAKE)
        heaviest = leaves[weights.index(1000)]
        assert star.node_parent[heaviest] == root  # 균등 분할이라면 한 단계 아래에 있었을 것
    root = star._balanced(leaves, [1, 1, 1, 1], solution.RAKE)  # 균등한 가중치는 완전 이진 모양
    assert all(star.node_parent[star.node_parent[leaf]] == root for leaf in leaves)


def test_setting_zero_values_is_applied():
    mod = 998244353
    solver = solution.LinearTreeDP(3, [(0, 1), (1, 2)], [5, 6, 7], [2, 3, 4], mod)
    assert solver.root_val() == (5 + 2 * (6 + 3 * 7)) % mod == 59
    solver.set_values(0, a=0)  # 0 도 유효한 새 값이다 (빈 값 None 과 구분)
    assert solver.root_val() == 2 * (6 + 3 * 7) % mod == 54
    solver.set_values(1, b=0)
    assert solver.root_val() == 2 * 6 % mod == 12
    solver.set_values(1, a=0)
    assert solver.root_val() == 0


def test_rake_tree_is_balanced_by_subtree_size():
    # 루트 0 의 무거운 자식은 길이 2000 의 사슬, 가벼운 자식은 크기 1000 의 사슬 하나와 잎 셋. 크기로 균형을 맞추면 큰 가벼운 서브트리가 rake 루트의 직접 자식이다.
    edges = [(0, 1)] + [(i, i + 1) for i in range(1, 2000)] + [(0, 2001)] + [(i, i + 1) for i in range(2001, 3000)] + [(0, 3001), (0, 3002), (0, 3003)]
    n = 3004
    union = lambda *args: frozenset().union(*[a for a in args if a is not None])  # noqa: E731  (값이 중요하지 않은 대수)
    tree = solution.StaticTopTree(n, edges, lambda v, light: frozenset({v}), union, lambda p: p, union)
    rake_root = tree.child_a[tree.vertex_node[0]]
    assert tree.kind[rake_root] == solution.RAKE
    node = tree.vertex_node[2001]
    while tree.kind[node] != solution.ADD_EDGE:
        node = tree.node_parent[node]
    assert tree.node_parent[node] == rake_root


def test_invalid_trees():
    def dummy(*args):
        return None

    with pytest.raises(ValueError, match="n - 1"):
        solution.StaticTopTree(3, [(0, 1)], dummy, dummy, dummy, dummy)
    with pytest.raises(ValueError, match="연결|사이클"):
        solution.StaticTopTree(4, [(0, 1), (1, 2), (2, 0)], dummy, dummy, dummy, dummy)
    with pytest.raises(ValueError, match="하나 이상"):
        solution.StaticTopTree(0, [], dummy, dummy, dummy, dummy)
    single = solution.TreeMaxIndependentSet(1, [], [7])
    assert single.best() == 7
    single.set_weight(0, -3)
    assert single.best() == 0  # 빈 집합


def test_large_tree_is_fast():
    rng = random.Random(5)
    n = 100000
    edges = [(rng.randrange(max(0, i - 50), i), i) for i in range(1, n)]  # 깊은 트리
    weights = [rng.randint(-10, 100) for _ in range(n)]
    started = time.perf_counter()
    solver = solution.TreeMaxIndependentSet(n, edges, weights)
    initial = solver.best()
    for _ in range(5000):
        solver.set_weight(rng.randrange(n), rng.randint(-10, 100))
    assert time.perf_counter() - started < 60
    assert initial == naive_max_independent_set(n, edges, weights, 0)


def test_main_dynamic_dp_format(monkeypatch, capsys):
    # 경로 1-2-3-4, 가중치 1 2 3 4. 질의마다 가중치를 바꾼 뒤 순진한 DP 로 계산한 값과 비교
    text = "4 3\n1 2 3 4\n1 2\n2 3\n3 4\n1 1\n2 10\n4 0\n"
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(text.encode())))
    solution.main()
    weights = [1, 2, 3, 4]
    expected = []
    for v, w in [(0, 1), (1, 10), (3, 0)]:
        weights[v] = w
        expected.append(naive_max_independent_set(4, [(0, 1), (1, 2), (2, 3)], weights, 0))
    assert capsys.readouterr().out == "\n".join(map(str, expected)) + "\n"
