"""2차원 누적 합 — 격자의 부분 직사각형 합을 O(1) 에 구하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- prefix[r][c] 는 grid[0..r-1][0..c-1] 직사각형의 합입니다. (위쪽 한 줄과 왼쪽 한 줄을 0 으로 둔 (R+1) × (C+1) 배열)
- 직접 실행하면 `N M`, N 줄의 M 개 수, `K`, K 개의 질문 `i j x y` (1부터, 양 끝 포함)를 받아 (i,j)~(x,y) 직사각형의 합을 출력합니다.
"""
import sys


def build_prefix_2d(grid: list) -> list:
    """prefix[r][c] = grid[0..r-1][0..c-1] 의 합. 포함-배제: 위 + 왼쪽 − 겹치는 왼쪽 위 + 자기 칸. O(R × C)"""
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
    for r in range(rows):
        for c in range(cols):
            prefix[r + 1][c + 1] = prefix[r][c + 1] + prefix[r + 1][c] - prefix[r][c] + grid[r][c]
    return prefix


def rect_sum(prefix: list, r1: int, c1: int, r2: int, c2: int):
    """grid[r1..r2][c1..c2] (양 끝 포함, 0부터)의 합. 큰 직사각형에서 위쪽과 왼쪽을 빼고, 두 번 빠진 모서리를 한 번 되돌린다. O(1)"""
    return prefix[r2 + 1][c2 + 1] - prefix[r1][c2 + 1] - prefix[r2 + 1][c1] + prefix[r1][c1]


def best_square_sum(grid: list, k: int):
    """k × k 부분 정사각형 중 합이 가장 큰 것의 합. 모든 위치를 O(1) 씩 확인한다."""
    prefix = build_prefix_2d(grid)
    rows, cols = len(grid), len(grid[0])
    best = None
    for r in range(rows - k + 1):
        for c in range(cols - k + 1):
            total = rect_sum(prefix, r, c, r + k - 1, c + k - 1)
            if best is None or total > best:
                best = total
    return best


def main() -> None:
    input = sys.stdin.readline
    n, m = map(int, input().split())
    prefix = build_prefix_2d([list(map(int, input().split())) for _ in range(n)])
    k = int(input())
    out = []
    for _ in range(k):
        i, j, x, y = map(int, input().split())
        out.append(rect_sum(prefix, i - 1, j - 1, x - 1, y - 1))
    print("\n".join(map(str, out)))


if __name__ == "__main__":
    main()
