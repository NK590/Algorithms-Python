# 연습문제 — DP 연습

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [LeetCode 53 Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) | 연속합 | 카데인. 모두 음수일 때 처리. `max_subarray_sum` |
| 2 | [백준 1912 연속합](https://www.acmicpc.net/problem/1912) | 연속합 | 같은 문제. [solution.py](solution.py)의 `main()`이 같은 형태를 처리한다 |
| 3 | [LeetCode 198 House Robber](https://leetcode.com/problems/house-robber/) | 이웃 금지 | `dp[i] = max(dp[i−1], dp[i−2] + a[i])`. `rob_houses` |
| 4 | [LeetCode 64 Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/) | 격자 | 첫 행·열 경계. `min_path_sum` |
| 5 | [백준 1932 정수 삼각형](https://www.acmicpc.net/problem/1932) | 삼각형 | 위에서 내려가는 최대 합. 아래에서 올라오며 계산. `triangle_max_path` |
| 6 | [백준 2579 계단 오르기](https://www.acmicpc.net/problem/2579) | 상태에 이력 | 연속 세 계단 금지, 마지막 계단 필수. `stairs_max_score` |
| 7 | [LeetCode 63 Unique Paths II](https://leetcode.com/problems/unique-paths-ii/) | 격자 경로 수 | 장애물이면 0. 시작·끝 칸 처리. `count_paths` |
| 8 | [백준 11053 가장 긴 증가하는 부분 수열](https://www.acmicpc.net/problem/11053) | LIS | O(n²) `lis_length`. 범위가 크면 [O(n log n)](../../../lv2-intermediate/04-dynamic-programming/lis/) |
| 9 | [백준 14002 가장 긴 증가하는 부분 수열 4](https://www.acmicpc.net/problem/14002) | LIS 복원 | 길이와 함께 수열을 출력. `lis_sequence` |
| 10 | [백준 11048 이동하기](https://www.acmicpc.net/problem/11048) | 격자 | 세 방향(오른쪽·아래·대각선)에서 오는 최대. 경계 처리 |
| 11 | [백준 1149 RGB거리](https://www.acmicpc.net/problem/1149) | 상태에 색 | `dp[i][색]`. 이웃과 다른 색만 이어 붙인다 |
| 12 | [백준 2156 포도주 시식](https://www.acmicpc.net/problem/2156) | 상태에 이력 | 연속 세 잔 금지(계단과 비슷하나 마지막을 꼭 마실 필요는 없다) |
| 13 | [백준 11054 가장 긴 바이토닉 부분 수열](https://www.acmicpc.net/problem/11054) | LIS 응용 | 앞에서 오는 LIS와 뒤에서 오는 LIS를 합친다 |

## 풀이 메모

- 1~7번은 이 폴더의 함수와 거의 같은 형태입니다. 먼저 상태를 한 문장으로 적고 직접 짜 본 뒤 [solution.py](solution.py)와 비교하세요.
- 6번과 12번은 비슷하지만 **마지막 계단을 꼭 밟아야 하는지**가 달라서 최종 답을 구하는 방법이 다릅니다. 이런 경계 조건 차이가 상태 설계를 바꿉니다.
- 8~9번은 `prev` 배열로 경로를 복원하는 연습입니다. 같은 길이의 LIS가 여럿이면 어느 것을 출력해도 되는지 문제를 확인하세요.
- 막히면 작은 입력에서 **모든 경우를 나열**하는 브루트포스를 만들어 점화식과 비교하세요. 이 폴더의 [테스트](test_solution.py)가 모두 그렇게 되어 있습니다.
