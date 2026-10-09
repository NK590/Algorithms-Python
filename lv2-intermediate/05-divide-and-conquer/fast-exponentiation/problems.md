# 연습문제 — 빠른 거듭제곱

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Exponentiation](https://cses.fi/problemset/task/1095) | 핵심 연습 | 지수의 비트마다 제곱과 곱을 수행한다 |
| 2 | [CSES — Exponentiation II](https://cses.fi/problemset/task/1712) | 핵심 연습 | 지수의 모듈러를 다룰 때 밑의 가역 조건을 확인한다 |
| 3 | [CSES — Fibonacci Numbers](https://cses.fi/problemset/task/1722) | 심화·응용 | 심화로 수 대신 행렬을 거듭제곱한다 |
| 4 | [LeetCode 50 Pow(x, n)](https://leetcode.com/problems/powx-n/) | 실수, 음수 지수 | `x^n`, n이 음수일 수 있다. `power_float` |
| 5 | [LeetCode 372 Super Pow](https://leetcode.com/problems/super-pow/) | 큰 지수 | 지수가 배열로 주어진 매우 큰 수. `a^(10k + d) = (a^k)^10 · a^d` |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
