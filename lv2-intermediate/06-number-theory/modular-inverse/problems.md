# 연습문제 — 모듈러 역원

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Binomial Coefficients](https://cses.fi/problemset/task/1079) | 핵심 연습 | 팩토리얼로 나눈 값을 역원의 곱으로 계산한다 |
| 2 | [AtCoder — Throne](https://atcoder.jp/contests/abc186/tasks/abc186_e) | 핵심 연습 | 서로소가 아닐 때 gcd로 합동식을 먼저 축약한다 |
| 3 | [CSES — Distributing Apples](https://cses.fi/problemset/task/1716) | 핵심 연습 | 분배 경우의 수를 이항계수로 변환한다 |
| 4 | [LeetCode 1916 Count Ways to Build Rooms in an Ant Colony](https://leetcode.com/problems/count-ways-to-build-rooms-in-an-ant-colony/) | 트리 + 역원 | 각 서브트리의 크기 곱으로 `n!`을 나누는 공식. 나눗셈 자리마다 역원을 곱하고, 크기 `1..n`의 역원을 한 번에 구하면 `inverse_table`이 쓰인다 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
