# 연습문제 — 그리디

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 4796 캠핑](https://www.acmicpc.net/problem/4796) | 기본형 | 주기마다 L일을 다 쓰고, 남은 날은 L일까지만. `max_camping_days`가 핵심 계산이다. [solution.py](solution.py)의 `main()`은 한 줄만 처리하므로, 실제 문제의 여러 줄 입력과 출력 형식에 맞게 직접 바꿔 보자 |
| 2 | [백준 5585 거스름돈](https://www.acmicpc.net/problem/5585) | 동전 | 큰 단위부터. 단위가 배수 관계라 그리디가 맞다 |
| 3 | [백준 11047 동전 0](https://www.acmicpc.net/problem/11047) | 동전 | 동전이 오름차순으로 주어지고 서로 배수다. `greedy_coin_change` |
| 4 | [LeetCode 455 Assign Cookies](https://leetcode.com/problems/assign-cookies/) | 정렬 + 짝짓기 | 둘 다 정렬하고 작은 것끼리 맞춘다 |
| 5 | [백준 1931 회의실 배정](https://www.acmicpc.net/problem/1931) | 활동 선택 | **끝나는 시간 → 시작 시간** 순 정렬. 시작과 끝이 같은 회의를 주의. `activity_selection` |
| 6 | [LeetCode 435 Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) | 활동 선택 | 지워야 하는 최소 개수 = 전체 − 고를 수 있는 최대 개수 |
| 7 | [백준 2217 로프](https://www.acmicpc.net/problem/2217) | 정렬 | 가장 약한 로프가 버티는 무게 × 개수를 모든 경우에 최대화한다 |
| 8 | [백준 1541 잃어버린 괄호](https://www.acmicpc.net/problem/1541) | 식 | 첫 `-` 뒤를 괄호로 묶어 모두 뺀다 |
| 9 | [백준 13305 주유소](https://www.acmicpc.net/problem/13305) | 최솟값 유지 | 지금까지 만난 가장 싼 기름값으로 다음 도로를 간다 |
| 10 | [LeetCode 122 Best Time to Buy and Sell Stock II](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/) | 증가분 | 오르는 구간의 차이를 모두 더한다 |
| 11 | [백준 1744 수 묶기](https://www.acmicpc.net/problem/1744) | 경우 나누기 | 양수·음수·0·1의 처리가 다르다. 큰 수끼리, 작은 음수끼리 묶는다 |

## 풀이 메모

- 5번이 가장 중요합니다. 정렬 기준을 `(끝, 시작)`으로 바꾸고, 반례(`[(0,10), (1,2), (3,4)]`)를 손으로 만들어 "시작이 빠른 순", "짧은 순"이 틀린다는 것을 확인하세요.
- 10~11번은 **경우를 나누어** 규칙을 세우는 연습입니다. 한 규칙으로 안 풀리면 입력을 부호나 크기로 쪼개 보세요.
- 풀기 전에 **작은 입력에서 모든 경우를 도는 브루트포스**를 짜 두면 규칙이 맞는지 바로 비교할 수 있습니다.
