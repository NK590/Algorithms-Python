"""플로이드-워셜 알고리즘 — 모든 정점 쌍의 최단 거리를 한 번에 (DP, O(V³))

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 간선 목록 `edges = [(u, v, w), ...]` (u → v, 가중치 w) 와 정점 수 `n` 으로 받고, 정점 번호는 0 ~ n-1 입니다.
- 핵심: "정점 0..k 만 거쳐도 된다"는 조건으로 최단 거리를 k 를 늘려 가며 갱신한다. 바깥 반복이 거쳐 가는 정점 k 다.
- 도달할 수 없는 쌍의 거리는 INF 입니다. 음수 간선이 있어도 되지만, 음수 사이클이 있으면 값이 의미를 잃습니다.
- 직접 실행하면 아래 형식의 입력을 받아 모든 쌍의 최단 거리 표를 출력합니다. (도달 불가는 0)

      N            정점 수
      M            간선 수
      a b c        (M 줄) a → b 간선, 가중치 c. 같은 쌍이 여러 번 나오면 최솟값
"""
import sys

INF = float("inf")

Edge = tuple[int, int, int]


def init_matrix(n: int, edges: list[Edge]) -> list[list[float]]:
    """dist[i][j] = i → j 로 가는 간선 하나의 최소 가중치 (자기 자신은 0, 간선이 없으면 INF)."""
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        if w < dist[u][v]:  # 같은 쌍의 중복 간선은 가장 작은 것만
            dist[u][v] = w
    return dist


def floyd_warshall(n: int, edges: list[Edge]) -> list[list[float]]:
    """모든 쌍의 최단 거리 행렬. 바깥 반복의 k 가 "거쳐 가도 되는 정점 0..k" 를 늘려 간다."""
    dist = init_matrix(n, edges)
    for k in range(n):
        dk = dist[k]
        for i in range(n):
            dik = dist[i][k]
            if dik == INF:
                continue
            di = dist[i]
            for j in range(n):
                if dik + dk[j] < di[j]:  # i → k → j 가 지금까지 알던 i → j 보다 짧으면
                    di[j] = dik + dk[j]
    return dist


def floyd_warshall_with_next(n: int, edges: list[Edge]) -> tuple[list[list[float]], list[list[int]]]:
    """최단 거리와 함께, next_hop[i][j] = i 에서 j 로 가는 최단 경로의 첫 번째 다음 정점(없으면 -1)을 돌려준다."""
    dist = init_matrix(n, edges)
    next_hop = [[-1] * n for _ in range(n)]
    for i in range(n):
        next_hop[i][i] = i
    for u, v, w in edges:
        if w == dist[u][v] and u != v:
            next_hop[u][v] = v
    for k in range(n):
        for i in range(n):
            if dist[i][k] == INF:
                continue
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_hop[i][j] = next_hop[i][k]
    return dist, next_hop


def restore_path(next_hop: list[list[int]], u: int, v: int) -> list[int]:
    """u → v 최단 경로의 정점 목록. 도달할 수 없으면 빈 리스트. 음수 사이클이 없을 때만 올바르다."""
    if next_hop[u][v] == -1:
        return []
    path = [u]
    while u != v:
        u = next_hop[u][v]
        path.append(u)
    return path


def has_negative_cycle(dist: list[list[float]]) -> bool:
    """floyd_warshall 이 끝난 뒤 자기 자신으로 가는 거리가 음수인 정점이 있으면 음수 사이클이 있다."""
    return any(dist[i][i] < 0 for i in range(len(dist)))


def transitive_closure(n: int, edges: list[tuple[int, int]]) -> list[list[bool]]:
    """reach[i][j] = i 에서 j 로 갈 수 있는가 (자기 자신은 항상 True). 워셜 알고리즘: 거리 대신 "갈 수 있다" 만 OR/AND 로 갱신한다.

    각 행을 파이썬 정수 하나(비트마스크)로 들고 있으면 안쪽 반복이 비트 연산 한 번으로 끝난다."""
    rows = [1 << i for i in range(n)]
    for u, v in edges:
        rows[u] |= 1 << v
    for k in range(n):
        for i in range(n):
            if rows[i] >> k & 1:  # i → k 로 갈 수 있으면 k 가 갈 수 있는 곳도 모두 갈 수 있다
                rows[i] |= rows[k]
    return [[bool(rows[i] >> j & 1) for j in range(n)] for i in range(n)]


def shortest_cycle(n: int, edges: list[Edge]) -> float:
    """방향 그래프에서 가장 짧은 사이클의 길이 (없으면 INF). 자기 자신으로 돌아오는 거리를 0 이 아니라 INF 에서 시작해 구한다."""
    dist = [[INF] * n for _ in range(n)]
    for u, v, w in edges:
        if w < dist[u][v]:
            dist[u][v] = w
    for k in range(n):
        for i in range(n):
            if dist[i][k] == INF:
                continue
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return min(dist[i][i] for i in range(n)) if n else INF


def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    m = int(input())
    edges = []
    for _ in range(m):
        a, b, c = map(int, input().split())
        edges.append((a - 1, b - 1, c))
    dist = floyd_warshall(n, edges)
    for row in dist:
        print(" ".join(str(d) if d != INF else "0" for d in row))


if __name__ == "__main__":
    main()
