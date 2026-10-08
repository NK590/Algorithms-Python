"""이분 그래프 판별 — 정점을 두 집합으로 나눠 모든 간선이 서로 다른 집합을 잇게 할 수 있는가

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 정리: 이분 그래프 ⇔ 길이가 홀수인 사이클이 없다. 한 정점을 색 0 으로 칠하고, 이웃은 반대 색으로 칠해 나가다 충돌이 나면 아니다.
- 그래프는 무방향 인접 리스트 `graph[u] = [v, ...]` (양방향이면 양쪽에 모두 넣는다), 정점 번호는 0 ~ n-1 입니다.
  연결되어 있지 않을 수 있으므로 아직 칠하지 않은 정점마다 BFS 를 새로 시작합니다.
- 직접 실행하면 아래 형식의 입력(이분 그래프)을 받아 테스트 케이스마다 YES/NO 를 출력합니다. (정점은 1부터)

      K            테스트 케이스 수
      V E          (케이스마다) 정점 수, 간선 수
      u v          (E 줄) u 와 v 를 잇는 간선
"""
import sys
from collections import deque

Graph = list[list[int]]


def two_color(graph: Graph) -> list[int] | None:
    """각 정점의 색(0 또는 1) 목록. 이분 그래프가 아니면 None. 색 0 과 1 이 두 집합이다."""
    n = len(graph)
    color = [-1] * n
    for s in range(n):
        if color[s] != -1:
            continue
        color[s] = 0
        queue = deque([s])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]  # 이웃은 반대 색
                    queue.append(v)
                elif color[v] == color[u]:  # 같은 색끼리 이어져 있다 (자기 자신으로의 간선도 여기서 걸린다)
                    return None
    return color


def is_bipartite(graph: Graph) -> bool:
    return two_color(graph) is not None


def partition(graph: Graph) -> tuple[list[int], list[int]] | None:
    """두 집합 (색 0 인 정점들, 색 1 인 정점들). 이분 그래프가 아니면 None."""
    color = two_color(graph)
    if color is None:
        return None
    return [v for v, c in enumerate(color) if c == 0], [v for v, c in enumerate(color) if c == 1]


def odd_cycle(graph: Graph) -> list[int] | None:
    """이분 그래프가 아닐 때 길이가 홀수인 사이클 하나를 정점 순서대로 반환한다. 이분 그래프이면 None.

    BFS 트리에서 같은 색(= 깊이의 홀짝이 같은) 두 정점 u, v 가 간선으로 이어지면, 두 정점에서 공통 조상까지 올라온 경로와
    간선 (u, v) 가 합쳐져 홀수 길이의 사이클이 된다. (u == v 인 자기 루프는 u 하나로 이루어진 길이 1 의 사이클로 같은 식에서 나온다)"""
    n = len(graph)
    color = [-1] * n
    parent = [-1] * n
    for s in range(n):
        if color[s] != -1:
            continue
        color[s] = 0
        queue = deque([s])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    parent[v] = u
                    queue.append(v)
                elif color[v] == color[u]:
                    ancestors = {}
                    x, depth = u, 0
                    while x != -1:
                        ancestors[x] = depth
                        x, depth = parent[x], depth + 1
                    path_v = []
                    y = v
                    while y not in ancestors:
                        path_v.append(y)
                        y = parent[y]
                    lca = y
                    path_u = []
                    x = u
                    while x != lca:
                        path_u.append(x)
                        x = parent[x]
                    # u → … → (lca 바로 아래) → lca → (lca 바로 아래) → … → v → 다시 u
                    return path_u + [lca] + path_v[::-1]
    return None


def is_bipartite_dsu(n: int, edges: list[tuple[int, int]]) -> bool:
    """유니온 파인드로 판별한다. 정점 x 마다 "x 가 색 0" 과 "x 가 색 1" 두 노드(x 와 x + n)를 두고,
    간선 (u, v) 는 "u 가 0 이면 v 는 1, u 가 1 이면 v 는 0" 이므로 (u, v + n) 과 (u + n, v) 를 합친다.
    어떤 x 에서 x 와 x + n 이 같은 집합이 되면 모순이다."""
    parent = list(range(2 * n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        parent[find(u)] = find(v + n)
        parent[find(u + n)] = find(v)
    return all(find(x) != find(x + n) for x in range(n))


def main() -> None:
    input = sys.stdin.readline
    k = int(input())
    out = []
    for _ in range(k):
        v, e = map(int, input().split())
        graph: Graph = [[] for _ in range(v)]
        for _ in range(e):
            a, b = map(int, input().split())
            graph[a - 1].append(b - 1)
            graph[b - 1].append(a - 1)
        out.append("YES" if is_bipartite(graph) else "NO")
    print("\n".join(out))


if __name__ == "__main__":
    main()
