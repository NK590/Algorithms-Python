"""격자 탐색 — 격자의 칸을 정점, 상하좌우 이웃을 간선으로 보고 DFS/BFS 하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 격자는 2차원 리스트이고 1 은 지나갈 수 있는 칸, 0 은 벽입니다. 이웃은 상하좌우 4칸입니다.
- 직접 실행하면 `N M` 과 N 줄의 0/1 문자열을 받아, (0, 0) 에서 (N-1, M-1) 까지의 최단 경로가 지나는 칸의 수를 출력합니다.
  (칸의 수 = 이동 횟수 + 1, 갈 수 없으면 -1)
"""
import sys
from collections import deque

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def _neighbors(r: int, c: int, rows: int, cols: int):
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc


def flood_fill(grid: list, r: int, c: int, new_value) -> int:
    """(r, c) 와 같은 값으로 이어진 칸들을 모두 new_value 로 칠하고, 칠한 칸 수를 반환한다. grid 를 직접 바꾼다."""
    old_value = grid[r][c]
    if old_value == new_value:
        return 0
    rows, cols = len(grid), len(grid[0])
    grid[r][c] = new_value  # 칠하는 것이 곧 방문 표시다
    stack = [(r, c)]
    painted = 1
    while stack:
        cr, cc = stack.pop()
        for nr, nc in _neighbors(cr, cc, rows, cols):
            if grid[nr][nc] == old_value:
                grid[nr][nc] = new_value
                painted += 1
                stack.append((nr, nc))
    return painted


def region_sizes(grid: list) -> list:
    """1 로 이어진 덩어리(상하좌우)들의 크기를 오름차순으로 반환한다. grid 는 바꾸지 않는다."""
    if not grid:
        return []
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    sizes = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 1 or visited[r][c]:
                continue
            visited[r][c] = True
            stack = [(r, c)]
            size = 0
            while stack:
                cr, cc = stack.pop()
                size += 1
                for nr, nc in _neighbors(cr, cc, rows, cols):
                    if grid[nr][nc] == 1 and not visited[nr][nc]:
                        visited[nr][nc] = True
                        stack.append((nr, nc))
            sizes.append(size)
    return sorted(sizes)


def count_regions(grid: list) -> int:
    return len(region_sizes(grid))


def distances_from(grid: list, start: tuple) -> list:
    """start 에서 각 칸까지의 최소 이동 횟수 (BFS). 벽이거나 갈 수 없는 칸은 -1."""
    rows, cols = len(grid), len(grid[0])
    dist = [[-1] * cols for _ in range(rows)]
    sr, sc = start
    if grid[sr][sc] != 1:
        return dist
    dist[sr][sc] = 0
    queue = deque([start])
    while queue:
        r, c = queue.popleft()
        for nr, nc in _neighbors(r, c, rows, cols):
            if grid[nr][nc] == 1 and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))
    return dist


def shortest_path_length(grid: list, start: tuple, goal: tuple) -> int:
    """start 에서 goal 까지의 최소 이동 횟수. 갈 수 없으면 -1."""
    return distances_from(grid, start)[goal[0]][goal[1]]


def main() -> None:
    input = sys.stdin.readline
    n, m = map(int, input().split())
    grid = [list(map(int, input().strip())) for _ in range(n)]
    moves = shortest_path_length(grid, (0, 0), (n - 1, m - 1))
    print(moves + 1 if moves != -1 else -1)


if __name__ == "__main__":
    main()
