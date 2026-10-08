# 연습문제 — 리 차오 트리 심화

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [Library Checker - Line Add Get Min](https://judge.yosupo.jp/problem/line_add_get_min) | 직선 추가 + 임의 `x` 최솟값 | 기본형. `add_line`/`query`. 정의역은 질의 `x` 범위로 잡거나 `±10⁹` |
| 2 | [백준 12795 반평면 땅따먹기](https://www.acmicpc.net/problem/12795) | 직선 추가 + 임의 `x` 최댓값 | `maximize=True`. [볼록 껍질 트릭](../../../lv3-advanced/07-dp-advanced/convex-hull-trick/)의 연습문제에도 있습니다 |
| 3 | [Library Checker - Segment Add Get Min](https://judge.yosupo.jp/problem/segment_add_get_min) | 선분 추가 + 최솟값, 없으면 `INFINITY` | [solution.py](solution.py)의 `main()`이 같은 형태. 반열린 `[l, r)` → 닫힌 `[l, r−1]`, 질의가 선분 밖이면 `None` |
| 4 | [Codeforces 678F Lena and Queries](https://codeforces.com/problemset/problem/678/F) | 직선을 넣고 빼며 `x = q`에서 최댓값 질의 | 삭제가 있는 문제. 오프라인 시간 구간 트리 + 롤백 (`min_over_time`의 형태). 삭제를 직접 구현하지 않고 우회 |
| 5 | [Codeforces 932F Escape Through Leaf](https://codeforces.com/problemset/problem/932/F) | 트리 DP: `dp[v] = min (a_v · b_u + dp[u])`, `u`는 `v`의 서브트리 | 리 차오 트리 병합 또는 작은 쪽을 큰 쪽에 합치기. 서브트리가 연속 구간이 되는 오일러 투어 + 선분 트리와도 푼다 |
| 6 | [Codeforces 1303G Sum of Prefix Sums](https://codeforces.com/problemset/problem/1303/G) | 트리의 모든 경로에 대한 접두사 합의 합 최대화 | [센트로이드 분해](../../02-tree-decomposition/centroid-decomposition/) + 직선으로 바꿔 질의. 경로를 센트로이드에서 양쪽으로 나눠 `직선 ∪ 질의` 구조 |
| 7 | [Codeforces 1175G Yet Another Partiton Problem](https://codeforces.com/problemset/problem/1175/G) | 수열을 `k`개로 나눠 `(구간 길이 × 구간 최솟값)`의 합 최소화 | 단조 스택 + **퍼시스턴트 리 차오 트리**(스택 팝 시 되돌리기). 이 단원에서 가장 어려운 응용 |

## 풀이 메모

- 1번~2번은 *직선 전체* 가 유효한 기본형이고 [CHT](../../../lv3-advanced/07-dp-advanced/convex-hull-trick/)의 `LiChaoTree`와 같습니다. 3번이 이 단원의 새 내용(선분)입니다.
- 3번에서 질의가 어떤 선분에도 덮이지 않는 `x`를 물으면 `None`을 `INFINITY`로 출력합니다. 정의역은 `[−10⁹, 10⁹]`로 두었습니다.
- 4번은 직선 `y = ax + b`가 추가되었다가 삭제되고 그 사이에 질의가 끼는 문제입니다. 각 직선이 존재한 시각 구간 `[추가 시각, 삭제 시각)`을 정리하면 `min_over_time(…, maximize=True)`가 그대로 대응합니다 (삭제되지 않은 직선은 끝 시각을 질의 수 + 1 정도로 잡습니다).
- 5번의 점화식 `dp[v] = min_u (a_v · b_u + dp[u])`는 *서브트리 안의 모든 `u`* 에서 직선 `(b_u, dp[u])`를 모아 `x = a_v`에서 질의하는 형태입니다. 서브트리를 오일러 투어 구간으로 보고 구간 트리의 노드마다 리 차오 트리를 두는 풀이가 구현이 쉬운 편입니다.
- 6번과 7번은 이 단원 구조들을 다른 기법(센트로이드 분해, 단조 스택 + 퍼시스턴트)과 결합하는 문제입니다. 먼저 직선으로 환원하는 단계를 종이에 전개한 뒤 구조를 고르세요.
