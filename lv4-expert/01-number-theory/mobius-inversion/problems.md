# 연습문제 — 뫼비우스 반전

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [AtCoder — Sum of gcd of Tuples (Hard)](https://atcoder.jp/contests/abc162/tasks/abc162_e) | 핵심 연습 | gcd가 배수인 경우의 수에서 정확한 gcd별 수를 복원한다 |
| 2 | [AtCoder — Divisible Pair](https://atcoder.jp/contests/abc206/tasks/abc206_e) | 핵심 연습 | 공약수가 있는 쌍을 포함·배제로 센다 |
| 3 | [SPOJ VLATTICE - Visible Lattice Points](https://www.spoj.com/problems/VLATTICE/) | 3차원 보이는 점 | `gcd(x, y, z) = 1`인 점 수 = `Σ μ(d)·⌊n/d⌋³` + 좌표축 보정 |
| 4 | [SPOJ PGCD - Primes in GCD Table](https://www.spoj.com/problems/PGCD/) | `gcd`가 소수인 쌍의 수 | 모든 소수 `p`에 대해 `gcd = p`인 쌍을 합친다. `Σ_p Σ_d μ(d)⌊n/(pd)⌋⌊m/(pd)⌋`를 `T = pd`로 묶기 |
| 5 | [Library Checker - Sum of Totient Function](https://judge.yosupo.jp/problem/sum_of_totient_function) | `Σ_{k ≤ N} φ(k)`, `N ≤ 10¹⁰` | 체로는 안 되고 디리클레 쌍곡선 `O(N^(2/3))` 필요. 이 구현의 `Σ gcd` 공식이 출발점 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
