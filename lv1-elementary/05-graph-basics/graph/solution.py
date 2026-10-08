"""그래프의 표현 — 정점과 간선을 코드로 담는 방법 (간선 목록, 인접 행렬, 인접 리스트)

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 정점은 0 ~ n-1 번이고, 간선은 (u, v) 또는 가중치가 있는 (u, v, w) 튜플입니다. 가중치가 없으면 1 로 봅니다.
- 직접 실행하면 `V E` 와 E 개의 `u v` (정점 번호는 1부터) 를 받아, 정점마다 이웃을 한 줄씩 출력합니다.
"""
import sys

INF = float("inf")


def _parse(edge):
    u, v = edge[0], edge[1]
    return u, v, (edge[2] if len(edge) > 2 else 1)


def build_adjacency_matrix(n: int, edges: list, directed: bool = False, no_edge=0) -> list:
    """matrix[u][v] = u → v 간선의 가중치, 간선이 없으면 no_edge. 메모리 O(n²), 간선 유무 확인 O(1).

    가중치가 0 인 간선이 있을 수 있다면 no_edge 를 INF 로 두어야 "간선 없음"과 구분된다.
    같은 쌍의 간선이 여러 개면 마지막 것이 남는다.
    """
    matrix = [[no_edge] * n for _ in range(n)]
    for edge in edges:
        u, v, w = _parse(edge)
        matrix[u][v] = w
        if not directed:
            matrix[v][u] = w
    return matrix


def build_adjacency_list(n: int, edges: list, directed: bool = False) -> list:
    """adj[u] = u 에서 나가는 간선의 도착 정점들. 메모리 O(n + E), 이웃 훑기 O(차수).

    무방향 간선은 양쪽에 모두 넣는다. 자기 자신으로 가는 간선은 한 번만 넣는다.
    """
    adj = [[] for _ in range(n)]
    for edge in edges:
        u, v = edge[0], edge[1]
        adj[u].append(v)
        if not directed and u != v:
            adj[v].append(u)
    return adj


def build_weighted_adjacency_list(n: int, edges: list, directed: bool = False) -> list:
    """adj[u] = [(v, w), ...]. 다익스트라 같은 최단 경로 알고리즘이 쓰는 형태."""
    adj = [[] for _ in range(n)]
    for edge in edges:
        u, v, w = _parse(edge)
        adj[u].append((v, w))
        if not directed and u != v:
            adj[v].append((u, w))
    return adj


def matrix_to_list(matrix: list, no_edge=0) -> list:
    """인접 행렬을 인접 리스트로 바꾼다. 행 전체를 훑으므로 O(n²)."""
    return [[v for v, w in enumerate(row) if w != no_edge] for row in matrix]


def list_to_matrix(adj: list) -> list:
    """인접 리스트를 (가중치 없는) 인접 행렬로 바꾼다. 간선이 있으면 1."""
    matrix = [[0] * len(adj) for _ in adj]
    for u, neighbors in enumerate(adj):
        for v in neighbors:
            matrix[u][v] = 1
    return matrix


def has_edge_matrix(matrix: list, u: int, v: int, no_edge=0) -> bool:
    """O(1)"""
    return matrix[u][v] != no_edge


def has_edge_list(adj: list, u: int, v: int) -> bool:
    """O(u 의 차수)"""
    return v in adj[u]


def degrees(adj: list, directed: bool = False):
    """무방향이면 정점별 차수 리스트, 방향이면 (진입 차수 리스트, 진출 차수 리스트)."""
    out_degree = [len(neighbors) for neighbors in adj]
    if not directed:
        return out_degree
    in_degree = [0] * len(adj)
    for neighbors in adj:
        for v in neighbors:
            in_degree[v] += 1
    return in_degree, out_degree


def main() -> None:
    input = sys.stdin.readline
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        u, v = map(int, input().split())
        edges.append((u - 1, v - 1))  # 입력은 1번부터, 코드는 0번부터
    adj = build_adjacency_list(n, edges)
    for u in range(n):
        print(u + 1, ":", *(v + 1 for v in sorted(adj[u])))


if __name__ == "__main__":
    main()
