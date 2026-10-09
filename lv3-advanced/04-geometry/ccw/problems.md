# 연습문제 — CCW와 외적

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Point Location Test](https://cses.fi/problemset/task/2189) | 핵심 연습 | 외적의 부호로 점이 선분의 어느 쪽인지 판단한다 |
| 2 | [AOJ — Counter-Clockwise](https://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_1_C) | 핵심 연습 | 공선점까지 포함한 위치 관계를 분류한다 |
| 3 | [CSES — Polygon Area](https://cses.fi/problemset/task/2191) | 핵심 연습 | 외적을 누적해 다각형 넓이를 구한다 |
| 4 | [LeetCode 1232 Check If It Is a Straight Line](https://leetcode.com/problems/check-if-it-is-a-straight-line/) | 일직선 판정 | 첫 두 점과 나머지 점의 `cross`가 모두 0인가 |
| 5 | [LeetCode 812 Largest Triangle Area](https://leetcode.com/problems/largest-triangle-area/) | 삼각형 넓이 | 모든 세 점의 `triangle_area2`의 최댓값. 20개 이하라 완전탐색 |
| 6 | [LeetCode 149 Max Points on a Line](https://leetcode.com/problems/max-points-on-a-line/) | 일직선 위의 점 수 | 한 점을 고정하고 다른 점과의 기울기를 기약분수로 센다. 외적으로 직접 판정하는 `O(n³)`과 비교 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
