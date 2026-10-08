# 연습문제 — 민-25 체

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [Project Euler 10 - Summation of primes](https://projecteuler.net/problem=10) | 200만 이하 소수의 합 | `prime_sum(2·10⁶)`을 체로 구한 값과 비교해 1단계(소수 테이블)가 맞는지 확인 |
| 2 | [Library Checker - Counting Primes](https://judge.yosupo.jp/problem/counting_primes) | `N ≤ 10¹¹` 이하 소수의 개수 | 1단계만으로 풀린다. 이 구현으로 `10¹¹`은 약 12초 (README 5절) |
| 3 | [Library Checker - Sum of Totient Function](https://judge.yosupo.jp/problem/sum_of_totient_function) | `Σ φ(m)`, `N ≤ 10¹⁰` | `sum_totient`와 같은 문제. 2단계(재귀)의 전형 |
| 4 | [Library Checker - Sum of Multiplicative Function](https://judge.yosupo.jp/problem/sum_of_multiplicative_function) | 임의의 곱셈적 함수의 합 (`f(p)`는 `p`의 저차 다항식) | `min25_sum`에 `prime_poly`와 `prime_power`를 넣어 풀기 |
| 5 | (직접 만들어 보는 문제) 메르텐스 함수 `M(n)` | `Σ μ(m)` | `sum_mobius`로 `M(10⁹)`를 구해 보고, [뫼비우스 반전](../../../lv4-expert/01-number-theory/mobius-inversion/)의 도로 푸는 풀이 (`O(n^{2/3})`)와 시간·구현을 비교 |

## 풀이 메모

- 1번은 한 줄이면 되지만 일부러 큰 `n`과 체로 구한 값을 비교하는 *검증 습관* 을 기르는 문제입니다 (이 저장소의 테스트가 같은 방식).
- 3~4번의 핵심은 **`f(p)`가 `p`의 다항식인지** 보는 것입니다. `f(p) = p − 1`(`φ`), `p + 1`(`σ`), `−1`(`μ`)은 다항식이라 가능하고, `f(p)`가 `p mod 4`에 의존하는 함수는 소수 테이블을 잔여류별로 나누어야 합니다 (이 구현 범위 밖).
- 5번에서 `M(10⁹) = −222`, `M(10¹⁰) = −33722`가 나옵니다 (실행으로 확인).
