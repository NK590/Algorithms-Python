# 연습문제 — DP 연습

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Maximum Subarray Sum](https://cses.fi/problemset/task/1643) | 핵심 연습 | 현재 위치에서 끝나는 최대 구간 합을 유지한다 |
| 2 | [AtCoder — Grid 1](https://atcoder.jp/contests/dp/tasks/dp_h) | 핵심 연습 | 격자 상태와 장애물 기저 조건을 설계한다 |
| 3 | [AtCoder — Knapsack 1](https://atcoder.jp/contests/dp/tasks/dp_d) | 핵심 연습 | 선택·미선택으로 배낭 DP에 연결한다 |
| 4 | [LeetCode 53 Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) | 연속합 | 카데인. 모두 음수일 때 처리. `max_subarray_sum` |
| 5 | [LeetCode 198 House Robber](https://leetcode.com/problems/house-robber/) | 이웃 금지 | `dp[i] = max(dp[i−1], dp[i−2] + a[i])`. `rob_houses` |
| 6 | [LeetCode 64 Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/) | 격자 | 첫 행·열 경계. `min_path_sum` |
| 7 | [LeetCode 63 Unique Paths II](https://leetcode.com/problems/unique-paths-ii/) | 격자 경로 수 | 장애물이면 0. 시작·끝 칸 처리. `count_paths` |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
