"""solution.py 검증: 모든 정점에서 BFS 를 돌려 모든 쌍의 거리를 구하는 브루트포스와 비교"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def random_tree(rng, max_n=12, low=0, high=9):
    n = rng.randint(1, max_n)
    perm = list(range(n))
    rng.shuffle(perm)
    edges = [(perm[rng.randrange(i)], perm[i], rng.randint(low, high)) for i in range(1, n)]
    return n, edges


def all_pair_distances(n, edges):
    """플로이드-워셜 (트리라서 경로가 하나뿐)"""
    inf = float("inf")
    d = [[inf] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for u, v, w in edges:
        d[u][v] = d[v][u] = w
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d


def test_diameter_matches_all_pairs_maximum():
    rng = random.Random(0)
    for _ in range(600):
        n, edges = random_tree(rng)
        d = all_pair_distances(n, edges)
        expected = max(max(row) for row in d)
        length, u, v = solution.tree_diameter(n, edges)
        assert length == expected == solution.tree_diameter_dp(n, edges), (n, edges)
        assert d[u][v] == length


def test_diameter_path_is_a_real_path_with_that_length():
    rng = random.Random(1)
    for _ in range(300):
        n, edges = random_tree(rng)
        length, u, v = solution.tree_diameter(n, edges)
        path = solution.diameter_path(n, edges)
        assert path[0] in (u, v) and path[-1] in (u, v)
        weight = {}
        for a, b, w in edges:
            weight[(a, b)] = weight[(b, a)] = w
        assert sum(weight[(a, b)] for a, b in zip(path, path[1:])) == length
        assert len(set(path)) == len(path)


def test_eccentricity_and_centers_match_brute_force():
    rng = random.Random(2)
    for _ in range(400):
        n, edges = random_tree(rng, low=1)
        d = all_pair_distances(n, edges)
        expected = [max(row) for row in d]
        assert solution.eccentricities(n, edges) == expected, (n, edges)
        smallest = min(expected)
        assert solution.tree_centers(n, edges) == [x for x in range(n) if expected[x] == smallest]
        assert len(solution.tree_centers(n, edges)) in (1, 2)


def test_small_and_special_trees():
    assert solution.tree_diameter(1, []) == (0, 0, 0)
    assert solution.tree_diameter_dp(1, []) == 0
    assert solution.diameter_path(1, []) == [0] and solution.diameter_path(0, []) == []
    assert solution.eccentricities(1, []) == [0] and solution.eccentricities(0, []) == []
    assert solution.tree_diameter(2, [(0, 1, 5)])[0] == 5
    assert solution.tree_diameter(4, [(0, 1, 0), (1, 2, 0), (2, 3, 0)])[0] == 0  # 가중치가 모두 0


def test_readme_example():
    # 정점 0..5: 0-1(3), 1-2(2), 1-3(4), 3-4(1), 3-5(6)
    edges = [(0, 1, 3), (1, 2, 2), (1, 3, 4), (3, 4, 1), (3, 5, 6)]
    assert solution.tree_diameter(6, edges)[0] == 13  # 0 - 1 - 3 - 5
    assert sorted(solution.diameter_path(6, edges)) == [0, 1, 3, 5]
    assert solution.eccentricities(6, edges) == [13, 10, 12, 7, 8, 13]
    assert solution.tree_centers(6, edges) == [3]


def test_a_long_path_does_not_recurse():
    n = 100_000
    edges = [(i, i + 1, 1) for i in range(n - 1)]
    assert solution.tree_diameter(n, edges)[0] == n - 1
    assert solution.tree_diameter_dp(n, edges) == n - 1
    assert sorted(solution.tree_centers(n, edges)) == [n // 2 - 1, n // 2]


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("5\n1 2 3\n1 3 2\n2 4 4\n2 5 3\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "9"
