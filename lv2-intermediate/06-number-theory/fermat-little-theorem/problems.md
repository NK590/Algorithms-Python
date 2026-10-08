# 연습문제 — 페르마의 소정리

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 1629 곱셈](https://www.acmicpc.net/problem/1629) | 빠른 거듭제곱 | 페르마의 소정리를 쓰기 전에 `a^b mod c`를 `O(log b)`로 계산하는 `power_mod`부터 익힌다 |
| 2 | [백준 11401 이항 계수 3](https://www.acmicpc.net/problem/11401) | 역원 + 조합 | `nCr mod 1,000,000,007`. `r!`과 `(n−r)!`을 `p − 2` 제곱으로 나눈다. [조합 nCr mod p](../ncr-mod/)의 기본형 |
| 3 | [백준 13172 Σ](https://www.acmicpc.net/problem/13172) | 역원 | 기댓값을 기약분수 `a/b`로 나타내 `a · b⁻¹ mod p`를 구하는 문제. `b⁻¹ = b^(p−2)` |
| 4 | [백준 5615 아파트 임대](https://www.acmicpc.net/problem/5615) | 소수 판정 | `2xy + x + y = N`을 만족하는 `x, y`의 존재가 `2N + 1`이 합성수라는 조건으로 바뀐다. 큰 수의 소수 판정이 필요해 페르마 검사의 한계(카마이클 수)를 체감하고 [밀러-라빈](../../../lv4-expert/01-number-theory/miller-rabin/)으로 넘어가는 문제 |

## 풀이 메모

- 2, 3번은 [solution.py](solution.py)의 `inverse_mod_prime`이 하는 일을 그대로 합니다. 입력이 `p`의 배수가 아닌지 확인하는 부분이 빠지기 쉽습니다.
- 4번처럼 소수 판정이 필요하면 [solution.py](solution.py)의 `fermat_test`를 그대로 쓰면 카마이클 수에서 틀릴 수 있습니다. `fermat_pseudoprimes`와 `carmichael_numbers`로 어떤 수가 속이는지 직접 확인해 보세요. (`561`, `1105`, `1729`, …)
- 지수가 `p − 1`을 넘으면 줄여서 계산해도 되지만, `power_mod`는 지수를 비트 단위로 처리해서 지수의 크기와 관계없이 `O(log b)`입니다. 줄이기가 꼭 필요한 경우는 지수 자체가 `b^c`처럼 계산하기 어려운 값일 때입니다.
- 윌슨의 정리나 페르마 검사로 "소수 판정 문제"를 억지로 풀기보다 `n ≤ 10⁷`이면 [체](../../../lv1-elementary/06-number-theory/sieve-of-eratosthenes/)를 쓰는 것이 낫다는 점도 기억해 두세요.
