# 연습문제 — 조합 nCr mod p

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 11050 이항 계수 1](https://www.acmicpc.net/problem/11050) | 정의 그대로 | `n`이 매우 작다. `math.comb`나 팩토리얼 나눗셈으로 충분 |
| 2 | [백준 11051 이항 계수 2](https://www.acmicpc.net/problem/11051) | 파스칼의 삼각형 | `n ≤ 1000`에 `mod 10007`. 나눗셈 없이 덧셈만으로 `binomial_pascal` |
| 3 | [백준 11401 이항 계수 3](https://www.acmicpc.net/problem/11401) | 팩토리얼 + 역원 | `n`이 400만, `mod 1,000,000,007`. [solution.py](solution.py)의 `main()`이 같은 형태(`binomial_once`) |
| 4 | [LeetCode 62 Unique Paths](https://leetcode.com/problems/unique-paths/) | 격자 경로 | 오른쪽·아래로만 가는 경로 수 = `C(m + n − 2, m − 1)`. `grid_paths_mod`와 같은 식 |
| 5 | [LeetCode 96 Unique Binary Search Trees](https://leetcode.com/problems/unique-binary-search-trees/) | 카탈란 수 | 노드 `n`개 이진 탐색 트리의 모양 수. `catalan_mod`. DP로도 풀 수 있으니 두 방법을 비교 |
| 6 | [백준 10422 괄호](https://www.acmicpc.net/problem/10422) | 카탈란 수 | 길이 `L`의 올바른 괄호 문자열의 수를 `mod 1,000,000,007`로. 홀수 길이는 0 |
| 7 | [AtCoder ABC145 D - Knight](https://atcoder.jp/contests/abc145/tasks/abc145_d) | 식 세우기 + 조합 | 두 가지 이동의 횟수를 연립방정식으로 구한 뒤 `C(a + b, a)`. 정수 해가 없으면 0 |
| 8 | [LeetCode 1569 Number of Ways to Reorder Array to Get Same BST](https://leetcode.com/problems/number-of-ways-to-reorder-array-to-get-same-bst/) | 재귀 + 조합 | 루트 이후의 왼쪽·오른쪽 서브트리 원소들을 섞는 방법 `C(l + r, l)`을 재귀로 곱한다. 원래 배열 자신은 세지 않으므로 마지막에 1을 뺀다 |
| 9 | [LeetCode 1735 Count Ways to Make Array With Product](https://leetcode.com/problems/count-ways-to-make-array-with-product/) | 소인수분해 + 별과 막대 | 곱이 `k`인 길이 `n`의 배열 수. `k`를 소인수분해해 소인수마다 중복 조합으로 지수를 나누고 곱한다 |

## 풀이 메모

- 3번은 `n`이 400만이라 표 `build_factorials`를 만들면 파이썬에서 시간이 걸립니다(`n = 10⁶`에서 0.2초). 질의가 하나뿐이라 `binomial_once`로 `r`번의 곱만 하면 됩니다(`r = min(r, n − r)`).
- 2번은 `10007`이 소수지만 `n ≤ 1000 < 10007`이라 팩토리얼 방식도 가능합니다. 파스칼은 모듈러가 합성수일 때도 되는 방법임을 알아 두세요. [테스트](test_solution.py)의 `test_pascal_works_for_composite_moduli`.
- 5번과 6번은 같은 수열(`C_n`)입니다. 6번은 `L`이 짝수일 때 `C_{L/2}`이고 `C(2n, n) − C(2n, n+1)`이라 `n+1`의 역원이 필요 없습니다.
- 7번은 두 종류의 이동 횟수 `a, b`가 `a + 2b = X`, `2a + b = Y`를 만족해야 합니다. 이 연립방정식이 음이 아닌 정수 해를 갖는지 먼저 확인하고(`X + Y`가 3의 배수), 답은 `C(a + b, a)`입니다. 조합이 한 번이라 `binomial_once`로 충분합니다.
- 8번과 9번은 단순한 공식 암기가 아니라 "나누어 세고 곱한다"라는 사고방식을 연습하기 좋습니다.
