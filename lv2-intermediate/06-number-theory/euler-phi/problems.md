# 연습문제 — 오일러 피 함수

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Divisor Analysis](https://cses.fi/problemset/task/2182) | 핵심 연습 | 모듈러 지수 계산에서 소수와 지수 축소 조건을 구분한다 |
| 2 | [LeetCode 372 Super Pow](https://leetcode.com/problems/super-pow/) | 확장 오일러 정리 | `a^b mod 1337`, `b`가 아주 긴 수. `1337 = 7 · 191`이라 `φ(1337) = 1140`. 지수를 `φ`로 줄이되 서로소가 아닌 경우를 조심 |
| 3 | [Project Euler 72 Counting fractions](https://projecteuler.net/problem=72) | `Σ φ` | `d ≤ 10⁶`인 기약 진분수의 개수 = `Σ_{q=2..d} φ(q)`. `phi_table`로 풀린다. `count_proper_reduced_fractions`가 같은 계산 |
| 4 | [Project Euler 69 Totient maximum](https://projecteuler.net/problem=69) | 공식 변형 | `n / φ(n) = Π p/(p − 1)`이 소인수의 종류에만 의존한다는 관찰로, 작은 소수를 모두 곱한 수가 답 |
| 5 | [Project Euler 70 Totient permutation](https://projecteuler.net/problem=70) | `φ`의 자릿수 조건 | `n / φ(n)`을 최소화하는 `n`을 찾을 때 `φ(n)`이 `n`의 자릿수 재배열이 되어야 함. 소인수가 두 개일 때가 후보 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
