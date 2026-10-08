# 연습문제 — 비트마스크 DP

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 1311 할 일 정하기 1](https://www.acmicpc.net/problem/1311) | 할당 문제 | 사람 i가 일 j를 하는 비용. `dp[mask]`. `assignment_min_cost` |
| 2 | [백준 2098 외판원 순회](https://www.acmicpc.net/problem/2098) | TSP | 0은 길이 없음. N ≤ 16. [solution.py](solution.py)의 `main()`이 같은 형태를 처리한다 |
| 3 | [백준 10971 외판원 순회 2](https://www.acmicpc.net/problem/10971) | TSP (작은 N) | N ≤ 10. 같은 문제를 순열 완전 탐색과 DP로 모두 풀어 비교 |
| 4 | [LeetCode 847 Shortest Path Visiting All Nodes](https://leetcode.com/problems/shortest-path-visiting-all-nodes/) | 방문 집합 + BFS | 상태 `(방문한 집합, 현재 위치)`로 BFS. 간선 가중치가 모두 1 |
| 5 | [백준 1562 계단 수](https://www.acmicpc.net/problem/1562) | 방문한 숫자 집합 | 0~9를 모두 한 번 이상 사용한 N자리 계단 수. `dp[길이][마지막 숫자][사용한 숫자 마스크]` |
| 6 | [백준 1086 박성원](https://www.acmicpc.net/problem/1086) | 순열 + 나머지 | 수를 이어 붙인 결과가 K의 배수가 되는 순서의 수. `dp[mask][나머지]` |
| 7 | [백준 1102 발전소](https://www.acmicpc.net/problem/1102) | 부분집합 DP | 켜진 발전소 집합을 상태로 하는 최소 비용 |

## 풀이 메모

- 3번은 N ≤ 10이라 순열로도 풀리므로, 먼저 이 폴더의 [테스트](test_solution.py) `brute_force_tsp`처럼 순열로 풀고 같은 답이 나오는지 비교하세요.
- 2번에서 입력의 `0`은 "길이 없음"이지만 대각선도 0입니다. `i == j`는 항상 건너뛰므로 `INF`로 바꾸든 두든 영향이 없습니다.
- 5번과 6번은 비트마스크에 다른 상태(마지막 숫자, 나머지)를 곱해서 쓰는 문제입니다. 상태 수가 `2ⁿ × 다른 차원`임을 확인하고 메모리를 계산해 보세요.
- n이 16을 넘거나 시간이 빠듯하면 PyPy3가 필요합니다.
