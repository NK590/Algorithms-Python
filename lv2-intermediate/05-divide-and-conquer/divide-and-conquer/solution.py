"""분할 정복 — 문제를 같은 모양의 더 작은 문제로 나누고(divide), 각각 풀고(conquer), 결과를 합친다(combine)

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 세 단계의 비용을 따져 보는 것이 핵심입니다. 반으로 나누고 합치는 데 O(n) 이 들면 T(n) = 2T(n/2) + O(n) = O(n log n) 입니다.
- 여섯 가지: 구간 합 최대(합칠 때 가운데를 걸치는 경우), 역전 쌍 세기(병합 정렬), 가장 가까운 두 점, Z 순서 방문 번호, 쿼드 트리 압축, 같은 값으로 이루어진 영역 세기.
- 멱 계산(a^b mod c) 같은 지수 줄이기는 [빠른 거듭제곱](../fast-exponentiation/) 에서 따로 다룹니다.
- 직접 실행하면 `N r c` 를 받아 2^N × 2^N 배열을 Z 모양으로 방문할 때 (r, c) 칸이 몇 번째인지 출력합니다. (0 부터)
"""
import sys


def max_subarray_dc(numbers: list[int]) -> int:
    """연속한 비어 있지 않은 구간 합의 최댓값. 구간은 ① 왼쪽 절반 안 ② 오른쪽 절반 안 ③ 가운데를 걸침 중 하나다.

    ③ 은 가운데에서 왼쪽으로 뻗은 최대 합 + 가운데에서 오른쪽으로 뻗은 최대 합. 합치는 비용 O(n) → 전체 O(n log n)."""

    def solve(lo, hi):  # 반열린 구간 [lo, hi)
        if hi - lo == 1:
            return numbers[lo]
        mid = (lo + hi) // 2
        left_best = solve(lo, mid)
        right_best = solve(mid, hi)
        running, best_left = 0, float("-inf")
        for i in range(mid - 1, lo - 1, -1):
            running += numbers[i]
            best_left = max(best_left, running)
        running, best_right = 0, float("-inf")
        for i in range(mid, hi):
            running += numbers[i]
            best_right = max(best_right, running)
        return max(left_best, right_best, best_left + best_right)

    return solve(0, len(numbers))


def count_inversions_dc(numbers: list[int]) -> int:
    """i < j 이면서 numbers[i] > numbers[j] 인 쌍의 수. 병합 정렬의 합치는 단계에서, 오른쪽 원소가 먼저 나올 때마다 왼쪽에 남은 원소 수를 더한다."""
    a = list(numbers)
    buffer = [0] * len(a)

    def sort(lo, hi):
        if hi - lo <= 1:
            return 0
        mid = (lo + hi) // 2
        count = sort(lo, mid) + sort(mid, hi)
        i, j, k = lo, mid, lo
        while i < mid and j < hi:
            if a[i] <= a[j]:
                buffer[k] = a[i]
                i += 1
            else:
                buffer[k] = a[j]
                count += mid - i  # a[i..mid) 가 모두 a[j] 보다 크다
                j += 1
            k += 1
        while i < mid:
            buffer[k] = a[i]
            i += 1
            k += 1
        while j < hi:
            buffer[k] = a[j]
            j += 1
            k += 1
        a[lo:hi] = buffer[lo:hi]
        return count

    return sort(0, len(a))


def closest_pair_squared(points: list[tuple[int, int]]) -> int:
    """점 n 개(n ≥ 2) 중 가장 가까운 두 점의 거리의 제곱. x 좌표로 정렬해 반으로 나누고, 가운데 선 근처의 띠(strip)만 합치는 단계에서 확인한다.

    띠 안의 점은 y 순으로 보면 각 점에서 뒤로 상수 개(최대 약 7 개)만 비교하면 충분하므로 합치는 비용이 O(n). 전체 O(n log n)."""
    pts = sorted(points)

    def d2(p, q):
        return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2

    def solve(lo, hi):  # pts[lo:hi], 이미 x 순으로 정렬됨
        if hi - lo <= 3:
            return min(d2(pts[i], pts[j]) for i in range(lo, hi) for j in range(i + 1, hi))
        mid = (lo + hi) // 2
        mid_x = pts[mid][0]
        best = min(solve(lo, mid), solve(mid, hi))
        strip = sorted((p for p in pts[lo:hi] if (p[0] - mid_x) ** 2 < best), key=lambda p: p[1])
        for i in range(len(strip)):
            for j in range(i + 1, len(strip)):
                if (strip[j][1] - strip[i][1]) ** 2 >= best:
                    break  # y 로 이미 best 이상 떨어졌으면 그 뒤는 볼 필요가 없다
                best = min(best, d2(strip[i], strip[j]))
        return best

    return solve(0, len(pts))


def z_order_index(n: int, r: int, c: int) -> int:
    """2ⁿ × 2ⁿ 배열을 Z 모양(왼쪽 위 → 오른쪽 위 → 왼쪽 아래 → 오른쪽 아래, 각 칸을 재귀적으로)으로 방문할 때 (r, c) 가 몇 번째인지(0 부터).

    네 사분면 중 어디에 있는지로 앞선 사분면의 칸 수(4^(n-1) 의 배수)를 더하고, 그 사분면 안에서 같은 문제를 푼다."""
    index = 0
    size = 1 << n
    while size > 1:
        half = size // 2
        quadrant = (2 if r >= half else 0) + (1 if c >= half else 0)
        index += quadrant * half * half
        r %= half
        c %= half
        size = half
    return index


def quad_tree(grid: list[str]) -> str:
    """0/1 로 이루어진 2ⁿ × 2ⁿ 영상을 쿼드 트리로 압축한다. 모두 같은 값이면 그 값 하나, 아니면 (왼위 오른위 왼아래 오른아래) 를 괄호로 묶는다."""

    def solve(r, c, size):
        first = grid[r][c]
        if all(grid[i][j] == first for i in range(r, r + size) for j in range(c, c + size)):
            return first
        half = size // 2
        return "(" + solve(r, c, half) + solve(r, c + half, half) + solve(r + half, c, half) + solve(r + half, c + half, half) + ")"

    return solve(0, 0, len(grid)) if grid else ""


def count_uniform_regions(grid: list[list[int]]) -> dict[int, int]:
    """N × N 종이 (N 은 3 의 거듭제곱) 를 모두 같은 값이 될 때까지 9 등분하며 센, 값별 같은 값 영역의 수."""
    counts: dict[int, int] = {}

    def solve(r, c, size):
        first = grid[r][c]
        if all(grid[i][j] == first for i in range(r, r + size) for j in range(c, c + size)):
            counts[first] = counts.get(first, 0) + 1
            return
        third = size // 3
        for dr in range(3):
            for dc in range(3):
                solve(r + dr * third, c + dc * third, third)

    if grid:
        solve(0, 0, len(grid))
    return counts


def main() -> None:
    n, r, c = map(int, sys.stdin.readline().split())
    print(z_order_index(n, r, c))


if __name__ == "__main__":
    main()
