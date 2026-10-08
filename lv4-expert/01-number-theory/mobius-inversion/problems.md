# 연습문제 — 뫼비우스 반전

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 11689 GCD(n, k) = 1](https://www.acmicpc.net/problem/11689) | `φ(n)`, `n ≤ 10¹²` | 뫼비우스 없이도 풀리는 기본. `n`의 약수 `d`에 대한 합 `Σ μ(d)·n/d`와 `Π (1 − 1/p)`가 같은 값임을 확인 |
| 2 | [백준 9359 서로소](https://www.acmicpc.net/problem/9359) | `[A, B]` 중 `N`과 서로소인 수 | `N`의 소인수의 부분집합으로 포함-배제. `count_coprime_to(B, N) − count_coprime_to(A − 1, N)` |
| 3 | [백준 1016 제곱 ㄴㄴ수](https://www.acmicpc.net/problem/1016) | 구간 `[min, max]`의 제곱 없는 수 | 구간이 `10¹²` 근처에서 길이 `10⁶`. 구간 체. `count_squarefree`와 결과 비교 |
| 4 | [AtCoder ABC162 E - Sum of gcd of Tuples (Hard)](https://atcoder.jp/contests/abc162/tasks/abc162_e) | 길이 `N` 수열의 gcd 합 | `g`의 배수만 쓰는 수열 수 `⌊K/g⌋^N`에서 `2g, 3g, …`의 몫을 빼는 *역방향 반전* |
| 5 | [AtCoder ABC206 E - Divisible Pair](https://atcoder.jp/contests/abc206/tasks/abc206_e) | `gcd ≠ 1`이면서 서로 약수가 아닌 쌍 | 서로소 쌍 + 약수 관계 제외. `count_pairs_with_gcd` |
| 6 | [SPOJ VLATTICE - Visible Lattice Points](https://www.spoj.com/problems/VLATTICE/) | 3차원 보이는 점 | `gcd(x, y, z) = 1`인 점 수 = `Σ μ(d)·⌊n/d⌋³` + 좌표축 보정 |
| 7 | [SPOJ PGCD - Primes in GCD Table](https://www.spoj.com/problems/PGCD/) | `gcd`가 소수인 쌍의 수 | 모든 소수 `p`에 대해 `gcd = p`인 쌍을 합친다. `Σ_p Σ_d μ(d)⌊n/(pd)⌋⌊m/(pd)⌋`를 `T = pd`로 묶기 |
| 8 | [Library Checker - Sum of Totient Function](https://judge.yosupo.jp/problem/sum_of_totient_function) | `Σ_{k ≤ N} φ(k)`, `N ≤ 10¹⁰` | 체로는 안 되고 디리클레 쌍곡선 `O(N^(2/3))` 필요. 이 구현의 `Σ gcd` 공식이 출발점 |

## 풀이 메모

- 1번을 [폴라드 로](../pollard-rho/)의 `euler_phi`로도 풀어 보세요. `n ≤ 10¹²`이면 시행 나눗셈으로 충분합니다.
- 2번은 항이 `2^(소인수의 수)`개이고 `N ≤ 10⁹`이면 소인수가 최대 9개라 512개의 약수만 훑으면 됩니다.
- 4번은 `f(g) = (gcd가 정확히 g인 수열의 수)`, `F(g) = (gcd가 g의 배수인 수열의 수) = ⌊K/g⌋^N`이라 `F(g) = Σ_{g|h} f(h)`입니다. *배수 합*에 대한 반전이라 `g`를 큰 것부터 처리하며 `f(g) = F(g) − Σ_{k ≥ 2} f(kg)`로 푸는 것이 약수 합 반전의 거울상입니다.
- 5번은 먼저 "서로소가 아닌 쌍"을 센 뒤, 한쪽이 다른 쪽의 약수인 쌍을 빼는 방식입니다.
- 6번, 7번, 8번은 `⌊n/d⌋` 블록 분해와 메르텐스 함수의 응용입니다. 7번은 소수 `p`마다 블록 분해를 하면 느리므로 `T = pd`로 변수를 바꿔 한 번의 체로 해결합니다.
