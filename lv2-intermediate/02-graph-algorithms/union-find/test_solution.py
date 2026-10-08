"""solution.py 검증: 라벨을 통째로 바꾸는 느리지만 확실한 방법과 랜덤 비교 + 최적화가 실제로 효과가 있는지 확인"""
import io
import math
import random

from tools.loader import load_solution

solution = load_solution(__file__)


class SlowSets:
    """원소마다 집합 번호(라벨)를 두고, 합칠 때 라벨을 모두 바꾸는 O(n) 방식"""

    def __init__(self, n):
        self.label = list(range(n))

    def union(self, a, b):
        la, lb = self.label[a], self.label[b]
        if la == lb:
            return False
        self.label = [la if x == lb else x for x in self.label]
        return True

    def connected(self, a, b):
        return self.label[a] == self.label[b]

    def size_of(self, x):
        return self.label.count(self.label[x])

    def count(self):
        return len(set(self.label))

    def groups(self):
        by_label = {}
        for i, lab in enumerate(self.label):
            by_label.setdefault(lab, []).append(i)
        return sorted(by_label.values(), key=lambda g: g[0])


def test_matches_slow_sets_on_random_operations():
    rng = random.Random(0)
    for _ in range(300):
        n = rng.randint(1, 12)
        fast, slow = solution.UnionFind(n), SlowSets(n)
        for _ in range(rng.randint(0, 30)):
            a, b = rng.randrange(n), rng.randrange(n)
            if rng.random() < 0.5:
                assert fast.union(a, b) == slow.union(a, b)
            else:
                assert fast.connected(a, b) == slow.connected(a, b)
            x = rng.randrange(n)
            assert fast.size_of(x) == slow.size_of(x)
        assert fast.count == slow.count()
        assert fast.groups() == slow.groups()


def test_basic_behaviour():
    uf = solution.UnionFind(5)
    assert uf.count == 5 and not uf.connected(0, 1)
    assert uf.union(0, 1) is True and uf.union(1, 0) is False  # 이미 같은 집합
    assert uf.connected(0, 1) and uf.size_of(0) == 2 and uf.count == 4
    uf.union(2, 3)
    uf.union(1, 3)
    assert uf.groups() == [[0, 1, 2, 3], [4]]
    assert uf.union(2, 2) is False


def depth(uf, x):
    d = 0
    while uf.parent[x] != x:
        x = uf.parent[x]
        d += 1
    return d


def test_union_by_size_keeps_trees_shallow_without_any_find_compression():
    # 합칠 때는 find 로 루트를 찾으므로 압축이 일어난다. 압축 없이 깊이만 보려면 부모를 직접 읽는다.
    # 가장 깊어지는 순서(같은 크기끼리 반복해서 합치기)에서도 깊이가 log2(n) 을 넘지 않는다.
    n = 1024
    uf = solution.UnionFind(n)
    step = 1
    while step < n:
        for i in range(0, n, 2 * step):
            uf.union(i, i + step)
        step *= 2
    assert max(depth(uf, x) for x in range(n)) <= int(math.log2(n))


def test_chain_of_unions_does_not_build_a_deep_tree():
    n = 2000
    # 큰 집합이 union 의 왼쪽에 오는 순서와 오른쪽에 오는 순서 모두에서 깊이가 log2(n) 이하여야 한다
    for join in (lambda uf, i: uf.union(i, i + 1), lambda uf, i: uf.union(i + 1, i)):
        uf = solution.UnionFind(n)
        for i in range(n - 1):
            join(uf, i)
        assert max(depth(uf, x) for x in range(n)) <= int(math.log2(n))


def test_find_compresses_the_whole_path():
    uf = solution.UnionFind(6)
    uf.parent = [0, 0, 1, 2, 3, 4]  # 5 → 4 → 3 → 2 → 1 → 0 으로 이어진 깊이 5 의 사슬
    assert uf.find(5) == 0
    assert all(uf.parent[x] == 0 for x in range(6))  # 지나온 모든 원소가 루트에 직접 연결


def test_find_on_a_very_deep_tree_does_not_recurse():
    n = 200_000
    uf = solution.UnionFind(n)
    uf.parent = [0] + list(range(n - 1))  # i 의 부모가 i-1 인 사슬
    assert uf.find(n - 1) == 0


def test_count_components_matches_depth_first_search():
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(1, 12)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 14))]
        adj = {i: set() for i in range(n)}
        for a, b in edges:
            adj[a].add(b)
            adj[b].add(a)
        seen, comps = set(), 0
        for s in range(n):
            if s in seen:
                continue
            comps += 1
            stack = [s]
            seen.add(s)
            while stack:
                u = stack.pop()
                for v in adj[u]:
                    if v not in seen:
                        seen.add(v)
                        stack.append(v)
        assert solution.count_components(n, edges) == comps, (n, edges)


def test_first_cycle_edge_matches_prefix_search():
    rng = random.Random(2)
    for _ in range(400):
        n = rng.randint(1, 10)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 12))]
        # 앞에서부터 i 개의 간선을 쓴 그래프에 사이클이 생기는가: 간선 수 > n - (연결 요소 수) 이면 사이클
        expected = 0
        for i in range(1, len(edges) + 1):
            comps = solution.count_components(n, edges[:i])
            if i > n - comps:
                expected = i
                break
        assert solution.first_cycle_edge(n, edges) == expected, (n, edges)
    assert solution.first_cycle_edge(3, [(0, 1), (1, 2), (0, 1)]) == 3  # 중복 간선도 사이클
    assert solution.first_cycle_edge(3, [(0, 0)]) == 1  # 자기 자신으로의 간선
    assert solution.first_cycle_edge(4, [(0, 1), (1, 2), (2, 3)]) == 0


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("7 8\n0 1 3\n1 1 7\n0 7 6\n1 7 1\n0 3 7\n0 4 2\n0 1 1\n1 1 1\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["NO", "NO", "YES"]
