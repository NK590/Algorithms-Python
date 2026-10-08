# 연습문제 — 분할 정복 최적화

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [LeetCode 1478 Allocate Mailboxes](https://leetcode.com/problems/allocate-mailboxes/) | 우체통 `k`개의 거리 합 | `n ≤ 100`이라 `O(kn²)`로 충분하지만 비용 `중앙값 거리 합`이 monge인지 `is_monge`로 확인하는 연습 |
| 2 | [백준 11066 파일 합치기](https://www.acmicpc.net/problem/11066) | 구간 DP (크누스 최적화) | 층이 없는 구간 DP의 비교 문제. `opt[l][r−1] ≤ opt[l][r] ≤ opt[l+1][r]` |
| 3 | [백준 13261 탈옥](https://www.acmicpc.net/problem/13261) | 구역 나누기 | [solution.py](solution.py)의 `main()`이 같은 형태. `L ≤ 8000`, `G ≤ 800`이면 `G > L`일 때 처리 |
| 4 | [Codeforces 321E Ciel and Gondolas](https://codeforces.com/problemset/problem/321/E) | 쌍의 비용이 있는 나누기 | 비용 `cost(j, i)` = 구간 안 모든 쌍의 값. 2차원 누적 합으로 `O(1)` |
| 5 | [Codeforces 833B The Bakery](https://codeforces.com/problemset/problem/833/B) | 서로 다른 값의 수의 합 최대 | 비용 = 구간의 서로 다른 값의 수 (최대화). 비용 계산을 구간 이동으로 |
| 6 | [Codeforces 868F Yet Another Minimization Problem](https://codeforces.com/problemset/problem/868/F) | 같은 값 쌍의 수의 합 최소 | 모스 알고리즘 식으로 비용을 점진적으로 갱신하며 분할 정복 안에서 계산 |

## 풀이 메모

- 3번은 층이 100~800개입니다. 한 층을 `next_layer`로 계산한 값을 `O(kn²)` 기준 구현과 먼저 작은 입력에서 비교하세요. 모든 `j`를 확인하는 것보다 얼마나 빠른지 [README](README.md#5-복잡도와-입력-크기-가이드)의 표처럼 측정해 볼 수 있습니다.
- 4번은 비용 `cost(j, i)`가 구간 안 모든 쌍의 값의 합입니다. 2차원 누적 합 `P[i][j]`로 `cost(j, i) = (P[i][i] − P[j][i] − P[i][j] + P[j][j]) / 2`를 `O(1)`에 계산합니다.
- 5번과 6번은 비용이 누적 합이 아니라 *구간의 통계*입니다. 구간을 한 칸씩 늘이고 줄이는 [모스 알고리즘](../../06-query-techniques/mos-algorithm/)의 포인터를 분할 정복 안에 넣어 비용을 `O(1)` 분할 상환으로 계산합니다. `next_layer`는 `cost(j, i)`를 분할 정복의 방문 순서대로 호출하므로, 구간의 두 끝점을 안에 기억해 두고 필요한 만큼만 옮기는 *상태가 있는 `cost` 함수*를 만들어 넘기는 방법을 시도해 볼 수 있습니다.
- 모든 문제에서 먼저 `O(kn²)` DP를 짜서 작은 입력의 정답을 확보한 뒤 최적화하세요. 단조성이 틀리면 조용히 틀린 답이 나옵니다.
