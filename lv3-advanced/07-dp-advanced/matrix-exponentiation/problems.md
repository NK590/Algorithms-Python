# 연습문제 — 행렬 거듭제곱

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [LeetCode 509 Fibonacci Number](https://leetcode.com/problems/fibonacci-number/) | 피보나치 | `n ≤ 30`. 반복문·행렬·두 배 공식 세 방법이 모두 같은 값을 주는지 확인 |
| 2 | [백준 2748 피보나치 수 2](https://www.acmicpc.net/problem/2748) | 피보나치 (정확한 값) | `n ≤ 90`. 파이썬은 큰 정수가 자동. `mod` 없는 `fibonacci_matrix` |
| 3 | [백준 2749 피보나치 수 3](https://www.acmicpc.net/problem/2749) | 피보나치 mod 10⁶ | `n ≤ 10¹⁸`. 피사노 주기(150만)로 줄이는 방법과 행렬 거듭제곱 두 풀이 |
| 4 | [백준 11444 피보나치 수 6](https://www.acmicpc.net/problem/11444) | 피보나치 mod 10⁹+7 | [solution.py](solution.py)의 `main()`이 같은 형태. `n ≤ 10¹⁸` |
| 5 | [백준 10830 행렬 제곱](https://www.acmicpc.net/problem/10830) | 행렬의 거듭제곱 | `B ≤ 10¹¹`, 결과를 1000으로 나눈 나머지. **`B = 1`일 때 입력 행렬의 원소에도 나머지를 취해야** 한다 |
| 6 | [LeetCode 1137 N-th Tribonacci Number](https://leetcode.com/problems/n-th-tribonacci-number/) | 3항 점화식 | `linear_recurrence_nth([1, 1, 1], [0, 1, 1], n)` |
| 7 | [Codeforces 450B Jzzhu and Sequences](https://codeforces.com/problemset/problem/450/B) | 2항 점화식, 음수 계수 | `fₙ = fₙ₋₁ − fₙ₋₂`. 나머지가 음수가 되지 않게. 사실 주기 6이라 행렬 없이도 풀리는 것을 알아채 보기 |
| 8 | [백준 12850 본대 산책2](https://www.acmicpc.net/problem/12850) | 정확히 `D`개의 간선 경로 | 8개 정점의 고정 그래프. `count_walks` |
| 9 | [백준 14289 본대 산책 3](https://www.acmicpc.net/problem/14289) | 일반 그래프의 경로 수 | 정점 수 `N ≤ 50`, `D ≤ 10⁹`. 방향 없는 간선은 대칭 |
| 10 | [LeetCode 935 Knight Dialer](https://leetcode.com/problems/knight-dialer/) | 전화 키패드 위 나이트 | 10개 상태의 행렬. `n ≤ 5000`이라 단순 DP도 되니 두 방법 비교 |
| 11 | [백준 11440 피보나치 수의 제곱의 합](https://www.acmicpc.net/problem/11440) | 합 | `ΣF(i)² = F(n)·F(n+1)`. 공식과 `recurrence_prefix_sum` 두 방법 |
| 12 | [백준 13976 타일 채우기 2](https://www.acmicpc.net/problem/13976) | `3 × N` 도미노 | `N ≤ 10¹⁸`. `N`이 홀수면 0, 짝수면 `m = N/2`에 대해 `bₘ = 4bₘ₋₁ − bₘ₋₂` (1, 3, 11, 41, …) |
| 13 | [Codeforces 691E Xor-sequences](https://codeforces.com/problemset/problem/691/E) | 조건부 이웃 그래프의 경로 수 | 두 수의 XOR의 1비트 수가 3의 배수이면 간선. `k ≤ 10¹⁸`, 정점 수 `n ≤ 100` |
| 14 | [AtCoder ABC009 D 漸化式](https://atcoder.jp/contests/abc009/tasks/abc009_4) | 다른 연산의 행렬 거듭제곱 | 곱셈이 AND, 덧셈이 XOR. 연산만 바꿔도 같은 코드가 된다는 것을 배운다 |

## 풀이 메모

- 1번은 세 구현을 비교해 보세요: 반복문, [`fibonacci_matrix`](solution.py), [`fibonacci_doubling`](solution.py).
- 3번은 같은 문제를 두 가지로 푸는 좋은 연습입니다. 피사노 주기는 `m = 10ᵏ`일 때 `15·10ᵏ⁻¹` (`10⁶`이면 150만). 주기를 쓰면 `n mod 주기`번의 반복만 하면 되지만, 행렬 거듭제곱은 주기를 몰라도 됩니다.
- 5번은 틀리기 쉽습니다: 입력 행렬의 원소가 1000이고 `B = 1`이면 결과도 `1000 mod 1000 = 0`으로 출력해야 합니다. `mat_pow`는 `mod`가 주어지면 입력도 줄입니다.
- 7번은 점화식을 `f₃ = f₂ − f₁`로 풀어 보면 6항 주기라는 것이 보입니다. 행렬을 쓴 풀이와 주기를 쓴 풀이를 비교해 보세요.
- 8번과 9번은 같은 구조입니다. 8번은 정점 8개의 고정 그래프라 인접 행렬을 직접 쓰고, 9번은 입력으로 받습니다.
- 12번은 `3 × N` 타일링의 수를 작은 `N`(2, 4, 6)에서 손으로 세어 1, 3, 11, 41을 확인하고, 짝수 열만 보면 2차 점화식 `bₘ = 4bₘ₋₁ − bₘ₋₂`임을 확인하세요. 그러면 2 × 2 행렬이면 충분합니다.
- 13번과 14번은 행렬의 "원소"가 다른 대수 구조일 수 있다는 것을 알려 줍니다. 13번의 간선 조건은 비트 개수, 14번은 연산 자체가 AND/XOR입니다.
