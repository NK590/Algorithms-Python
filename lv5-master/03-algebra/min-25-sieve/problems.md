# 연습문제 — 민-25 체

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [Library Checker — Counting Primes](https://judge.yosupo.jp/problem/counting_primes) | 핵심 연습 | 몫이 같은 상태들을 묶어 큰 n의 소수 개수를 센다 |
| 2 | [Library Checker — Sum of Multiplicative Function](https://judge.yosupo.jp/problem/sum_of_multiplicative_function_large) | 핵심 연습 | 소수 거듭제곱 전이로 곱셈적 함수의 누적합을 구한다 |
| 3 | [Project Euler 10 - Summation of primes](https://projecteuler.net/problem=10) | 200만 이하 소수의 합 | `prime_sum(2·10⁶)`을 체로 구한 값과 비교해 1단계(소수 테이블)가 맞는지 확인 |
| 4 | [Library Checker - Sum of Totient Function](https://judge.yosupo.jp/problem/sum_of_totient_function) | `Σ φ(m)`, `N ≤ 10¹⁰` | `sum_totient`와 같은 문제. 2단계(재귀)의 전형 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
