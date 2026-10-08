"""0-1 BFS — 간선 가중치가 0 또는 1 일 때 덱(deque)으로 O(V+E) 에 구하는 최단 거리

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 가중치 0 인 간선으로 닿는 정점은 덱의 **앞**에, 가중치 1 인 간선은 **뒤**에 넣는다. 덱은 항상 "거리 d 인 정점들, 그 뒤에 거리 d+1 인 정점들" 순서가 유지된다.
- 그래프는 인접 리스트 `graph[u] = [(v, w), ...]` (w 는 0 또는 1), 정점 번호는 0 ~ n-1 입니다.
- 도달할 수 없는 정점의 거리는 INF 입니다.
- 직접 실행하면 아래 형식의 입력(알고스팟)을 받아, 왼쪽 위에서 오른쪽 아래까지 벽을 최소 몇 개 부수면 가는지 출력합니다.

      M N          가로 M, 세로 N
      N 줄         각 줄은 길이 M 의 0/1 문자열 (0 = 빈 방, 1 = 벽)
"""
import sys
from collections import deque

INF = float("inf")


def zero_one_bfs(graph: list[list[tuple[int, int]]], start: int) -> list[float]:
    """start 에서 모든 정점까지의 최단 거리. 모든 가중치가 0 또는 1 이어야 한다."""
    dist = [INF] * len(graph)
    dist[start] = 0
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                if w == 0:
                    queue.appendleft(v)  # 같은 거리이므로 앞쪽에서 먼저 처리한다
                else:
                    queue.append(v)  # 거리가 1 늘어나므로 뒤쪽으로 보낸다
    return dist


def grid_min_walls(grid: list[str]) -> int:
    """왼쪽 위 → 오른쪽 아래로 상하좌우 이동할 때 부숴야 하는 벽('1')의 최소 개수.

    칸에 들어갈 때의 비용이 그 칸이 벽이면 1, 빈 방이면 0. 같은 틀을 그리드에서 간선 목록 없이 바로 쓴다."""
    rows, cols = len(grid), len(grid[0])
    dist = [[INF] * cols for _ in range(rows)]
    dist[0][0] = 0
    queue = deque([(0, 0)])
    while queue:
        r, c = queue.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                w = 1 if grid[nr][nc] == "1" else 0
                if dist[r][c] + w < dist[nr][nc]:
                    dist[nr][nc] = dist[r][c] + w
                    if w == 0:
                        queue.appendleft((nr, nc))
                    else:
                        queue.append((nr, nc))
    return dist[rows - 1][cols - 1]


def main() -> None:
    input = sys.stdin.readline
    m, n = map(int, input().split())
    grid = [input().strip() for _ in range(n)]
    print(grid_min_walls(grid))


if __name__ == "__main__":
    main()
