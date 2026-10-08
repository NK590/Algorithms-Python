# 연습문제 — 볼록 껍질 트릭

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [AtCoder Educational DP Z - Frog 3](https://atcoder.jp/contests/dp/tasks/dp_z) | `dp[i] = min_j dp[j] + (h_i − h_j)² + C` | `min_cost_batches`와 같은 점화식. 기울기 `−2h_j`는 내림차순, 질의 `h_i`는 오름차순. `O(n²)` DP와 비교 |
| 2 | [백준 6171 땅 사기](https://www.acmicpc.net/problem/6171) | 직사각형 묶음 | [solution.py](solution.py)의 `main()`이 같은 형태. 가려지는 땅을 먼저 버리는 단계가 핵심 |
| 3 | [백준 13263 나무 자르기](https://www.acmicpc.net/problem/13263) | `dp[i] = min_j dp[j] + b_j · a_i` | 가장 순수한 형태. `b`는 내림차순, `a`는 오름차순으로 주어진다 |
| 4 | [Codeforces 319C Kalila and Dimna](https://codeforces.com/problemset/problem/319/C) | 같은 점화식 + 입력 정렬이 보장됨 | 문제 조건에서 기울기·질의의 단조성을 찾아내는 연습 |
| 5 | [백준 4008 특공대](https://www.acmicpc.net/problem/4008) | 이차식 최대화 | 2차 항의 계수가 음수. 최대 껍질(`maximize=True`)과 기울기 방향 |
| 6 | [백준 10067 수열 나누기](https://www.acmicpc.net/problem/10067) | `k`층 DP + CHT | 층마다 CHT를 새로 만든다. 경로 복원 |
| 7 | [Codeforces 660F Bear and Bowling 4](https://codeforces.com/problemset/problem/660/F) | 부분 배열의 점수 최대화 | 질의 `x`가 정렬되지 않아 이진 탐색 `query`나 리차오 트리가 필요 |
| 8 | [백준 12795 반평면 땅따먹기](https://www.acmicpc.net/problem/12795) | 직선 추가 + 임의 `x` 최대 질의 | 기울기가 정렬되지 않았다. 리차오 트리(`LiChaoTree`)나 동적 CHT |
| 9 | [Codeforces 1083E The Fair Nut and Rectangles](https://codeforces.com/problemset/problem/1083/E) | 직사각형 합집합 넓이 − 비용 | 정렬 후 `dp[i] = max_j dp[j] − x_j·y_i + ...`. 겹치는 부분을 빼는 항의 분리 |

## 풀이 메모

- 1번은 `O(n²)` DP를 먼저 짜서 작은 입력을 검증한 뒤 `min_cost_batches`와 비교하세요. 이 환경에서 `n = 4000`에서 CHT 0.0055초, 단순 DP 1.02초였습니다.
- 2번은 정렬 키를 `(−w, −h)`로 두고 `h`가 이전 최댓값보다 클 때만 남기는 방식입니다. 이 단계를 빼먹으면 `h`가 내림차순이 아니라 CHT의 전제가 깨집니다.
- 3번, 4번처럼 문제 조건이 단조성을 *보장*하는 경우가 많습니다. 보장되지 않는 7번, 8번에서는 `query`(이진 탐색)나 `LiChaoTree`로 바꿔 쓰는 것을 연습하세요.
- 5번은 점화식을 전개했을 때 이차 항의 계수가 음수라 최대화 껍질이 됩니다. 기울기가 오름차순으로 들어오도록 변수를 바꾸는 부호 실수가 잦습니다.
- 모든 문제에서 점화식을 `(i만의 항) + (j만의 항) + (i의 값) × (j의 값)`으로 *손으로* 전개하는 것이 첫 단계입니다. 곱 항이 안 나오면 CHT를 쓸 수 없습니다.
