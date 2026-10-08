"""비트마스크 DP — "지금까지 방문한 집합" 을 정수 하나(비트마스크)로 표현해 상태로 쓰는 DP

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 상태: dp[mask][last] = 집합 mask 의 원소들을 모두 한 번씩 거치고 마지막에 last 에 있을 때의 최솟값(또는 경우의 수).
  원소가 n 개면 상태가 2ⁿ·n 개라서 n 이 약 20 이하일 때 쓸 수 있습니다.
- 세 가지: 외판원 순회(TSP, Held-Karp), 일 배정(할당 문제), 해밀턴 경로의 수.
- 직접 실행하면 `N` 과 N×N 비용 행렬(0 은 길이 없음)을 받아 모든 도시를 한 번씩 거쳐 출발 도시로 돌아오는 최소 비용을 출력합니다.
"""
import sys

INF = float("inf")


def tsp(dist: list[list[float]]) -> float:
    """외판원 순회: 0 번 도시에서 출발해 모든 도시를 한 번씩 거치고 0 번으로 돌아오는 최소 비용. dist[i][j] = INF 면 길이 없음.

    dp[mask][j] = 0 에서 출발해 mask 의 도시들을 방문하고 j 에서 끝나는 최소 비용 (mask 는 0 과 j 를 포함).
    dp[mask | (1<<k)][k] = min(dp[mask][j] + dist[j][k]) (k 는 mask 에 없음). 가능한 길이 없으면 INF."""
    n = len(dist)
    if n <= 1:
        return 0
    full = (1 << n) - 1
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0
    for mask in range(1, 1 << n, 2):  # 0 번 도시가 포함된(홀수) 마스크만 의미 있다
        row = dp[mask]
        for j in range(n):
            cost = row[j]
            if cost == INF:
                continue
            dj = dist[j]
            for k in range(1, n):
                if mask >> k & 1:
                    continue
                new = cost + dj[k]
                nxt = dp[mask | (1 << k)]
                if new < nxt[k]:
                    nxt[k] = new
    return min((dp[full][j] + dist[j][0] for j in range(1, n)), default=INF)


def tsp_with_path(dist: list[list[float]]) -> tuple[float, list[int]]:
    """(최소 비용, 도시 방문 순서 [0, …, 0]). 길이 없으면 (INF, []). 각 상태에서 어디서 왔는지를 따로 기록해 거꾸로 따라간다."""
    n = len(dist)
    if n == 0:
        return 0, []
    if n == 1:
        return 0, [0, 0]
    full = (1 << n) - 1
    dp = [[INF] * n for _ in range(1 << n)]
    came = [[-1] * n for _ in range(1 << n)]
    dp[1][0] = 0
    for mask in range(1, 1 << n, 2):
        for j in range(n):
            cost = dp[mask][j]
            if cost == INF:
                continue
            for k in range(1, n):
                if mask >> k & 1:
                    continue
                new = cost + dist[j][k]
                if new < dp[mask | (1 << k)][k]:
                    dp[mask | (1 << k)][k] = new
                    came[mask | (1 << k)][k] = j
    best, last = INF, -1
    for j in range(1, n):
        total = dp[full][j] + dist[j][0]
        if total < best:
            best, last = total, j
    if last == -1:
        return INF, []
    route = []  # 마지막 도시에서 출발점까지 거꾸로 모은다
    mask, j = full, last
    while j != -1:  # came[1][0] = -1 에서 멈춘다
        route.append(j)
        mask, j = mask ^ (1 << j), came[mask][j]
    return best, route[::-1] + [0]


def assignment_min_cost(cost: list[list[int]]) -> int:
    """n 명에게 n 개의 일을 하나씩 배정하는 최소 비용 (할당 문제). cost[i][j] = i 번 사람이 j 번 일을 할 때의 비용.

    dp[mask] = 앞의 popcount(mask) 명이 mask 에 해당하는 일들을 맡았을 때의 최소 비용. 다음 사람이 아직 안 맡은 일 하나를 맡는다. 상태 2ⁿ 개, 전이 n 개."""
    n = len(cost)
    if n == 0:
        return 0
    dp = [INF] * (1 << n)
    dp[0] = 0
    for mask in range(1 << n):
        if dp[mask] == INF:
            continue
        person = bin(mask).count("1")
        if person == n:
            continue
        for job in range(n):
            if not mask >> job & 1:
                new = dp[mask] + cost[person][job]
                if new < dp[mask | (1 << job)]:
                    dp[mask | (1 << job)] = new
    return dp[(1 << n) - 1]


def count_hamiltonian_paths(adj: list[list[int]]) -> int:
    """방향 그래프(adj[i][j] = 1 이면 i → j 간선)에서 모든 정점을 한 번씩 지나는 경로(시작·끝 자유)의 수.

    dp[mask][j] = mask 의 정점들을 한 번씩 지나며 j 에서 끝나는 경로의 수."""
    n = len(adj)
    if n == 0:
        return 0
    dp = [[0] * n for _ in range(1 << n)]
    for v in range(n):
        dp[1 << v][v] = 1
    for mask in range(1, 1 << n):
        for j in range(n):
            ways = dp[mask][j]
            if not ways:
                continue
            for k in range(n):
                if not mask >> k & 1 and adj[j][k]:
                    dp[mask | (1 << k)][k] += ways
    return sum(dp[(1 << n) - 1])


def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    matrix = [list(map(int, input().split())) for _ in range(n)]
    dist = [[matrix[i][j] if matrix[i][j] != 0 else INF for j in range(n)] for i in range(n)]
    result = tsp(dist)
    print(int(result))


if __name__ == "__main__":
    main()
