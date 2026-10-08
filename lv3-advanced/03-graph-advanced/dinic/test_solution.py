"""solution.py 검증: 모든 s-t 컷을 직접 세어 최소 컷을 구하는 완전탐색(최대 유량 최소 컷 정리)과 비교하고, 유량 보존 법칙을 확인"""
import io
import itertools
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def brute_force_min_cut(n, edges, s, t):
    """edges: (u, v, c) 방향 간선. s 쪽 정점 집합 S 를 모두 시도해 S 에서 나가는 간선 용량의 합의 최솟값."""
    others = [v for v in range(n) if v not in (s, t)]
    best = None
    for mask in range(1 << len(others)):
        side = {s} | {others[i] for i in range(len(others)) if mask >> i & 1}
        cut = sum(c for u, v, c in edges if u in side and v not in side)
        best = cut if best is None else min(best, cut)
    return best


def build(n, edges):
    network = solution.Dinic(n)
    ids = [network.add_edge(u, v, c) for u, v, c in edges]
    return network, ids


def random_network(rng, n):
    edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 6)) for _ in range(rng.randint(0, 3 * n))]
    return edges


def test_max_flow_equals_min_cut_on_random_networks():
    rng = random.Random(0)
    for _ in range(600):
        n = rng.randint(2, 7)
        edges = random_network(rng, n)
        network, _ = build(n, edges)
        assert network.max_flow(0, n - 1) == brute_force_min_cut(n, edges, 0, n - 1), (n, edges)


def test_flow_conservation_and_capacity_constraints():
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(2, 8)
        edges = random_network(rng, n)
        network, ids = build(n, edges)
        value = network.max_flow(0, n - 1)
        net = [0] * n
        for (u, v, c), edge_id in zip(edges, ids):
            f = network.flow_on(edge_id)
            assert 0 <= f <= c, (edges, edge_id, f)
            net[u] -= f
            net[v] += f
        assert all(net[v] == 0 for v in range(n) if v not in (0, n - 1)), (edges, net)
        assert net[n - 1] == value and net[0] == -value


def test_min_cut_side_has_capacity_equal_to_flow():
    rng = random.Random(2)
    for _ in range(300):
        n = rng.randint(2, 8)
        edges = random_network(rng, n)
        network, _ = build(n, edges)
        value = network.max_flow(0, n - 1)
        side = network.min_cut_source_side(0)
        assert side[0] and not side[n - 1]
        assert sum(c for u, v, c in edges if side[u] and not side[v]) == value, (edges,)


def test_classic_examples():
    # 다이아몬드: 출발점에서 나가는 용량이 3 + 2 = 5 이고 가운데 다리 덕에 모두 흘릴 수 있다 → 최대 유량 5
    edges = [(0, 1, 3), (0, 2, 2), (1, 3, 3), (2, 3, 2), (1, 2, 1)]
    network, _ = build(4, edges)
    assert network.max_flow(0, 3) == 5
    # 역간선으로 유량을 되돌려야 최적이 되는 예 (잘못 고른 경로를 취소)
    edges = [(0, 1, 1), (0, 2, 1), (1, 2, 1), (1, 3, 1), (2, 3, 1)]
    network, _ = build(4, edges)
    assert network.max_flow(0, 3) == 2
    network = solution.Dinic(2)
    network.add_edge(0, 1, 5)
    assert network.max_flow(0, 1) == 5 and network.max_flow(0, 1) == 0  # 다시 흘려 봐도 더는 없다


def test_undirected_edges_with_reverse_capacity():
    network = solution.Dinic(3)
    network.add_edge(0, 1, 4, 4)
    network.add_edge(1, 2, 3, 3)
    assert network.max_flow(0, 2) == 3
    network = solution.Dinic(3)
    network.add_edge(0, 1, 4, 4)
    network.add_edge(2, 1, 3, 3)  # 방향을 거꾸로 적어도 무방향이라 같다
    assert network.max_flow(0, 2) == 3


def test_same_source_and_sink_is_rejected_and_disconnected_gives_zero():
    import pytest

    network = solution.Dinic(3)
    network.add_edge(0, 1, 5)
    assert network.max_flow(0, 2) == 0
    with pytest.raises(ValueError, match="같습니다"):
        network.max_flow(1, 1)


def brute_force_matching(left, pairs):
    """왼쪽 정점을 차례로 보며 짝을 짓거나 건너뛰는 완전탐색."""
    adjacency = [[b for a, b in sorted(pairs) if a == x] for x in range(left)]

    def go(x, used):
        if x == left:
            return 0
        best = go(x + 1, used)
        for b in adjacency[x]:
            if not used >> b & 1:
                best = max(best, 1 + go(x + 1, used | 1 << b))
        return best

    return go(0, 0)


def test_bipartite_matching_through_flow():
    rng = random.Random(3)
    for _ in range(150):
        left, right = rng.randint(1, 6), rng.randint(1, 6)
        pairs = {(a, b) for a in range(left) for b in range(right) if rng.random() < 0.4}
        network = solution.Dinic(left + right + 2)
        s, t = left + right, left + right + 1
        for a in range(left):
            network.add_edge(s, a, 1)
        for b in range(right):
            network.add_edge(left + b, t, 1)
        for a, b in pairs:
            network.add_edge(a, left + b, 1)
        assert network.max_flow(s, t) == brute_force_matching(left, pairs), (left, right, pairs)


def edmonds_karp(n, edges, s, t):
    """독립적인 기준 구현: 인접 행렬 위에서 BFS 로 증가 경로를 하나씩 찾는다."""
    capacity = [[0] * n for _ in range(n)]
    for u, v, c in edges:
        capacity[u][v] += c
    flow = 0
    while True:
        parent = [-1] * n
        parent[s] = s
        queue = [s]
        for u in queue:
            for v in range(n):
                if parent[v] < 0 and capacity[u][v] > 0:
                    parent[v] = u
                    queue.append(v)
        if parent[t] < 0:
            return flow
        bottleneck, v = float("inf"), t
        while v != s:
            bottleneck = min(bottleneck, capacity[parent[v]][v])
            v = parent[v]
        v = t
        while v != s:
            capacity[parent[v]][v] -= bottleneck
            capacity[v][parent[v]] += bottleneck
            v = parent[v]
        flow += bottleneck


def test_matches_independent_edmonds_karp_on_larger_random_networks():
    rng = random.Random(5)
    for _ in range(60):
        n = rng.randint(10, 40)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(1, 20)) for _ in range(rng.randint(n, 6 * n))]
        network, _ = build(n, edges)
        assert network.max_flow(0, n - 1) == edmonds_karp(n, edges, 0, n - 1), (n, edges)


def test_large_grid_network_is_fast_and_consistent():
    rng = random.Random(4)
    side = 60  # 3600 개의 정점, 격자 간선
    n = side * side + 2
    network = solution.Dinic(n)
    source, sink = side * side, side * side + 1
    edges = []
    for r in range(side):
        for c in range(side):
            v = r * side + c
            if c + 1 < side:
                forward, backward = rng.randint(1, 9), rng.randint(1, 9)
                network.add_edge(v, v + 1, forward, backward)
                edges += [(v, v + 1, forward), (v + 1, v, backward)]
            if r + 1 < side:
                forward, backward = rng.randint(1, 9), rng.randint(1, 9)
                network.add_edge(v, v + side, forward, backward)
                edges += [(v, v + side, forward), (v + side, v, backward)]
    for r in range(side):
        network.add_edge(source, r * side, 10**6)
        network.add_edge(r * side + side - 1, sink, 10**6)
        edges += [(source, r * side, 10**6), (r * side + side - 1, sink, 10**6)]
    value = network.max_flow(source, sink)
    side_of_source = network.min_cut_source_side(source)
    assert side_of_source[source] and not side_of_source[sink]
    assert sum(c for u, v, c in edges if side_of_source[u] and not side_of_source[v]) == value  # 최대 유량 = 최소 컷
    assert 0 < value < side * 9 * 2


def test_long_path_does_not_recurse():
    n = 50_000
    network = solution.Dinic(n)
    for i in range(n - 1):
        network.add_edge(i, i + 1, 7)
    assert network.max_flow(0, n - 1) == 7


def test_main_distinguishes_lowercase_and_uppercase_vertices(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("2\nA a 2\na Z 5\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "2"  # a 가 A 와 다른 정점이어야 병목 2 가 보인다 (같은 정점이면 5)


def test_main(monkeypatch, capsys):
    text = "9\nA B 3\nB C 3\nC D 5\nD Z 4\nA Z 6\nB Z 2\nA C 1\nB D 7\nZ A 1\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(text))
    solution.main()
    out = int(capsys.readouterr().out)
    # 정점을 A, B, C, D, Z → 0, 1, 2, 3, 4 로 줄여 무방향 간선(양방향 용량)으로 최소 컷을 완전탐색
    index = {"A": 0, "B": 1, "C": 2, "D": 3, "Z": 4}
    edges = []
    for line in text.split("\n")[1:-1]:
        u, v, c = line.split()
        edges.append((index[u], index[v], int(c)))
        edges.append((index[v], index[u], int(c)))
    assert out == brute_force_min_cut(5, edges, 0, 4)
    assert out > 0
