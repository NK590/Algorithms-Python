"""트리 — 사이클이 없고 연결된 그래프, 루트를 정하면 부모-자식 관계가 생긴다

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 정점은 0 ~ n-1 번입니다. 간선은 (u, v) 무방향이고, 트리는 정점이 n 개면 간선이 정확히 n-1 개입니다.
- 직접 실행하면 `N` 과 N-1 개의 간선(정점 번호는 1부터)을 받아, 1번을 루트로 했을 때 2번부터 N번까지의 부모를 출력합니다.
"""
import sys
from collections import deque


def _adjacency(n: int, edges: list) -> list:
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def is_tree(n: int, edges: list) -> bool:
    """n 개의 정점과 주어진 간선이 트리인지. 간선이 n-1 개이고 모든 정점이 연결되어 있으면 트리다."""
    if n == 0 or len(edges) != n - 1:
        return False
    adj = _adjacency(n, edges)
    seen = [False] * n
    seen[0] = True
    queue = deque([0])
    reached = 1
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                reached += 1
                queue.append(v)
    return reached == n  # 간선이 n-1 개인데 연결되어 있으면 사이클이 있을 수 없다


def build_rooted_tree(n: int, edges: list, root: int = 0) -> tuple:
    """루트를 정해 (parent, children, order) 를 만든다. parent[root] 는 -1.

    order 는 루트에서 가까운 순서(BFS)라서, 어떤 정점도 자신의 부모보다 먼저 나오지 않는다.
    """
    adj = _adjacency(n, edges)
    parent = [-1] * n
    children = [[] for _ in range(n)]
    order = [root]
    seen = [False] * n
    seen[root] = True
    for u in order:  # order 에 원소를 추가하면서 순회하면 BFS 가 된다
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                parent[v] = u
                children[u].append(v)
                order.append(v)
    return parent, children, order


def depths(parent: list, order: list) -> list:
    """루트의 깊이를 0 으로 했을 때 정점별 깊이. order 순서대로 부모의 깊이 + 1."""
    depth = [0] * len(parent)
    for v in order[1:]:
        depth[v] = depth[parent[v]] + 1
    return depth


def subtree_sizes(parent: list, order: list) -> list:
    """정점별 서브트리의 크기(자기 자신 포함). 자식에서 부모로 거꾸로 올라가며 더한다."""
    size = [1] * len(parent)
    for v in reversed(order):
        if parent[v] != -1:
            size[parent[v]] += size[v]
    return size


def leaves(children: list) -> list:
    """자식이 없는 정점들."""
    return [v for v, kids in enumerate(children) if not kids]


def path_to_root(parent: list, v: int) -> list:
    """v 에서 루트까지의 경로 (v 가 맨 앞, 루트가 맨 뒤)."""
    path = [v]
    while parent[path[-1]] != -1:
        path.append(parent[path[-1]])
    return path


def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    edges = []
    for _ in range(n - 1):
        u, v = map(int, input().split())
        edges.append((u - 1, v - 1))
    parent, _, _ = build_rooted_tree(n, edges, root=0)
    print("\n".join(str(parent[v] + 1) for v in range(1, n)))


if __name__ == "__main__":
    main()
