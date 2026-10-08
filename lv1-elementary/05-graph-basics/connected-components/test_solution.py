"""solution.py 검증: 도달 가능성 닫힘(플로이드-워셜식)과 유니온-파인드로 서로 다른 방식과 비교"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def random_graph(rng):
    n = rng.randint(1, 9)
    edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 10))]
    return n, edges


def reachability_groups(n, edges):
    """도달 가능 행렬을 만들고(워셜 방식) 같은 행을 가진 정점끼리 묶는다."""
    reach = [[i == j for j in range(n)] for i in range(n)]
    for u, v in edges:
        reach[u][v] = reach[v][u] = True
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if reach[i][k] and reach[k][j]:
                    reach[i][j] = True
    return sorted({tuple(j for j in range(n) if reach[i][j]) for i in range(n)})


def union_find_components(n, edges):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        parent[find(u)] = find(v)
    return len({find(v) for v in range(n)})


def test_readme_example():
    edges = [(0, 1), (1, 2), (3, 4)]
    assert solution.connected_components(6, edges) == [[0, 1, 2], [3, 4], [5]]
    assert solution.component_ids(6, edges) == [0, 0, 0, 1, 1, 2]
    assert solution.count_components(6, edges) == 3
    assert not solution.is_connected(6, edges)
    assert solution.largest_component_size(6, edges) == 3


def test_components_match_reachability_closure():
    rng = random.Random(0)
    for _ in range(400):
        n, edges = random_graph(rng)
        groups = [tuple(g) for g in solution.connected_components(n, edges)]
        assert sorted(groups) == reachability_groups(n, edges), (n, edges)


def test_count_matches_union_find():
    rng = random.Random(1)
    for _ in range(400):
        n, edges = random_graph(rng)
        assert solution.count_components(n, edges) == union_find_components(n, edges)


def test_edge_cases():
    assert solution.connected_components(0, []) == []
    assert solution.count_components(0, []) == 0
    assert not solution.is_connected(0, [])
    assert solution.is_connected(1, [])
    assert solution.largest_component_size(0, []) == 0
    assert solution.count_components(5, []) == 5  # 간선이 없으면 정점마다 하나씩


def test_has_cycle_matches_edge_count_formula():
    # 숲(사이클 없는 그래프)이면 간선 수 = 정점 수 − 연결 요소 수 이다. 자기 간선·중복 간선도 사이클로 센다.
    rng = random.Random(2)
    for _ in range(500):
        n, edges = random_graph(rng)
        formula = len(edges) != n - solution.count_components(n, edges)
        assert solution.has_cycle(n, edges) == formula, (n, edges)


def test_has_cycle_examples():
    assert not solution.has_cycle(4, [(0, 1), (1, 2), (2, 3)])
    assert solution.has_cycle(3, [(0, 1), (1, 2), (2, 0)])
    assert solution.has_cycle(2, [(0, 1), (0, 1)])  # 같은 쌍을 잇는 간선이 둘
    assert solution.has_cycle(1, [(0, 0)])
    assert not solution.has_cycle(0, [])


def test_large_path_and_forest():
    n = 100_000
    path = [(i, i + 1) for i in range(n - 1)]
    assert solution.is_connected(n, path) and not solution.has_cycle(n, path)
    assert solution.count_components(n, path[::2]) == n - len(path[::2])


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("6 5\n1 2\n2 5\n5 1\n3 4\n4 6\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "2"
