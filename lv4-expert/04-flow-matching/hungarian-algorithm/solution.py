"""헝가리안 알고리즘(Hungarian Algorithm, Kuhn–Munkres) — n × m 비용 행렬에서 행마다 서로 다른 열을 하나씩 골라 비용의 합을 최소로 (할당 문제), O(n²m)

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 쌍대 변수(퍼텐셜) u[i] (행), v[j] (열) 를 유지한다. 모든 (i, j) 에서 u[i] + v[j] ≤ cost[i][j] 이고 배정된 칸에서는 등호이면 그 배정이 최적이다 (선형 계획법의 쌍대성: 합 u + v = 최소 비용).
- 행을 하나씩 추가한다. 새 행 i 를 시작점으로 "교대 경로" 를 다익스트라처럼 넓혀 가며, 아직 못 가 본 열 j 의 최소 여유(slack) minv[j] = min over 방문한 행 (cost - u - v) 를 관리한다.
  가장 작은 여유 delta 만큼 방문한 행의 u 를 올리고 방문한 열의 v 를 내려서 새 등호 간선을 만들고, 짝이 없는 열에 닿으면 교대 경로를 따라 배정을 뒤집는다. 행 하나에 O(nm), 전체 O(n²m).
- hungarian(cost, maximize=False): n ≤ m 이면 모든 행이 배정되고, n > m 이면 (행과 열을 바꿔 풀어서) 일부 행은 배정되지 않아 -1. cost 의 None 은 "배정 불가" 로 취급 (모든 행을 배정할 수 없으면 ValueError).
- hungarian_duals(cost): (최소 합, 배정, u, v) — 쌍대 해를 증명서로 쓸 수 있다.
- bottleneck_assignment(cost): 합이 아니라 "배정된 칸 중 최댓값" 을 최소화 (비용 값에 대한 이분 탐색 + 이분 매칭).
- 직접 실행하면 Library Checker "Assignment Problem" 형식 — `N`, 이어서 N 줄의 N 개 정수 — 를 받아 최소 비용과 행마다 배정된 열(0 부터)을 출력합니다.
"""
import sys
from typing import Optional, Sequence

INF = float("inf")


def _solve(cost: Sequence[Sequence[float]]) -> tuple[list[int], list[float], list[float]]:
    """n ≤ m 인 행렬. (행마다 배정된 열, u, v) 를 돌려준다 (u, v 는 1부터)."""
    n, m = len(cost), len(cost[0])
    u = [0.0] * (n + 1)
    v = [0.0] * (m + 1)
    row_of = [0] * (m + 1)  # row_of[j] = 열 j 에 배정된 행 (1부터, 0 이면 없음)
    way = [0] * (m + 1)  # way[j] = 최소 여유로 열 j 에 닿은 직전 열 (교대 경로 복원용)
    for i in range(1, n + 1):
        row_of[0] = i
        j0 = 0
        slack = [INF] * (m + 1)
        used = [False] * (m + 1)
        while True:
            used[j0] = True
            i0 = row_of[j0]
            delta, j1 = INF, 0
            for j in range(1, m + 1):
                if not used[j]:
                    current = cost[i0 - 1][j - 1] - u[i0] - v[j]
                    if current < slack[j]:
                        slack[j], way[j] = current, j0
                    if slack[j] < delta:
                        delta, j1 = slack[j], j
            for j in range(m + 1):
                if used[j]:
                    u[row_of[j]] += delta
                    v[j] -= delta
                else:
                    slack[j] -= delta
            j0 = j1
            if row_of[j0] == 0:
                break
        while j0:  # 교대 경로를 따라 배정을 뒤집는다
            j1 = way[j0]
            row_of[j0] = row_of[j1]
            j0 = j1
    assignment = [-1] * n
    for j in range(1, m + 1):
        if row_of[j]:
            assignment[row_of[j] - 1] = j - 1
    return assignment, u, v


def _prepare(cost: Sequence[Sequence[Optional[float]]], maximize: bool) -> tuple[list[list[float]], float]:
    """None(배정 불가) 을 큰 값으로 바꾸고 최대화는 부호를 뒤집는다. (행렬, 큰 값) 을 돌려준다."""
    finite = [abs(x) for row in cost for x in row if x is not None]
    big = sum(finite) + 1  # 이만큼이면 충분: None 을 쓰는 배정과 쓰지 않는 배정은 서로 다른 칸의 절댓값 합(≤ sum(finite))만큼만 차이 날 수 있어 None 하나가 항상 더 비싸다
    sign = -1 if maximize else 1
    return [[big if x is None else sign * x for x in row] for row in cost], big


def hungarian_duals(cost: Sequence[Sequence[Optional[float]]], maximize: bool = False) -> tuple[float, list[int], list[float], list[float]]:
    """(최소 합, 행마다 배정된 열, u, v). maximize 면 최대 합과 부호가 바뀐 쌍대 해를 돌려준다. n > m 이면 열이 없는 행은 -1."""
    n = len(cost)
    if n == 0:
        return 0, [], [], []
    m = len(cost[0])
    if any(len(row) != m for row in cost):
        raise ValueError("행마다 열의 수가 같아야 합니다")
    if m == 0:
        return 0, [-1] * n, [0.0] * n, []
    matrix, big = _prepare(cost, maximize)
    if n <= m:
        assignment, u, v = _solve(matrix)
        row_duals, column_duals = u[1:], v[1:]
    else:
        transposed = [[matrix[i][j] for i in range(n)] for j in range(m)]
        column_assignment, u, v = _solve(transposed)  # 열마다 서로 다른 행을 배정
        assignment = [-1] * n
        for j, i in enumerate(column_assignment):
            assignment[i] = j
        row_duals, column_duals = v[1:], u[1:]
    for i, j in enumerate(assignment):
        if j >= 0 and cost[i][j] is None:
            raise ValueError("모든 행을 배정할 수 없습니다 (None 칸을 피하는 완전 배정이 없습니다)")
    total = sum(cost[i][j] for i, j in enumerate(assignment) if j >= 0)
    if maximize:
        row_duals = [-x for x in row_duals]
        column_duals = [-x for x in column_duals]
    return total, assignment, row_duals, column_duals


def hungarian(cost: Sequence[Sequence[Optional[float]]], maximize: bool = False) -> tuple[float, list[int]]:
    """(합의 최솟값(maximize 면 최댓값), 행마다 배정된 열)."""
    total, assignment, _, _ = hungarian_duals(cost, maximize)
    return total, assignment


def bottleneck_assignment(cost: Sequence[Sequence[float]]) -> tuple[float, list[int]]:
    """n ≤ m 인 행렬에서 행마다 서로 다른 열을 골라 "고른 값 중 최댓값" 을 최소로. (그 최댓값, 배정) 을 돌려준다."""
    n = len(cost)
    if n == 0:
        return 0, []
    m = len(cost[0])
    if n > m:
        raise ValueError("행 수가 열 수보다 클 수 없습니다")

    def perfect_matching(limit: float) -> Optional[list[int]]:
        match_of_column = [-1] * m

        def try_row(i: int, seen: list[bool]) -> bool:
            for j in range(m):
                if cost[i][j] <= limit and not seen[j]:
                    seen[j] = True
                    if match_of_column[j] == -1 or try_row(match_of_column[j], seen):
                        match_of_column[j] = i
                        return True
            return False

        for i in range(n):
            if not try_row(i, [False] * m):
                return None
        assignment = [-1] * n
        for j, i in enumerate(match_of_column):
            if i >= 0:
                assignment[i] = j
        return assignment

    values = sorted({x for row in cost for x in row})
    low, high = 0, len(values) - 1  # values[high] 이면 항상 완전 매칭이 있다
    while low < high:
        mid = (low + high) // 2
        if perfect_matching(values[mid]) is not None:
            high = mid
        else:
            low = mid + 1
    return values[low], perfect_matching(values[low])  # type: ignore[return-value]


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    cost = [[int(data[1 + i * n + j]) for j in range(n)] for i in range(n)]
    total, assignment = hungarian(cost)
    print(total)
    print(" ".join(map(str, assignment)))


if __name__ == "__main__":
    main()
