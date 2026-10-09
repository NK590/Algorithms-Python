# 연습문제 — 기댓값 DP

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [AtCoder — Coins](https://atcoder.jp/contests/dp/tasks/dp_i) | 핵심 연습 | 확률 질량을 동전의 두 결과로 나눠 전달한다 |
| 2 | [AtCoder — Sushi](https://atcoder.jp/contests/dp/tasks/dp_j) | 핵심 연습 | 자기 상태로 되돌아오는 확률을 식의 왼쪽으로 옮긴다 |
| 3 | [LeetCode 1230 Toss Strange Coins](https://leetcode.com/problems/toss-strange-coins/) | 앞면이 정확히 `k`번일 확률 | 확률 DP(앞으로 전파). `dp[i][j]` = `i`개를 던져 앞면 `j`개 |
| 4 | [LeetCode 837 New 21 Game](https://leetcode.com/problems/new-21-game/) | 합이 `K` 이상에서 멈출 때 `N` 이하일 확률 | 슬라이딩 윈도우로 `O(N)`. [expected_rolls_to_reach](solution.py)와 같은 윈도우 구조 |
| 5 | [LeetCode 688 Knight Probability in Chessboard](https://leetcode.com/problems/knight-probability-in-chessboard/) | 나이트가 `k`번 움직인 뒤 판 위에 남을 확률 | 확률 DP, 상태 = (칸, 남은 횟수) |
| 6 | [LeetCode 808 Soup Servings](https://leetcode.com/problems/soup-servings/) | 먼저 비는 확률 | `n`이 매우 크면 확률이 1에 수렴하는 성질로 잘라 낸다 |
| 7 | [AtCoder ABC275 E - Sugoroku 4](https://atcoder.jp/contests/abc275/tasks/abc275_e) | 확률 `mod 998244353` | 역원을 곱해 모듈러로. `fraction_mod`와 같은 변환. 목표를 넘으면 되돌아오는 규칙 |
| 8 | [Codeforces 518D Ilya and Escalator](https://codeforces.com/problemset/problem/518/D) | 에스컬레이터의 평균 인원 | 확률 DP(`n, t ≤ 2000`), 기댓값의 선형성 (각 사람이 탔는지의 확률) |
| 9 | [Codeforces 280C Game on Tree](https://codeforces.com/problemset/problem/280/C) | 정점 지우기 게임의 평균 횟수 | 선형성: 정점 `v`가 한 번의 선택이 되는 확률 `1/depth(v)`의 합 |
| 10 | [AtCoder ABC189 F - Sugoroku2](https://atcoder.jp/contests/abc189/tasks/abc189_f) | 주사위 + 되돌아가는 칸 | `E[s] = a_s + b_s·E[0]` 꼴로 쓰는 "a + b·x 트릭". 무한 루프(불가능) 판정 |
| 11 | [Codeforces 24D Broken Robot](https://codeforces.com/problemset/problem/24/D) | 격자 위 로봇의 평균 이동 횟수 | 한 줄이 삼중 대각 연립방정식. 가우스 소거를 `O(m)`에 (토마스 알고리즘) |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
