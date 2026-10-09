# 연습문제 — 그리디

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Movie Festival](https://cses.fi/problemset/task/1629) | 핵심 연습 | 끝나는 시간이 가장 빠른 구간을 골라 교환 논증을 연습한다 |
| 2 | [CSES — Ferris Wheel](https://cses.fi/problemset/task/1090) | 핵심 연습 | 가장 무거운 사람과 가장 가벼운 사람을 짝짓는다 |
| 3 | [CSES — Tasks and Deadlines](https://cses.fi/problemset/task/1630) | 핵심 연습 | 작업 순서를 서로 바꾸어 비용 차이를 계산한다 |
| 4 | [LeetCode 455 Assign Cookies](https://leetcode.com/problems/assign-cookies/) | 정렬 + 짝짓기 | 둘 다 정렬하고 작은 것끼리 맞춘다 |
| 5 | [LeetCode 435 Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) | 활동 선택 | 지워야 하는 최소 개수 = 전체 − 고를 수 있는 최대 개수 |
| 6 | [LeetCode 122 Best Time to Buy and Sell Stock II](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/) | 증가분 | 오르는 구간의 차이를 모두 더한다 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
