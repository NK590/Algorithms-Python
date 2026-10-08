"""solution.py 검증: 정점이나 간선을 하나씩 지우고 연결 요소 수가 늘어나는지 직접 세는 완전탐색과 비교"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def count_components(vertices, edges):
    vertices = set(vertices)
    parent = {v: v for v in vertices}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        if a in vertices and b in vertices:
            parent[find(a)] = find(b)
    return len({find(v) for v in vertices})


def brute_force(n, edges):
    base = count_components(range(n), edges)
    cut_vertices = [v for v in range(n) if count_components([u for u in range(n) if u != v], edges) > base]
    bridges = [i for i in range(len(edges)) if count_components(range(n), edges[:i] + edges[i + 1 :]) > base]
    return cut_vertices, bridges


def random_multigraph(rng, n, m):
    return [(rng.randrange(n), rng.randrange(n)) for _ in range(m)]


def test_matches_brute_force_on_random_multigraphs():
    rng = random.Random(0)
    for _ in range(800):
        n = rng.randint(1, 9)
        edges = random_multigraph(rng, n, rng.randint(0, 12))  # 자기 루프와 평행 간선도 나온다
        assert solution.find_cut_vertices_and_bridges(n, edges) == brute_force(n, edges), (n, edges)


def test_known_shapes():
    # 사슬: 안쪽 정점이 모두 단절점이고 모든 간선이 단절선
    chain = [(0, 1), (1, 2), (2, 3)]
    assert solution.find_cut_vertices_and_bridges(4, chain) == ([1, 2], [0, 1, 2])
    # 사이클: 단절점도 단절선도 없다
    cycle = [(0, 1), (1, 2), (2, 3), (3, 0)]
    assert solution.find_cut_vertices_and_bridges(4, cycle) == ([], [])
    # 두 삼각형이 한 정점을 공유 (나비 모양): 공유 정점만 단절점, 단절선은 없다
    bowtie = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 2)]
    assert solution.find_cut_vertices_and_bridges(5, bowtie) == ([2], [])
    # 별 모양: 중심이 단절점
    assert solution.find_cut_vertices_and_bridges(4, [(0, 1), (0, 2), (0, 3)]) == ([0], [0, 1, 2])


def test_parallel_edges_are_not_bridges_but_self_loops_are_ignored():
    assert solution.find_cut_vertices_and_bridges(2, [(0, 1), (0, 1)]) == ([], [])
    assert solution.find_cut_vertices_and_bridges(2, [(0, 1), (1, 1), (0, 0)]) == ([], [0])
    assert solution.find_cut_vertices_and_bridges(3, [(0, 1), (0, 1), (1, 2)]) == ([1], [2])


def test_root_is_a_cut_vertex_only_with_two_dfs_children():
    assert solution.find_cut_vertices_and_bridges(3, [(0, 1), (0, 2)])[0] == [0]
    assert solution.find_cut_vertices_and_bridges(3, [(0, 1), (1, 2), (2, 0)])[0] == []
    assert solution.find_cut_vertices_and_bridges(3, [(0, 1)])[0] == []  # 고립된 정점이 있어도 영향 없음


def test_disconnected_graph_is_handled_component_by_component():
    edges = [(0, 1), (1, 2), (3, 4), (4, 5), (5, 3), (5, 6)]
    cuts, bridges = solution.find_cut_vertices_and_bridges(8, edges)
    assert cuts == [1, 5] and bridges == [0, 1, 5]


def test_bridge_pairs_are_sorted_pairs():
    assert solution.bridge_pairs(4, [(3, 2), (1, 0), (2, 1)]) == [(0, 1), (1, 2), (2, 3)]


def connected(u, v, edges):
    parent = list(range(max(max(a, b) for a, b in edges + [(u, v)]) + 1))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        parent[find(a)] = find(b)
    return find(u) == find(v)


def test_two_edge_connected_components_match_the_definition():
    """같은 요소 ⟺ 연결되어 있고, 간선 하나를 지워도 여전히 연결 (서로 다른 두 경로가 있다)"""
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(1, 8)
        edges = random_multigraph(rng, n, rng.randint(0, 12))
        component = solution.two_edge_connected_components(n, edges)
        for u in range(n):
            for v in range(n):
                expected = connected(u, v, edges) and all(
                    connected(u, v, edges[:i] + edges[i + 1 :]) for i in range(len(edges))
                )
                assert (component[u] == component[v]) == expected, (n, edges, u, v)


def test_bridge_tree_links_are_exactly_the_bridges_and_form_a_forest():
    rng = random.Random(2)
    for _ in range(300):
        n = rng.randint(1, 9)
        edges = random_multigraph(rng, n, rng.randint(0, 12))
        component, links = solution.bridge_tree(n, edges)
        _, bridge_ids = brute_force(n, edges)
        assert len(links) == len(bridge_ids) and links == sorted(links)
        assert all(a < b for a, b in links)  # 서로 다른 요소를 잇는다
        count = len(set(component))
        assert count - len(links) == count_components(range(count), links)  # 숲: 요소 수 - 간선 수 = 연결 요소 수
    triangle_pair = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 5), (5, 3)]
    component, links = solution.bridge_tree(6, triangle_pair)
    assert component[0] == component[1] == component[2] != component[3] == component[4] == component[5]
    assert links == [(component[2], component[3])]


def test_deep_chain_does_not_recurse():
    n = 100_000
    chain = [(i, i + 1) for i in range(n - 1)]
    cuts, bridges = solution.find_cut_vertices_and_bridges(n, chain)
    assert len(cuts) == n - 2 and len(bridges) == n - 1
    cycle = chain + [(n - 1, 0)]
    assert solution.find_cut_vertices_and_bridges(n, cycle) == ([], [])


def test_main(monkeypatch, capsys):
    edges = [(1, 4), (6, 7), (4, 5), (6, 1), (5, 7), (2, 5), (2, 1), (3, 2)]
    text = "7 8\n" + "".join(f"{a} {b}\n" for a, b in edges)
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(text.encode())))
    solution.main()
    expected = sorted((min(a, b), max(a, b)) for a, b in (edges[i] for i in brute_force(7, [(a - 1, b - 1) for a, b in edges])[1]))
    assert capsys.readouterr().out.strip().splitlines() == [str(len(expected))] + [f"{a} {b}" for a, b in expected]
    assert expected == [(2, 3)]  # 3 번 정점만 2 번에 매달려 있고 나머지는 모두 고리로 얽혀 있다
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(b"3 2\n1 2\n2 3\n")))
    solution.main()
    assert capsys.readouterr().out.strip().splitlines() == ["2", "1 2", "2 3"]
