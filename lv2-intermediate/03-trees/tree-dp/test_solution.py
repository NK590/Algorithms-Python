"""solution.py 검증: 모든 정점 부분집합(2ⁿ)을 시도하는 브루트포스와 비교"""
import io
import itertools
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def random_tree(rng, max_n=11):
    n = rng.randint(1, max_n)
    edges = [(rng.randrange(i), i) for i in range(1, n)]
    # 정점 번호를 섞어서 루트(0)가 항상 부모 쪽에 있는 특수한 모양을 피한다
    perm = list(range(n))
    rng.shuffle(perm)
    return n, [(perm[u], perm[v]) for u, v in edges]


def subsets(n):
    for mask in range(1 << n):
        yield mask, [v for v in range(n) if mask >> v & 1]


def brute_force_independent_set(n, weights, edges):
    best = 0
    for mask, picked in subsets(n):
        if all(not (mask >> u & 1 and mask >> v & 1) for u, v in edges):
            best = max(best, sum(weights[v] for v in picked))
    return best


def brute_force_vertex_cover(n, edges):
    return min(len(p) for mask, p in subsets(n) if all(mask >> u & 1 or mask >> v & 1 for u, v in edges))


def brute_force_dominating_set(n, edges):
    adj = [[v] for v in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return min(len(p) for mask, p in subsets(n) if all(any(mask >> w & 1 for w in adj[v]) for v in range(n)))


def test_independent_set_matches_brute_force_and_reconstruction_is_valid():
    rng = random.Random(0)
    for _ in range(500):
        n, edges = random_tree(rng)
        weights = [rng.randint(1, 9) for _ in range(n)]
        total, chosen = solution.max_weight_independent_set(n, weights, edges)
        assert total == brute_force_independent_set(n, weights, edges), (n, weights, edges)
        assert sum(weights[v] for v in chosen) == total
        assert all(not (u in chosen and v in chosen) for u, v in edges)


def test_independent_set_with_zero_and_negative_weights():
    # 가중치가 0 이하인 정점은 고르지 않는 것이 낫다
    total, chosen = solution.max_weight_independent_set(3, [-5, 4, -1], [(0, 1), (1, 2)])
    assert (total, chosen) == (4, [1])
    assert solution.max_weight_independent_set(1, [7], []) == (7, [0])
    assert solution.max_weight_independent_set(0, [], []) == (0, [])


def test_vertex_cover_matches_brute_force():
    rng = random.Random(1)
    for _ in range(500):
        n, edges = random_tree(rng)
        assert solution.min_vertex_cover(n, edges) == brute_force_vertex_cover(n, edges), (n, edges)
    assert solution.min_vertex_cover(1, []) == 0
    assert solution.min_vertex_cover(0, []) == 0


def test_vertex_cover_plus_independent_set_equals_n_for_unit_weights():
    # 쾨니그/갈라이 정리: 최소 정점 덮개 + 최대 독립 집합 = n
    rng = random.Random(2)
    for _ in range(200):
        n, edges = random_tree(rng, max_n=14)
        total, _ = solution.max_weight_independent_set(n, [1] * n, edges)
        assert solution.min_vertex_cover(n, edges) + total == n


def test_dominating_set_matches_brute_force():
    rng = random.Random(3)
    for _ in range(500):
        n, edges = random_tree(rng)
        assert solution.min_dominating_set(n, edges) == brute_force_dominating_set(n, edges), (n, edges)
    assert solution.min_dominating_set(1, []) == 1
    assert solution.min_dominating_set(0, []) == 0
    assert solution.min_dominating_set(2, [(0, 1)]) == 1
    # 별 모양: 가운데 하나면 충분하다
    assert solution.min_dominating_set(6, [(0, i) for i in range(1, 6)]) == 1


def test_a_deep_tree_does_not_recurse():
    n = 100_000
    edges = [(i, i + 1) for i in range(n - 1)]  # 사슬
    total, _ = solution.max_weight_independent_set(n, [1] * n, edges)
    assert total == (n + 1) // 2
    assert solution.min_vertex_cover(n, edges) == n // 2
    assert solution.min_dominating_set(n, edges) == (n + 2) // 3


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("5\n1 2 3 4 5\n1 2\n1 3\n2 4\n2 5\n"))
    solution.main()
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == "12" and lines[1] == "3 4 5"
