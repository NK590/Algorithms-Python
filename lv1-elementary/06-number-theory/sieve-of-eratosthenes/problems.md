# 연습문제 — 에라토스테네스의 체

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Counting Divisors](https://cses.fi/problemset/task/1713) | 핵심 연습 | 소인수 전처리로 여러 수의 약수 개수를 계산한다 |
| 2 | [CSES — Common Divisors](https://cses.fi/problemset/task/1081) | 핵심 연습 | 배수 순회로 많은 수의 공약수를 찾는다 |
| 3 | [CSES — Divisor Analysis](https://cses.fi/problemset/task/2182) | 핵심 연습 | 소인수 정보에서 약수 관련 공식을 적용한다 |
| 4 | [LeetCode 204 Count Primes](https://leetcode.com/problems/count-primes/) | 개수 | `count_primes`. n 미만이라는 경계에 주의 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
