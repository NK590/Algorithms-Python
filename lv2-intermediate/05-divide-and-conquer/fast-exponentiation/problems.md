# 연습문제 — 빠른 거듭제곱

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 1629 곱셈](https://www.acmicpc.net/problem/1629) | 기본형 | `A^B mod C`, 모두 21억 이하. [solution.py](solution.py)의 `main()`이 같은 형태를 처리한다 |
| 2 | [LeetCode 50 Pow(x, n)](https://leetcode.com/problems/powx-n/) | 실수, 음수 지수 | `x^n`, n이 음수일 수 있다. `power_float` |
| 3 | [LeetCode 372 Super Pow](https://leetcode.com/problems/super-pow/) | 큰 지수 | 지수가 배열로 주어진 매우 큰 수. `a^(10k + d) = (a^k)^10 · a^d` |
| 4 | [백준 13172 Σ](https://www.acmicpc.net/problem/13172) | 모듈러 역원 | 기댓값 합을 `p`로 나눈 값을 `mod 1,000,000,007`으로. 분모의 역원 = `b^(M−2)` |
| 5 | [백준 11444 피보나치 수 6](https://www.acmicpc.net/problem/11444) | n이 10¹⁸ | `F(n) mod 1,000,000,007`. 배가법 `fibonacci_doubling` 또는 행렬 거듭제곱 |
| 6 | [백준 10830 행렬 제곱](https://www.acmicpc.net/problem/10830) | 행렬 | 숫자 대신 행렬을 곱하는 같은 틀 |
| 7 | [백준 2749 피보나치 수 3](https://www.acmicpc.net/problem/2749) | 피사노 주기 / 배가법 | 매우 큰 n의 피보나치 수의 나머지 |

## 풀이 메모

- 1번에서 중간 결과에 `% C`를 매번 적용했는지 확인하세요. 마지막에만 나누면 느립니다.
- 5번과 7번은 [행렬 거듭제곱](../../../lv3-advanced/07-dp-advanced/matrix-exponentiation/)의 가장 쉬운 예입니다. 배가법은 같은 값을 행렬 없이 두 변수로 계산합니다. ([테스트](test_solution.py)의 `test_fibonacci_doubling_matches_loop`)
- 4번은 약분이 필요 없고 분모의 모듈러 역원만 구하면 됩니다. 역원은 `pow(b, M - 2, M)`입니다. ([모듈러 역원](../../06-number-theory/modular-inverse/))
- 6번과 같은 행렬 곱셈을 직접 구현하면 `power_mod`의 `*`를 행렬 곱셈으로, 단위원 `1`을 단위 행렬로 바꾸는 것임을 알 수 있습니다.
