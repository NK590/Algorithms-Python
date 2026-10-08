"""solution.py 검증: 모든 2색 칠하기(2ⁿ)를 시도하는 브루트포스와 비교, 반환된 색·사이클은 직접 검증"""
import io
import itertools
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def build(n, edges):
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    return graph


def brute_force_bipartite(n, edges):
    return any(all(c[u] != c[v] for u, v in edges) for c in itertools.product((0, 1), repeat=n))


def random_graph(rng):
    n = rng.randint(1, 8)
    edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 10))]
    return n, edges


def test_matches_brute_force_and_coloring_is_proper():
    rng = random.Random(0)
    yes = no = 0
    for _ in range(1500):
        n, edges = random_graph(rng)
        graph = build(n, edges)
        expected = brute_force_bipartite(n, edges)
        color = solution.two_color(graph)
        assert (color is not None) == expected, (n, edges)
        assert solution.is_bipartite(graph) == expected
        assert solution.is_bipartite_dsu(n, edges) == expected, (n, edges)
        if color is not None:
            assert all(color[u] != color[v] for u, v in edges)
            assert set(color) <= {0, 1}
            yes += 1
        else:
            no += 1
    assert yes > 200 and no > 200


def test_partition():
    graph = build(5, [(0, 1), (1, 2), (2, 3), (3, 0), (4, 3)])
    left, right = solution.partition(graph)
    assert sorted(left + right) == list(range(5))
    assert all((u in left) != (v in left) for u in range(5) for v in graph[u])
    assert solution.partition(build(3, [(0, 1), (1, 2), (2, 0)])) is None


def test_special_cases():
    assert solution.two_color([]) == []
    assert solution.two_color([[]]) == [0]  # 간선이 없는 정점
    assert solution.two_color(build(1, [(0, 0)])) is None  # 자기 자신으로 가는 간선은 홀수 사이클(길이 1)
    assert solution.is_bipartite_dsu(1, [(0, 0)]) is False
    assert solution.is_bipartite(build(4, [(0, 1), (2, 3)])) is True  # 연결되지 않은 그래프
    # 두 번째 연결 요소에만 홀수 사이클이 있는 경우 (첫 요소만 보면 놓친다)
    assert solution.is_bipartite(build(5, [(0, 1), (2, 3), (3, 4), (4, 2)])) is False


def test_even_cycle_is_bipartite_odd_cycle_is_not():
    for length in range(3, 12):
        cycle = [(i, (i + 1) % length) for i in range(length)]
        assert solution.is_bipartite(build(length, cycle)) == (length % 2 == 0)


def check_odd_cycle(edges, cycle):
    edge_set = {frozenset(e) for e in edges}
    assert len(cycle) % 2 == 1
    assert len(set(cycle)) == len(cycle)
    if len(cycle) == 1:
        assert frozenset((cycle[0],)) in edge_set
        return
    for a, b in zip(cycle, cycle[1:] + cycle[:1]):
        assert frozenset((a, b)) in edge_set, (cycle, a, b)


def test_odd_cycle_is_a_real_odd_cycle():
    rng = random.Random(1)
    found = 0
    for _ in range(1500):
        n, edges = random_graph(rng)
        graph = build(n, edges)
        cycle = solution.odd_cycle(graph)
        assert (cycle is None) == solution.is_bipartite(graph)
        if cycle is not None:
            check_odd_cycle(edges, cycle)
            found += 1
    assert found > 200


def test_odd_cycle_examples():
    assert solution.odd_cycle(build(3, [(0, 1), (1, 2), (2, 0)])) is not None
    assert sorted(solution.odd_cycle(build(5, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 2)]))) == [2, 3, 4]  # 꼬리(0-1)가 붙은 삼각형
    assert solution.odd_cycle(build(5, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 1)])) is None  # 길이 4 의 사이클은 짝수
    assert solution.odd_cycle(build(4, [(0, 1), (1, 2), (2, 3), (3, 0)])) is None
    assert solution.odd_cycle(build(1, [(0, 0)])) == [0]


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("2\n3 2\n1 3\n2 3\n4 4\n1 2\n2 3\n3 4\n4 2\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["YES", "NO"]
