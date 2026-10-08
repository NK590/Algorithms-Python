"""solution.py 검증: 무작위 트리에서 정의를 그대로 옮긴 느린 계산과 비교"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def random_tree(rng, n):
    """정점 이름을 섞은 무작위 트리: (간선 목록, 루트로 삼을 정점, 진짜 부모 배열)"""
    labels = list(range(n))
    rng.shuffle(labels)
    true_parent = [-1] * n
    edges = []
    for i in range(1, n):
        p = rng.randrange(i)
        true_parent[labels[i]] = labels[p]
        edges.append((labels[p], labels[i]) if rng.random() < 0.5 else (labels[i], labels[p]))
    rng.shuffle(edges)
    return edges, labels[0], true_parent


def test_readme_example():
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5)]
    parent, children, order = solution.build_rooted_tree(6, edges, root=0)
    assert parent == [-1, 0, 0, 1, 1, 2]
    assert children == [[1, 2], [3, 4], [5], [], [], []]
    assert order == [0, 1, 2, 3, 4, 5]
    assert solution.depths(parent, order) == [0, 1, 1, 2, 2, 2]
    assert solution.subtree_sizes(parent, order) == [6, 3, 2, 1, 1, 1]
    assert solution.leaves(children) == [3, 4, 5]
    assert solution.path_to_root(parent, 4) == [4, 1, 0]


def test_parents_match_the_tree_the_edges_were_made_from():
    rng = random.Random(0)
    for _ in range(300):
        n = rng.randint(1, 12)
        edges, root, true_parent = random_tree(rng, n)
        parent, children, order = solution.build_rooted_tree(n, edges, root)
        assert parent == true_parent
        assert sorted(order) == list(range(n)) and order[0] == root
        assert all(parent[v] == u for u in range(n) for v in children[u])


def test_depth_and_subtree_size_match_brute_force():
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(1, 12)
        edges, root, _ = random_tree(rng, n)
        parent, _, order = solution.build_rooted_tree(n, edges, root)
        depth = solution.depths(parent, order)
        size = solution.subtree_sizes(parent, order)
        for v in range(n):
            assert depth[v] == len(solution.path_to_root(parent, v)) - 1
            # v 의 서브트리 = v 를 조상으로 갖는 정점(자기 포함)
            assert size[v] == sum(v in solution.path_to_root(parent, w) for w in range(n))


def test_is_tree():
    assert solution.is_tree(1, [])
    assert solution.is_tree(3, [(0, 1), (1, 2)])
    assert not solution.is_tree(3, [(0, 1)])  # 연결되지 않았다
    assert not solution.is_tree(3, [(0, 1), (1, 2), (2, 0)])  # 간선이 너무 많다
    assert not solution.is_tree(4, [(0, 1), (1, 2), (2, 0)])  # 간선 수는 n-1 이지만 사이클이 있고 3번이 떨어져 있다
    assert not solution.is_tree(0, [])
    rng = random.Random(2)
    for _ in range(200):
        n = rng.randint(1, 10)
        edges, _, _ = random_tree(rng, n)
        assert solution.is_tree(n, edges)


def test_deep_tree_does_not_need_recursion():
    n = 100_000
    edges = [(i, i + 1) for i in range(n - 1)]
    parent, _, order = solution.build_rooted_tree(n, edges, 0)
    assert solution.depths(parent, order)[-1] == n - 1
    assert solution.subtree_sizes(parent, order)[0] == n


def test_main_prints_parents(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("5\n1 2\n1 3\n3 4\n3 5\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["1", "1", "3", "3"]
