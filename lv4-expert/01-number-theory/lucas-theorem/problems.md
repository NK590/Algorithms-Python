# 연습문제 — 뤼카 정리

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [Library Checker — Binomial Coefficient (Prime Mod)](https://judge.yosupo.jp/problem/binomial_coefficient_prime_mod) | 핵심 연습 | n과 r을 소수 진법의 자릿수로 나눠 조합을 곱한다 |
| 2 | [LeetCode 62 Unique Paths](https://leetcode.com/problems/unique-paths/) | `C(m + n − 2, m − 1)` | 정확한 값. `math.comb`와 `binomial_mod`가 같은 나머지를 내는지 비교 |
| 3 | [Project Euler 148 - Exploring Pascal's triangle](https://projecteuler.net/problem=148) | 파스칼 삼각형 처음 10⁹줄에서 7로 나누어떨어지지 않는 항의 수 | `n`번째 줄의 개수 `Π (nᵢ + 1)`(7진법), 줄 합을 자릿수 DP처럼 |
| 4 | [Library Checker - Binomial Coefficient](https://judge.yosupo.jp/problem/binomial_coefficient) | 임의의 `m ≤ 10⁷` | 소인수 `p^e`마다 곱 표 + CRT. `binomial_mod`가 그대로 대응 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
