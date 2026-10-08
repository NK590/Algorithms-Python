"""solution.py 검증: 정의에서 바로 만든 독립성 판정(사이클 DFS, 부분집합 XOR)과 모든 부분집합 전수 탐색으로 비교"""
import io
import itertools
import random

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)
Matroid = solution.Matroid


# ---- 정의에서 바로 만든 독립성 판정 (solution 의 구현과 다른 길) -------------------------------------

def uniform_independent(k, items):
    return len(items) <= k


def partition_independent(group_of, capacity, items):
    return all(sum(1 for e in items if group_of[e] == g) <= capacity[g] for g in set(group_of))


def graphic_independent(edges, items):
    """사이클 존재 여부를 DFS 로 판정 (자기 루프나 평행 간선도 사이클)."""
    adj = {}
    for e in items:
        a, b = edges[e]
        adj.setdefault(a, []).append((b, e))
        adj.setdefault(b, []).append((a, e))
    seen = set()
    for s in adj:
        if s in seen:
            continue
        seen.add(s)
        stack = [(s, -1)]
        while stack:
            v, via = stack.pop()
            for to, e in adj[v]:
                if e == via:
                    continue
                if to in seen:
                    return False
                seen.add(to)
                stack.append((to, e))
    return True


def linear_independent(vectors, items):
    """GF(2) 일차 독립: 공집합이 아닌 부분집합의 XOR 이 모두 0 이 아니다."""
    vs = [vectors[e] for e in items]
    for r in range(1, len(vs) + 1):
        for sub in itertools.combinations(vs, r):
            x = 0
            for v in sub:
                x ^= v
            if x == 0:
                return False
    return True


def make_random_matroid(rng, n):
    """(matroid, 정의에서 만든 판정 함수) 를 무작위로 하나."""
    kind = rng.choice(["uniform", "partition", "graphic", "linear"])
    if kind == "uniform":
        k = rng.randint(0, n)
        return solution.UniformMatroid(k), lambda items: uniform_independent(k, items)
    if kind == "partition":
        groups = rng.randint(1, max(1, n // 2))
        group_of = [rng.randrange(groups) for _ in range(n)]
        capacity = [rng.randint(0, 2) for _ in range(groups)]
        return solution.PartitionMatroid(group_of, capacity), lambda items: partition_independent(group_of, capacity, items)
    if kind == "graphic":
        vertices = rng.randint(2, max(2, n // 2 + 1))
        edges = [(rng.randrange(vertices), rng.randrange(vertices)) for _ in range(n)]
        return solution.GraphicMatroid(vertices, edges), lambda items: graphic_independent(edges, items)
    bits = rng.randint(1, 5)
    vectors = [rng.randrange(0, 1 << bits) for _ in range(n)]
    return solution.LinearMatroid(vectors), lambda items: linear_independent(vectors, items)


def all_subsets(n):
    for mask in range(1 << n):
        yield [e for e in range(n) if mask >> e & 1]


def brute_by_size(n, indep1, indep2, weight=None):
    """크기 k 마다 (최대 가중치) 를 전수 탐색으로 구한다. weight 가 없으면 존재 여부만."""
    best = {}
    for items in all_subsets(n):
        if indep1(items) and indep2(items):
            w = sum(weight[e] for e in items) if weight is not None else 0
            k = len(items)
            if k not in best or w > best[k]:
                best[k] = w
    return best


# ---- 매트로이드 클래스 자체 --------------------------------------------------------------------------

def test_oracles_agree_with_definitions():
    rng = random.Random(0)
    for _ in range(150):
        n = rng.randint(1, 8)
        matroid, reference = make_random_matroid(rng, n)
        for items in all_subsets(n):
            assert matroid.independent(items) == reference(items), (type(matroid).__name__, items)


def test_matroid_axioms_hold_for_every_class():
    """공집합 독립, 부분집합 닫힘, 교환 성질 — 테스트가 쓰는 매트로이드가 정말 매트로이드인지 확인."""
    rng = random.Random(1)
    for _ in range(120):
        n = rng.randint(1, 7)
        matroid, reference = make_random_matroid(rng, n)
        independent = [frozenset(s) for s in all_subsets(n) if reference(s)]
        family = set(independent)
        assert frozenset() in family
        for s in independent:
            for e in s:
                assert s - {e} in family
        for small in independent:
            for large in independent:
                if len(small) < len(large):
                    assert any(small | {x} in family for x in large - small)


def test_fast_exchange_matches_the_generic_definition():
    rng = random.Random(2)
    for _ in range(400):
        n = rng.randint(2, 9)
        matroid, reference = make_random_matroid(rng, n)
        independent = [s for s in all_subsets(n) if reference(s)]
        current = rng.choice(independent)
        for x in range(n):
            if x in current:
                continue
            fast = sorted(matroid.exchangeable(current, x))
            slow = sorted(Matroid.exchangeable(matroid, current, x))
            assert fast == slow, (type(matroid).__name__, current, x)


def test_matroid_base_class_requires_an_oracle():
    with pytest.raises(NotImplementedError):
        Matroid().independent([0])


# ---- 최대 크기 ---------------------------------------------------------------------------------------

def test_matches_brute_force_on_random_pairs_of_matroids():
    rng = random.Random(3)
    for _ in range(500):
        n = rng.randint(1, 10)
        m1, ref1 = make_random_matroid(rng, n)
        m2, ref2 = make_random_matroid(rng, n)
        result = solution.matroid_intersection(n, m1, m2)
        assert result == sorted(result) and len(set(result)) == len(result)
        assert ref1(result) and ref2(result)
        assert len(result) == max(brute_by_size(n, ref1, ref2)), (n,)


def test_starting_from_any_common_independent_set_reaches_the_maximum():
    rng = random.Random(4)
    for _ in range(200):
        n = rng.randint(1, 9)
        m1, ref1 = make_random_matroid(rng, n)
        m2, ref2 = make_random_matroid(rng, n)
        optimum = max(brute_by_size(n, ref1, ref2))
        commons = [s for s in all_subsets(n) if ref1(s) and ref2(s)]
        start = rng.choice(commons)
        result = solution.matroid_intersection(n, m1, m2, initial=start)
        assert len(result) == optimum
        assert ref1(result) and ref2(result)


def test_initial_must_be_a_common_independent_set():
    with pytest.raises(ValueError, match="공통 독립"):
        solution.matroid_intersection(3, solution.UniformMatroid(1), solution.UniformMatroid(3), initial=[0, 1])
    with pytest.raises(ValueError, match="공통 독립"):
        solution.matroid_intersection(3, solution.UniformMatroid(3), solution.UniformMatroid(1), initial=[0, 1])


def test_empty_ground_set_and_zero_capacity():
    assert solution.matroid_intersection(0, solution.UniformMatroid(0), solution.UniformMatroid(0)) == []
    assert solution.matroid_intersection(3, solution.UniformMatroid(0), solution.UniformMatroid(3)) == []
    assert solution.matroid_intersection(3, solution.PartitionMatroid([0, 0, 1], [0, 1]), solution.UniformMatroid(3)) == [2]


def test_bipartite_matching_as_two_partition_matroids():
    """간선이 원소, 왼쪽 정점별·오른쪽 정점별로 하나씩만 — 이분 매칭."""
    rng = random.Random(5)

    def kuhn(left, right, es):
        adj = [[] for _ in range(left)]
        for a, b in es:
            adj[a].append(b)
        match_right = [-1] * right

        def try_(v, seen):
            for to in adj[v]:
                if to in seen:
                    continue
                seen.add(to)
                if match_right[to] == -1 or try_(match_right[to], seen):
                    match_right[to] = v
                    return True
            return False

        return sum(try_(v, set()) for v in range(left))

    for _ in range(300):
        left, right = rng.randint(1, 12), rng.randint(1, 12)
        es = [(a, b) for a in range(left) for b in range(right) if rng.random() < 0.2]
        m1 = solution.PartitionMatroid([a for a, _ in es], 1)
        m2 = solution.PartitionMatroid([b for _, b in es], 1)
        result = solution.matroid_intersection(len(es), m1, m2)
        assert len(result) == kuhn(left, right, es)
        assert len({es[e][0] for e in result}) == len(result) == len({es[e][1] for e in result})


def test_rainbow_forest_matches_brute_force():
    rng = random.Random(6)
    for _ in range(250):
        n = rng.randint(2, 6)
        m = rng.randint(1, 10)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(m)]
        colors = [rng.randrange(rng.randint(1, 4)) for _ in range(m)]
        graphic = solution.GraphicMatroid(n, edges)
        partition = solution.PartitionMatroid(colors, 1)
        result = solution.matroid_intersection(m, graphic, partition)
        brute = max(
            len(items)
            for items in all_subsets(m)
            if graphic_independent(edges, items) and len({colors[e] for e in items}) == len(items)
        )
        assert len(result) == brute
        assert graphic_independent(edges, result) and len({colors[e] for e in result}) == len(result)


def test_linear_matroid_with_partition():
    rng = random.Random(7)
    for _ in range(200):
        n = rng.randint(1, 10)
        vectors = [rng.randrange(1, 16) for _ in range(n)]
        groups = [rng.randrange(3) for _ in range(n)]
        m1, m2 = solution.LinearMatroid(vectors), solution.PartitionMatroid(groups, 1)
        result = solution.matroid_intersection(n, m1, m2)
        brute = max(
            len(s) for s in all_subsets(n) if linear_independent(vectors, s) and len({groups[e] for e in s}) == len(s)
        )
        assert len(result) == brute


# ---- 가중치 판 ----------------------------------------------------------------------------------------

def test_weighted_matches_brute_force_for_every_size():
    rng = random.Random(8)
    for _ in range(400):
        n = rng.randint(1, 9)
        m1, ref1 = make_random_matroid(rng, n)
        m2, ref2 = make_random_matroid(rng, n)
        weight = [rng.randint(-4, 9) for _ in range(n)]
        by_size = solution.weighted_matroid_intersection(n, m1, m2, weight)
        expected = brute_by_size(n, ref1, ref2, weight)
        assert len(by_size) == max(expected) + 1
        for k, (total, items) in enumerate(by_size):
            assert len(items) == k
            assert ref1(items) and ref2(items)
            assert total == sum(weight[e] for e in items) == expected[k], (k, items)


def test_weighted_with_ties_and_zero_weights():
    rng = random.Random(9)
    for _ in range(300):
        n = rng.randint(1, 9)
        m1, ref1 = make_random_matroid(rng, n)
        m2, ref2 = make_random_matroid(rng, n)
        weight = [rng.choice([0, 1, 1, 2]) for _ in range(n)]
        by_size = solution.weighted_matroid_intersection(n, m1, m2, weight)
        expected = brute_by_size(n, ref1, ref2, weight)
        assert [total for total, _ in by_size] == [expected[k] for k in range(len(by_size))]
        zero = solution.weighted_matroid_intersection(n, m1, m2, [0] * n)
        assert len(zero) == len(solution.matroid_intersection(n, m1, m2)) + 1


def test_weighted_float_weights():
    rng = random.Random(10)
    for _ in range(100):
        n = rng.randint(1, 8)
        m1, ref1 = make_random_matroid(rng, n)
        m2, ref2 = make_random_matroid(rng, n)
        weight = [rng.randint(-8, 8) / 4 for _ in range(n)]
        by_size = solution.weighted_matroid_intersection(n, m1, m2, weight)
        expected = brute_by_size(n, ref1, ref2, weight)
        assert [total for total, _ in by_size] == [expected[k] for k in range(len(by_size))]


def test_minimum_weight_arborescence():
    """뿌리 r 에서 나가는 최소 가중치 신장 arborescence = 무방향 그래픽 매트로이드 ∩ 도착 정점별 1개 (뿌리는 0개)."""
    rng = random.Random(11)
    for _ in range(200):
        n = rng.randint(2, 5)
        arcs = [(a, b) for a in range(n) for b in range(n) if a != b and rng.random() < 0.55]
        if not arcs:
            continue
        cost = [rng.randint(1, 9) for _ in arcs]
        graphic = solution.GraphicMatroid(n, arcs)
        capacity = [0] + [1] * (n - 1)  # 정점 0 이 뿌리
        in_degree = solution.PartitionMatroid([b for _, b in arcs], capacity)
        by_size = solution.weighted_matroid_intersection(len(arcs), graphic, in_degree, [-c for c in cost])
        best = None
        for items in itertools.combinations(range(len(arcs)), n - 1):
            if graphic_independent(arcs, items) and partition_independent([b for _, b in arcs], capacity, items):
                total = sum(cost[e] for e in items)
                best = total if best is None else min(best, total)
        if best is None:
            assert len(by_size) - 1 < n - 1
        else:
            assert len(by_size) - 1 == n - 1 and -by_size[n - 1][0] == best


def exchange_graph_by_definition(n, ref1, ref2, current):
    """독립성 판정 함수만으로 정의 그대로 교환 그래프를 만든다: (간선 목록, 출발점, 도착점)."""
    inside = sorted(current)
    outside = [x for x in range(n) if x not in inside]
    arcs = {v: [] for v in range(n)}
    for y in inside:
        for x in outside:
            trial = [e for e in inside if e != y] + [x]
            if ref1(trial):
                arcs[y].append(x)
            if ref2(trial):
                arcs[x].append(y)
    sources = [x for x in outside if ref1(inside + [x])]
    sinks = [x for x in outside if ref2(inside + [x])]
    return arcs, sources, sinks


def random_common_independent_set(rng, n, ref1, ref2):
    order = list(range(n))
    rng.shuffle(order)
    chosen = []
    for e in order:
        if rng.random() < 0.4 and ref1(chosen + [e]) and ref2(chosen + [e]):
            chosen.append(e)
    return chosen


def test_augmenting_path_is_a_shortest_path_of_the_exchange_graph():
    """아무 공통 독립 집합 I 에서 시작해도 찾은 경로는 정의대로 만든 교환 그래프의 최단 경로이고, 뒤집으면 공통 독립 집합이 하나 커진다."""
    rng = random.Random(14)
    checked = 0
    for _ in range(1500):
        n = rng.randint(3, 11)
        m1, ref1 = make_random_matroid(rng, n)
        m2, ref2 = make_random_matroid(rng, n)
        current = random_common_independent_set(rng, n, ref1, ref2)
        in_set = [e in current for e in range(n)]
        arcs, sources, sinks = exchange_graph_by_definition(n, ref1, ref2, current)
        # 정점 수가 최소인 경로의 길이를 BFS 로
        distance = {s: 1 for s in sources}
        queue = list(sources)
        for v in queue:
            for to in arcs[v]:
                if to not in distance:
                    distance[to] = distance[v] + 1
                    queue.append(to)
        reachable = [distance[x] for x in sinks if x in distance]
        path = solution._shortest_path(n, m1, m2, in_set)
        if not reachable:
            assert path is None
            continue
        assert path is not None and len(path) == min(reachable), (n, current, path)
        assert path[0] in sources and path[-1] in sinks and len(set(path)) == len(path)
        assert all(b in arcs[a] for a, b in zip(path, path[1:]))
        flipped = sorted(set(current) ^ set(path))
        assert ref1(flipped) and ref2(flipped) and len(flipped) == len(current) + 1
        checked += 1
    assert checked > 300


def all_simple_paths(arcs, sources, sinks):
    sink_set = set(sinks)

    def extend(path):
        if path[-1] in sink_set:
            yield list(path)
        for to in arcs[path[-1]]:
            if to not in path:
                path.append(to)
                yield from extend(path)
                path.pop()

    for s in sources:
        yield from extend([s])


def test_weighted_path_minimizes_weight_then_length():
    """가중치 판의 각 단계에서, 고른 경로는 모든 단순 경로 중 (값의 합, 정점 수) 이 사전순으로 최소."""
    rng = random.Random(15)
    checked = 0
    for _ in range(300):
        n = rng.randint(3, 8)
        m1, ref1 = make_random_matroid(rng, n)
        m2, ref2 = make_random_matroid(rng, n)
        weight = [rng.choice([0, 0, 1, 2, 3, -1]) for _ in range(n)]
        in_set = [False] * n
        while True:
            current = [e for e in range(n) if in_set[e]]
            arcs, sources, sinks = exchange_graph_by_definition(n, ref1, ref2, current)
            cost = [(weight[v] if in_set[v] else -weight[v]) for v in range(n)]
            keys = [(sum(cost[v] for v in path), len(path)) for path in all_simple_paths(arcs, sources, sinks)]
            path = solution._lightest_path(n, m1, m2, weight, in_set)
            if not keys:
                assert path is None
                break
            assert path is not None
            assert (sum(cost[v] for v in path), len(path)) == min(keys), (n, weight, current, path)
            solution._flip(in_set, path)
            checked += 1
    assert checked > 300


def test_weighted_tie_goes_to_the_path_with_fewer_vertices(monkeypatch):
    """무게 합이 같은 경로가 둘이면 정점 수가 적은 쪽: 직접 만든 교환 그래프에서 긴 경로 0-1-2-3 과 짧은 경로 4-3 (값은 모두 0)."""
    n = 5
    arcs = [[1], [2], [3], [], [3]]
    monkeypatch.setattr(solution, "_exchange_graph", lambda n_, m1, m2, in_set: (arcs, [0, 4], [3]))
    assert solution._lightest_path(n, None, None, [0] * n, [False] * n) == [4, 3]
    # 무게가 다르면 정점 수와 상관없이 무게 합이 작은 쪽 (원소 4 를 넣는 값이 +1 이라 손해)
    assert solution._lightest_path(n, None, None, [0, 0, 0, 0, -1], [False] * n) == [0, 1, 2, 3]
    # 가중치가 같은 경로가 하나뿐이면 그 경로
    monkeypatch.setattr(solution, "_exchange_graph", lambda n_, m1, m2, in_set: ([[1], [], [], [], []], [0], [1]))
    assert solution._lightest_path(n, None, None, [5] * n, [False] * n) == [0, 1]


def test_shortest_path_prefers_fewer_vertices_over_exploration_order(monkeypatch):
    """BFS: 0 -> (2, 1), 1 -> 3 -> 4(도착), 2 -> 4. 마지막에 넣은 것부터 탐색(DFS 식) 하면 긴 경로 0-1-3-4 를 고른다."""
    arcs = [[2, 1], [3], [4], [4], []]
    monkeypatch.setattr(solution, "_exchange_graph", lambda n_, m1, m2, in_set: (arcs, [0], [4]))
    assert solution._shortest_path(5, None, None, [False] * 5) == [0, 2, 4]
    monkeypatch.setattr(solution, "_exchange_graph", lambda n_, m1, m2, in_set: ([[], [], [], [], []], [0], [4]))
    assert solution._shortest_path(5, None, None, [False] * 5) is None


def test_min_max_theorem():
    """에드먼즈의 정리: 최대 공통 독립 집합의 크기 = min over A of r1(A) + r2(E \\ A). 모든 A 를 훑어 계산."""
    rng = random.Random(13)

    def rank(ref, items):
        chosen = []
        for e in items:
            if ref(chosen + [e]):
                chosen.append(e)
        return len(chosen)

    for _ in range(150):
        n = rng.randint(1, 9)
        m1, ref1 = make_random_matroid(rng, n)
        m2, ref2 = make_random_matroid(rng, n)
        bound = min(
            rank(ref1, a) + rank(ref2, [e for e in range(n) if e not in a]) for a in all_subsets(n)
        )
        assert len(solution.matroid_intersection(n, m1, m2)) == bound


def test_larger_instances_are_independent_sets_of_both_matroids():
    rng = random.Random(12)
    n_vertices, m = 30, 90
    edges = [(rng.randrange(n_vertices), rng.randrange(n_vertices)) for _ in range(m)]
    colors = [rng.randrange(20) for _ in range(m)]
    graphic = solution.GraphicMatroid(n_vertices, edges)
    partition = solution.PartitionMatroid(colors, 1)
    result = solution.matroid_intersection(m, graphic, partition)
    assert graphic_independent(edges, result)
    assert len({colors[e] for e in result}) == len(result)
    # 적어도 극대: 어떤 원소도 그대로 더할 수는 없다
    for x in range(m):
        if x not in result:
            assert not (graphic.independent(result + [x]) and partition.independent(result + [x]))
    assert len(result) <= min(n_vertices - 1, 20)
    weighted = solution.weighted_matroid_intersection(m, graphic, partition, [rng.randint(1, 50) for _ in range(m)])
    assert len(weighted) - 1 == len(result)


def test_main_prints_a_rainbow_forest(monkeypatch, capsys):
    # 정점 4, 간선 5 (a b color)
    monkeypatch.setattr("sys.stdin", io.StringIO("4 5\n0 1 7\n1 2 7\n2 3 9\n0 2 9\n1 3 4\n"))
    solution.main()
    lines = capsys.readouterr().out.split("\n")
    assert lines[0] == "3"
    chosen = list(map(int, lines[1].split()))
    edges = [(0, 1), (1, 2), (2, 3), (0, 2), (1, 3)]
    colors = [7, 7, 9, 9, 4]
    assert len(chosen) == 3 and len({colors[e] for e in chosen}) == 3 and graphic_independent(edges, chosen)
