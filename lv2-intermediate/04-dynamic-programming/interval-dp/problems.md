# 연습문제 — 구간 DP

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [AtCoder — Slimes](https://atcoder.jp/contests/dp/tasks/dp_n) | 핵심 연습 | 마지막 합치는 경계를 열거한다 |
| 2 | [CSES — Removal Game](https://cses.fi/problemset/task/1097) | 핵심 연습 | 양 끝 선택을 점수 차이 상태로 표현한다 |
| 3 | [CSES — Rectangle Cutting](https://cses.fi/problemset/task/1744) | 핵심 연습 | 직사각형을 자르는 마지막 분할을 열거한다 |
| 4 | [LeetCode 516 Longest Palindromic Subsequence](https://leetcode.com/problems/longest-palindromic-subsequence/) | 양 끝 | `longest_palindromic_subsequence` |
| 5 | [LeetCode 312 Burst Balloons](https://leetcode.com/problems/burst-balloons/) | 마지막을 기준 | "마지막에 터뜨릴 풍선"으로 뒤집기. `burst_balloons` |
| 6 | [LeetCode 1130 Minimum Cost Tree From Leaf Values](https://leetcode.com/problems/minimum-cost-tree-from-leaf-values/) | 구간 분할 | 구간을 둘로 나누고 각 구간의 최댓값의 곱을 더한다 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
