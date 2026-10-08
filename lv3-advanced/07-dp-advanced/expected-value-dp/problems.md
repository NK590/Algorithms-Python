# 연습문제 — 기댓값 DP

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [LeetCode 1230 Toss Strange Coins](https://leetcode.com/problems/toss-strange-coins/) | 앞면이 정확히 `k`번일 확률 | 확률 DP(앞으로 전파). `dp[i][j]` = `i`개를 던져 앞면 `j`개 |
| 2 | [AtCoder Educational DP I - Coins](https://atcoder.jp/contests/dp/tasks/dp_i) | 앞면이 더 많을 확률 | 같은 DP, 실수 오차. 정확한 값이 필요하면 `Fraction`으로 바꿔 본다 |
| 3 | [LeetCode 837 New 21 Game](https://leetcode.com/problems/new-21-game/) | 합이 `K` 이상에서 멈출 때 `N` 이하일 확률 | 슬라이딩 윈도우로 `O(N)`. [expected_rolls_to_reach](solution.py)와 같은 윈도우 구조 |
| 4 | [LeetCode 688 Knight Probability in Chessboard](https://leetcode.com/problems/knight-probability-in-chessboard/) | 나이트가 `k`번 움직인 뒤 판 위에 남을 확률 | 확률 DP, 상태 = (칸, 남은 횟수) |
| 5 | [AtCoder Educational DP J - Sushi](https://atcoder.jp/contests/dp/tasks/dp_j) | 접시를 다 비울 때까지의 평균 횟수 | 상태 = (1개, 2개, 3개 남은 접시 수). 자기 자신으로 돌아오는 전이를 정리하는 법 |
| 6 | [LeetCode 808 Soup Servings](https://leetcode.com/problems/soup-servings/) | 먼저 비는 확률 | `n`이 매우 크면 확률이 1에 수렴하는 성질로 잘라 낸다 |
| 7 | [AtCoder ABC275 E - Sugoroku 4](https://atcoder.jp/contests/abc275/tasks/abc275_e) | 확률 `mod 998244353` | 역원을 곱해 모듈러로. `fraction_mod`와 같은 변환. 목표를 넘으면 되돌아오는 규칙 |
| 8 | [Codeforces 518D Ilya and Escalator](https://codeforces.com/problemset/problem/518/D) | 에스컬레이터의 평균 인원 | 확률 DP(`n, t ≤ 2000`), 기댓값의 선형성 (각 사람이 탔는지의 확률) |
| 9 | [Codeforces 280C Game on Tree](https://codeforces.com/problemset/problem/280/C) | 정점 지우기 게임의 평균 횟수 | 선형성: 정점 `v`가 한 번의 선택이 되는 확률 `1/depth(v)`의 합 |
| 10 | [AtCoder ABC189 F - Sugoroku2](https://atcoder.jp/contests/abc189/tasks/abc189_f) | 주사위 + 되돌아가는 칸 | `E[s] = a_s + b_s·E[0]` 꼴로 쓰는 "a + b·x 트릭". 무한 루프(불가능) 판정 |
| 11 | [Codeforces 24D Broken Robot](https://codeforces.com/problemset/problem/24/D) | 격자 위 로봇의 평균 이동 횟수 | 한 줄이 삼중 대각 연립방정식. 가우스 소거를 `O(m)`에 (토마스 알고리즘) |

## 풀이 메모

- 1번과 2번은 확률 DP입니다. 값이 작은 입력에서 `Fraction`으로 바꿔 정확한 확률을 구해 보세요(오차가 없는지).
- 3번의 슬라이딩 윈도우는 [README](README.md)의 `expected_rolls_to_reach`가 쓰는 것과 같은 틀입니다. 합 `window_sum`을 한 칸씩 밀며 갱신하세요.
- 5번은 `E[a, b, c] = 1 + (a/n)·E[a−1, b, c] + (b/n)·E[a+1, b−1, c] + (c/n)·E[a, b+1, c−1] + ((n−a−b−c)/n)·E[a, b, c]`처럼 자기 자신으로 돌아오는 항이 있습니다. 좌변으로 옮겨 `(1 − 자기 확률)`로 나누면 방향이 있는 DP가 됩니다.
- 7번을 풀 때는 확률 `1/6`을 `6⁻¹ mod 998244353`으로 바꿔 모듈러 곱셈으로 유지합니다. 먼저 `Fraction`으로 풀어 작은 입력의 정답을 확보한 뒤 모듈러 풀이와 `fraction_mod`로 비교하세요.
- 9번과 8번은 선형성의 연습입니다. 상태를 만들기 전에 "합으로 쪼갤 수 있는가"를 먼저 물어보세요.
- 10번은 순환이 있어 단순 DP가 안 되는 대표적인 문제입니다. 시작 값을 미지수로 두고 모든 값을 그 미지수의 1차식으로 계산한 뒤 마지막에 일치 조건을 푸세요.
- 11번은 연립방정식이 큰 경우입니다. 이 문서의 `solve_linear`는 `O(S³)`이므로 구조(삼중 대각)를 활용한 `O(S)` 풀이가 필요합니다.
