# 연습문제 — 밀러-라빈 소수 판정법

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [LeetCode 204 Count Primes](https://leetcode.com/problems/count-primes/) | 소수의 개수 | 체로 풀리는 크기. 밀러-라빈으로도 풀어 보고 어느 범위부터 체가 느려지는지 비교 |
| 2 | [백준 1929 소수 구하기](https://www.acmicpc.net/problem/1929) | 구간의 소수 출력 | 구간 전체는 체가 맞다. `is_prime`을 하나씩 부르는 풀이와 시간을 비교 |
| 3 | [SPOJ PON - Prime or Not](https://www.spoj.com/problems/PON/) | 소수 판정 (질의 여러 개) | 밀러-라빈의 가장 순수한 문제. 입력이 `10⁹`에서 `10¹⁸` 사이 |
| 4 | [백준 5615 아파트 임대](https://www.acmicpc.net/problem/5615) | `2S + 1`이 소수인가 | [solution.py](solution.py)의 `main()`이 같은 형태. `S = 2xy + x + y` → `2S + 1 = (2x + 1)(2y + 1)`로 변형하는 단계가 핵심 |
| 5 | [Library Checker - Primality Test](https://judge.yosupo.jp/problem/primality_test) | 소수 판정, 질의 10⁵개, `N ≤ 10¹⁸` | 결정적 밑 집합의 정당성. 파이썬이 시간 안에 들어오는지 측정 |
| 6 | [백준 4149 큰 수 소인수분해](https://www.acmicpc.net/problem/4149) | 소인수분해 | 밀러-라빈 + [폴라드 로](../pollard-rho/). 이 문서의 `is_prime`이 분해의 중간 단계 |

## 풀이 메모

- 1번과 2번은 체로 푸는 것이 정답입니다. 같은 범위를 `is_prime`으로 훑어 보고 [복잡도 치트시트](../../../docs/complexity-cheatsheet.md)의 입력 크기 가이드와 비교하세요.
- 3번과 5번은 입력 수가 많으므로 `sys.stdin.buffer.read().split()`로 한 번에 읽고 한 번에 출력하세요. `is_prime`은 작은 소수로 먼저 거르기 때문에 합성수 대부분은 매우 빠르게 처리됩니다.
- 4번은 소수 판정 문제로 변형되는 과정을 직접 유도해 보세요. 식 `S = 2xy + x + y`의 양변에 2를 곱하고 1을 더하면 `2S + 1 = 4xy + 2x + 2y + 1 = (2x + 1)(2y + 1)`. 따라서 `2S + 1`이 소수이면 그런 `x, y ≥ 1`이 없습니다.
- 6번은 [폴라드 로](../pollard-rho/)와 함께 풉니다. 먼저 `is_prime`으로 소수인지 확인하고, 합성수라면 약수 하나를 찾는 과정을 반복합니다.
