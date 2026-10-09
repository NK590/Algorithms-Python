# 연습문제 — 대표 그리디 유형

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Tasks and Deadlines](https://cses.fi/problemset/task/1630) | 핵심 연습 | 정렬로 대기 시간의 누적 비용을 줄인다 |
| 2 | [CSES — Restaurant Customers](https://cses.fi/problemset/task/1619) | 핵심 연습 | 동시 사용량을 이벤트 순서로 센다 |
| 3 | [CSES — Movie Festival II](https://cses.fi/problemset/task/1632) | 심화·응용 | 심화로 정렬과 종료 시각 자료구조를 결합한다 |
| 4 | [LeetCode 55 Jump Game](https://leetcode.com/problems/jump-game/) | ③ 도달 범위 | `farthest` 하나로 끝난다 (`can_reach_end`) |
| 5 | [LeetCode 45 Jump Game II](https://leetcode.com/problems/jump-game-ii/) | ③ 응용 | 최소 점프 수. 현재 점프로 갈 수 있는 끝을 기억하며 BFS 단계처럼 센다 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
