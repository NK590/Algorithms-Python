# 연습문제 — 뤼카 정리

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [LeetCode 62 Unique Paths](https://leetcode.com/problems/unique-paths/) | `C(m + n − 2, m − 1)` | 정확한 값. `math.comb`와 `binomial_mod`가 같은 나머지를 내는지 비교 |
| 2 | [백준 11401 이항 계수 3](https://www.acmicpc.net/problem/11401) | `C(n, k) mod 10⁹+7`, `n ≤ 4·10⁶` | `n < p`라서 뤼카가 아니라 팩토리얼 + 페르마 역원이 맞다 |
| 3 | [백준 11402 이항 계수 4](https://www.acmicpc.net/problem/11402) | `n ≤ 4·10¹⁸`, `M ≤ 2000` (소수) | [solution.py](solution.py)의 `main()`이 같은 형태. 뤼카의 기본 |
| 4 | [Project Euler 148 - Exploring Pascal's triangle](https://projecteuler.net/problem=148) | 파스칼 삼각형 처음 10⁹줄에서 7로 나누어떨어지지 않는 항의 수 | `n`번째 줄의 개수 `Π (nᵢ + 1)`(7진법), 줄 합을 자릿수 DP처럼 |
| 5 | [Library Checker - Binomial Coefficient (Prime Mod)](https://judge.yosupo.jp/problem/binomial_coefficient_prime_mod) | `n, k ≤ 10¹⁸`, 소수 `m ≤ 10⁶` 질의 여러 개 | 같은 `p`는 표 재사용. 질의 수가 많으면 입력 읽기도 중요 |
| 6 | [Library Checker - Binomial Coefficient](https://judge.yosupo.jp/problem/binomial_coefficient) | 임의의 `m ≤ 10⁷` | 소인수 `p^e`마다 곱 표 + CRT. `binomial_mod`가 그대로 대응 |

## 풀이 메모

- 2번과 3번은 모듈러와 `n`의 크기에 따라 방법이 갈립니다: `n < p`(2번)는 팩토리얼 공식, `n ≥ p`(3번)는 뤼카. 두 방법이 `n < p`에서 같은 값을 내는지 [테스트](test_solution.py)처럼 비교해 보세요.
- 4번은 7진법으로 `n`을 쓴 줄의 "7의 배수가 아닌 항의 수"가 `Π (nᵢ + 1)`임을 뤼카에서 유도합니다. `0..7ᵐ−1`번 줄 전체의 합은 한 자리의 합 `1 + 2 + … + 7 = 28`의 거듭제곱 `28ᵐ`이고, `10⁹`을 7진법으로 쓴 자릿수를 위에서부터 고정해 가며 더하면 답이 나옵니다.
- 5번과 6번은 입력이 많으므로 `sys.stdin.buffer.read().split()` 하나로 읽습니다. 6번은 `m`이 `10⁷`까지라 소인수 `p^e`의 곱 표가 최대 `10⁷`이어서 파이썬에서는 느립니다.
- 모든 문제에서 `m`이 소수인지, 소수의 거듭제곱인지, 일반 합성수인지를 먼저 판단하세요. 이 판단이 방법을 결정합니다.
