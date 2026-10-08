# 연습문제 — 오일러 피 함수

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 4355 서로소](https://www.acmicpc.net/problem/4355) | `φ(n)` 기본형 | 소인수분해로 `n · Π(1 − 1/p)`. 여러 개의 `n`이 입력되므로 `O(√n)`을 매번 돈다. `n = 1`일 때 문제의 정의를 확인할 것 |
| 2 | [백준 11689 GCD(n, k) = 1](https://www.acmicpc.net/problem/11689) | `φ(n)`, n이 매우 큼 | `n`이 10¹²까지라 `gcd`를 하나씩 부르는 방법은 불가능. 소인수분해 한 번 |
| 3 | [LeetCode 372 Super Pow](https://leetcode.com/problems/super-pow/) | 확장 오일러 정리 | `a^b mod 1337`, `b`가 아주 긴 수. `1337 = 7 · 191`이라 `φ(1337) = 1140`. 지수를 `φ`로 줄이되 서로소가 아닌 경우를 조심 |
| 4 | [Project Euler 72 Counting fractions](https://projecteuler.net/problem=72) | `Σ φ` | `d ≤ 10⁶`인 기약 진분수의 개수 = `Σ_{q=2..d} φ(q)`. `phi_table`로 풀린다. `count_proper_reduced_fractions`가 같은 계산 |
| 5 | [Project Euler 69 Totient maximum](https://projecteuler.net/problem=69) | 공식 변형 | `n / φ(n) = Π p/(p − 1)`이 소인수의 종류에만 의존한다는 관찰로, 작은 소수를 모두 곱한 수가 답 |
| 6 | [Project Euler 70 Totient permutation](https://projecteuler.net/problem=70) | `φ`의 자릿수 조건 | `n / φ(n)`을 최소화하는 `n`을 찾을 때 `φ(n)`이 `n`의 자릿수 재배열이 되어야 함. 소인수가 두 개일 때가 후보 |

## 풀이 메모

- 1, 2번은 [solution.py](solution.py)의 `phi`를 그대로 쓰면 됩니다. [테스트](test_solution.py)가 모든 작은 `n`에서 `gcd`로 세어 본 값과 비교합니다.
- 4번처럼 "모든 `q`에 대한 합"이면 `phi`를 `q`마다 부르지 말고 `phi_table`을 쓰세요. `10⁶`에서 표가 0.5초, 하나씩 `phi`를 부르면 훨씬 오래 걸립니다([README](README.md#5-복잡도와-입력-크기-가이드)의 측정값 참고).
- 3번에서 지수를 `φ`로만 나눈 나머지로 바꾸면 `gcd(a, 1337) ≠ 1`인 `a`(7, 191의 배수)에서 틀립니다. `e ≥ φ(m)`이면 `e mod φ(m) + φ(m)`을 쓰는 `pow_mod_large_exponent`의 규칙을 떠올리세요. (지수가 큰 수의 문자열 배열로 주어지므로 자리마다 `φ`로 줄인 나머지를 갱신하거나, 또는 `a^(10k+d) = (a^k)^10 · a^d`를 쓰는 방법이 있다)
- 5, 6번은 코드로 `n`을 전부 돌려 보는 방법과 수학적으로 후보를 좁히는 방법의 차이를 체감하기 좋은 문제입니다.
