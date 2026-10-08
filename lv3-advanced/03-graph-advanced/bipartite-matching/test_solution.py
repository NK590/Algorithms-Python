"""solution.py 검증: 가능한 모든 매칭을 따져 보는 완전탐색과 비교하고, 돌려준 매칭·덮개·독립 집합이 실제로 조건을 만족하는지 확인"""
import io
import itertools
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def brute_force_matching(left_n, adjacency):
    def go(u, used):
        if u == left_n:
            return 0
        best = go(u + 1, used)
        for v in adjacency[u]:
            if not used >> v & 1:
                best = max(best, 1 + go(u + 1, used | 1 << v))
        return best

    return go(0, 0)


def random_bipartite(rng, left_n, right_n, density):
    return [[v for v in range(right_n) if rng.random() < density] for _ in range(left_n)]


def assert_valid_matching(left_n, right_n, adjacency, size, match_left, match_right):
    assert sum(1 for v in match_left if v != -1) == size == sum(1 for u in match_right if u != -1)
    for u, v in enumerate(match_left):
        if v != -1:
            assert v in adjacency[u] and match_right[v] == u


def test_both_algorithms_match_brute_force_and_return_valid_matchings():
    rng = random.Random(0)
    for _ in range(500):
        left_n, right_n = rng.randint(0, 7), rng.randint(0, 7)
        adjacency = random_bipartite(rng, left_n, right_n, rng.choice([0.15, 0.3, 0.6]))
        expected = brute_force_matching(left_n, adjacency)
        for algorithm in (solution.kuhn_matching, solution.hopcroft_karp):
            size, match_left, match_right = algorithm(left_n, right_n, adjacency)
            assert size == expected, (algorithm.__name__, left_n, right_n, adjacency)
            assert_valid_matching(left_n, right_n, adjacency, size, match_left, match_right)


def test_augmenting_path_must_rearrange_earlier_choices():
    # 0-{0,1}, 1-{0}: 0 이 먼저 정점 0 을 가져가도 1 을 위해 정점 1 로 옮겨야 완전 매칭
    for algorithm in (solution.kuhn_matching, solution.hopcroft_karp):
        assert algorithm(2, 2, [[0, 1], [0]])[0] == 2
        assert algorithm(3, 3, [[0, 1], [0, 2], [0]])[0] == 3
        assert algorithm(3, 2, [[0], [0], [0, 1]])[0] == 2


def brute_force_min_cover_size(left_n, right_n, adjacency):
    vertices = [("L", u) for u in range(left_n)] + [("R", v) for v in range(right_n)]
    edges = [(("L", u), ("R", v)) for u in range(left_n) for v in adjacency[u]]
    for k in range(len(vertices) + 1):
        for subset in itertools.combinations(vertices, k):
            chosen = set(subset)
            if all(a in chosen or b in chosen for a, b in edges):
                return k
    return 0


def test_konig_vertex_cover_and_independent_set():
    rng = random.Random(1)
    for _ in range(300):
        left_n, right_n = rng.randint(0, 6), rng.randint(0, 6)
        adjacency = random_bipartite(rng, left_n, right_n, rng.choice([0.2, 0.4, 0.7]))
        matching = solution.hopcroft_karp(left_n, right_n, adjacency)[0]
        left_cover, right_cover = solution.minimum_vertex_cover(left_n, right_n, adjacency)
        cover_left, cover_right = set(left_cover), set(right_cover)
        assert all(u in cover_left or v in cover_right for u in range(left_n) for v in adjacency[u]), adjacency
        assert len(left_cover) + len(right_cover) == matching == brute_force_min_cover_size(left_n, right_n, adjacency)
        left_free, right_free = solution.maximum_independent_set(left_n, right_n, adjacency)
        free_left, free_right = set(left_free), set(right_free)
        assert not any(u in free_left and v in free_right for u in range(left_n) for v in adjacency[u])
        assert len(left_free) + len(right_free) == left_n + right_n - matching


def brute_force_min_path_cover(n, edges):
    best = n
    for k in range(len(edges) + 1):
        for subset in itertools.combinations(edges, k):
            outs = [a for a, _ in subset]
            ins = [b for _, b in subset]
            if len(set(outs)) == len(outs) and len(set(ins)) == len(ins):  # 각 정점이 이어지는 간선을 최대 하나씩만 쓴다
                best = min(best, n - k)
    return best


def test_min_path_cover_in_dag_matches_brute_force():
    rng = random.Random(2)
    for _ in range(200):
        n = rng.randint(1, 6)
        edges = [(a, b) for a in range(n) for b in range(a + 1, n) if rng.random() < 0.35]  # a < b 라서 DAG
        assert solution.min_path_cover(n, edges) == brute_force_min_path_cover(n, edges), (n, edges)
    assert solution.min_path_cover(4, [(0, 1), (0, 2), (0, 3)]) == 3  # 한 정점에서 나가는 경로는 하나뿐
    assert solution.min_path_cover(0, []) == 0


def test_large_random_graphs_agree_and_hopcroft_karp_handles_long_alternating_paths():
    rng = random.Random(3)
    n = 3000
    adjacency = [rng.sample(range(n), 3) for _ in range(n)]
    assert solution.kuhn_matching(n, n, adjacency)[0] == solution.hopcroft_karp(n, n, adjacency)[0]
    # 사다리 모양: u 는 u 와 u + 1 에 연결, 마지막 정점은 u 에만 → 증가 경로가 매우 길어질 수 있다
    n = 50_000
    ladder = [[u, u + 1] for u in range(n - 1)] + [[n - 1]]
    size, match_left, match_right = solution.hopcroft_karp(n, n, ladder)
    assert size == n
    assert_valid_matching(n, n, ladder, size, match_left, match_right)
    assert solution.kuhn_matching(n, n, ladder)[0] == n


def test_main(monkeypatch, capsys):
    text = "5 5\n2 2 5\n3 2 3 4\n2 1 5\n3 1 2 5\n1 5\n"
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(text.encode())))
    solution.main()
    adjacency = [[1, 4], [1, 2, 3], [0, 4], [0, 1, 4], [4]]
    assert int(capsys.readouterr().out) == brute_force_matching(5, adjacency) == 4
