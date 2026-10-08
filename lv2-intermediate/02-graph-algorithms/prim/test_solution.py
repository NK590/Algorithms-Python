"""solution.py 검증: 간선의 모든 부분집합을 나열하는 브루트포스, 그리고 크루스칼(독립 구현)과 비교"""
import io
import itertools
import random

from tools.loader import load_solution

solution = load_solution(__file__)
INF = float("inf")


def build(n, edges):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
        if u != v:
            graph[v].append((u, w))
    return graph


def component_of(n, edges, start):
    reach = {start}
    changed = True
    while changed:
        changed = False
        for u, v, _ in edges:
            if (u in reach) != (v in reach):
                reach |= {u, v}
                changed = True
    return reach


def is_tree_over(vertices, subset):
    """subset 이 vertices 를 사이클 없이 연결하는가"""
    if len(subset) != len(vertices) - 1:
        return False
    parent = {v: v for v in vertices}

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    for u, v, _ in subset:
        ru, rv = find(u), find(v)
        if ru == rv:
            return False
        parent[ru] = rv
    return True


def brute_force_mst(n, edges, start):
    """start 가 속한 연결 요소의 신장 트리 중 가중치 합의 최솟값"""
    vertices = component_of(n, edges, start)
    inside = [e for e in edges if e[0] in vertices]
    best = None
    for subset in itertools.combinations(inside, len(vertices) - 1):
        if is_tree_over(vertices, subset):
            total = sum(w for _, _, w in subset)
            best = total if best is None else min(best, total)
    return best


def kruskal_total(n, edges):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total = 0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            total += w
    return total


def random_graph(rng, low=1):
    n = rng.randint(1, 6)
    edges = [(rng.randrange(n), rng.randrange(n), rng.randint(low, 9)) for _ in range(rng.randint(0, 10))]
    return n, edges


def test_readme_example():
    edges = [(0, 1, 4), (0, 2, 1), (1, 2, 2), (1, 3, 5), (2, 3, 8), (2, 4, 10), (3, 4, 2), (3, 5, 6), (4, 5, 3)]
    total, chosen = solution.prim(build(6, edges), 0)
    assert total == 13
    assert chosen == [(0, 2, 1), (2, 1, 2), (1, 3, 5), (3, 4, 2), (4, 5, 3)]


def test_matches_brute_force_on_the_start_component():
    rng = random.Random(0)
    for _ in range(600):
        n, edges = random_graph(rng, low=-3)
        start = rng.randrange(n)
        total, chosen = solution.prim(build(n, edges), start)
        assert total == brute_force_mst(n, edges, start), (n, edges, start)
        vertices = component_of(n, edges, start)
        assert is_tree_over(vertices, chosen), (n, edges, start, chosen)
        assert total == sum(w for _, _, w in chosen)


def test_agrees_with_kruskal_on_connected_graphs():
    rng = random.Random(1)
    checked = 0
    for _ in range(400):
        n = rng.randint(2, 12)
        edges = [(i, rng.randrange(i), rng.randint(1, 20)) for i in range(1, n)]  # 연결을 보장하는 뼈대
        edges += [(rng.randrange(n), rng.randrange(n), rng.randint(1, 20)) for _ in range(rng.randint(0, 20))]
        assert solution.prim(build(n, edges), rng.randrange(n))[0] == kruskal_total(n, edges)
        checked += 1
    assert checked == 400


def test_any_start_vertex_gives_the_same_total():
    rng = random.Random(2)
    for _ in range(100):
        n = rng.randint(2, 8)
        edges = [(i, rng.randrange(i), rng.randint(1, 9)) for i in range(1, n)]
        edges += [(rng.randrange(n), rng.randrange(n), rng.randint(1, 9)) for _ in range(6)]
        totals = {solution.prim(build(n, edges), s)[0] for s in range(n)}
        assert len(totals) == 1


def test_special_cases():
    assert solution.prim([[]], 0) == (0, [])
    assert solution.prim(build(3, [(0, 1, 4)]), 0) == (4, [(0, 1, 4)])  # 닿지 않는 정점 2 는 다루지 않는다
    assert solution.prim(build(2, [(0, 1, 5), (0, 1, 3), (0, 0, 1)]), 0)[0] == 3


def to_matrix(n, edges):
    matrix = [[INF] * n for _ in range(n)]
    for u, v, w in edges:
        if u != v:
            matrix[u][v] = matrix[v][u] = min(matrix[u][v], w)
    return matrix


def test_dense_version_matches_heap_version():
    rng = random.Random(3)
    for _ in range(500):
        n, edges = random_graph(rng, low=-3)
        expected = solution.prim(build(n, [e for e in edges if e[0] != e[1]]), 0)[0]
        assert solution.prim_dense(to_matrix(n, edges)) == expected, (n, edges)
    assert solution.prim_dense([]) == 0


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("3 3\n1 2 1\n2 3 2\n1 3 3\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "3"
