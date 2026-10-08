"""2차원 배열 — 격자(행렬) 모양의 데이터를 리스트의 리스트로 다루기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 격자의 칸은 grid[행][열] 로 읽습니다. 행(row)은 위에서 아래로, 열(col)은 왼쪽에서 오른쪽으로 늘어납니다.
- 직접 실행하면 첫 줄에 N, 다음 N줄에 N개씩의 정수를 받아 전치(행과 열을 맞바꾼) 행렬을 출력합니다.
"""
import sys

# 상, 우, 하, 좌 (시계 방향). 한 칸 이동할 때 (행, 열)이 바뀌는 양
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def make_grid(rows: int, cols: int, fill=0) -> list:
    """rows × cols 격자를 만든다. 행마다 새 리스트를 만들어야 한다."""
    return [[fill] * cols for _ in range(rows)]


def make_grid_wrong(rows: int, cols: int, fill=0) -> list:
    """흔한 실수: 같은 행 리스트를 rows 번 가리키게 해서, 한 칸을 바꾸면 같은 열이 전부 바뀐다."""
    return [[fill] * cols] * rows


def transpose(grid: list) -> list:
    """행과 열을 맞바꾼다. (i, j) 칸이 (j, i) 로 간다."""
    if not grid:
        return []
    return [[grid[r][c] for r in range(len(grid))] for c in range(len(grid[0]))]


def rotate_clockwise(grid: list) -> list:
    """시계 방향으로 90도 돌린다. 새 격자의 (c, rows-1-r) 칸이 원래 (r, c) 칸이다."""
    if not grid:
        return []
    rows, cols = len(grid), len(grid[0])
    rotated = make_grid(cols, rows)
    for r in range(rows):
        for c in range(cols):
            rotated[c][rows - 1 - r] = grid[r][c]
    return rotated


def neighbors(r: int, c: int, rows: int, cols: int) -> list:
    """(r, c) 의 상하좌우 칸 중 격자 안에 있는 칸들을 반환한다."""
    result = []
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:  # 범위 검사를 빼먹으면 -1 인덱스가 반대편 칸을 읽는다
            result.append((nr, nc))
    return result


def spiral_grid(rows: int, cols: int) -> list:
    """왼쪽 위에서 시작해 시계 방향 나선으로 1, 2, 3, ... 을 채운 격자를 만든다."""
    grid = make_grid(rows, cols)  # 0 은 아직 안 채운 칸
    r = c = 0
    d = 1  # DIRECTIONS 의 인덱스. 1 은 오른쪽이라 오른쪽으로 먼저 간다
    for number in range(1, rows * cols + 1):
        grid[r][c] = number
        if number == rows * cols:
            break
        nr, nc = r + DIRECTIONS[d][0], c + DIRECTIONS[d][1]
        # 앞 칸이 격자 밖이거나 이미 채운 칸이면 방향을 시계 방향으로 돌린다.
        if not (0 <= nr < rows and 0 <= nc < cols) or grid[nr][nc] != 0:
            d = (d + 1) % 4
            nr, nc = r + DIRECTIONS[d][0], c + DIRECTIONS[d][1]
        r, c = nr, nc
    return grid


def row_and_column_sums(grid: list) -> tuple:
    """(행별 합 리스트, 열별 합 리스트)"""
    row_sums = [sum(row) for row in grid]
    col_sums = [sum(grid[r][c] for r in range(len(grid))) for c in range(len(grid[0]))] if grid else []
    return row_sums, col_sums


def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    grid = [list(map(int, input().split())) for _ in range(n)]
    print("\n".join(" ".join(map(str, row)) for row in transpose(grid)))


if __name__ == "__main__":
    main()
