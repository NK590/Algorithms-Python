# 연습문제 — 다이나믹 프로그래밍

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Dice Combinations](https://cses.fi/problemset/task/1633) | 핵심 연습 | 마지막 행동으로 경우의 수 점화식을 세운다 |
| 2 | [AtCoder — Frog 1](https://atcoder.jp/contests/dp/tasks/dp_a) | 핵심 연습 | 현재 위치에 도달하는 최소 비용을 정의한다 |
| 3 | [AtCoder — Frog 2](https://atcoder.jp/contests/dp/tasks/dp_b) | 핵심 연습 | 이전 상태를 더 넓게 탐색해 전이를 일반화한다 |
| 4 | [LeetCode 509 Fibonacci Number](https://leetcode.com/problems/fibonacci-number/) | 기본형 | 세 가지 구현(재귀·메모이제이션·표)을 모두 써 본다 |
| 5 | [LeetCode 70 Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) | 점화식 | 마지막 걸음이 1칸/2칸. `climb_stairs` |
| 6 | [LeetCode 746 Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs/) | 최솟값 | `dp[i] = cost[i] + min(dp[i−1], dp[i−2])` |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
