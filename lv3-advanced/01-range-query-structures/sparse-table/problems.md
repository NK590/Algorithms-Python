# 연습문제 — 희소 배열

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 10868 최솟값](https://www.acmicpc.net/problem/10868) | 정적 RMQ | 기본형. [solution.py](solution.py)의 `main()`이 같은 형태. 닫힌 구간 `[a, b]`(1부터) → `query(a − 1, b)` |
| 2 | [백준 2357 최솟값과 최댓값](https://www.acmicpc.net/problem/2357) | 최솟값 + 최댓값 | 표 두 개 (`min`, `max`) |
| 3 | [LeetCode 1438 Longest Continuous Subarray With Absolute Diff ≤ Limit](https://leetcode.com/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/) | 투 포인터 + RMQ | 구간의 `max − min`을 매번 `O(1)`로 확인. (모노톤 덱으로도 풀린다) |
| 4 | [백준 2104 부분배열 고르기](https://www.acmicpc.net/problem/2104) | 최솟값 × 합 | 구간 최솟값(RMQ)과 구간 합(누적 합)을 함께 쓰는 분할 정복 또는 스택 풀이 |
| 5 | [백준 6549 히스토그램에서 가장 큰 직사각형](https://www.acmicpc.net/problem/6549) | RMQ + 분할 정복 | 구간의 최솟값 위치(`RangeArgmin`)로 나누는 풀이. 모노톤 스택이 더 간단하지만 분할 정복 연습용 |
| 6 | [백준 17435 합성함수와 쿼리](https://www.acmicpc.net/problem/17435) | 점프 표 | `f^(2^k)(x)` 표를 만들어 `f^n(x)`를 `n`의 이진수대로 합성. 구간 대신 이동을 합성하는 같은 아이디어 |
| 7 | [백준 11437 LCA](https://www.acmicpc.net/problem/11437) | 오일러 투어 + RMQ | 트리를 DFS 순서의 배열로 펴고 구간 최소 깊이로 LCA. [최소 공통 조상](../../03-graph-advanced/lca/)을 배우면 다시 풀어 보기 |

## 풀이 메모

- 1번과 2번은 값이 바뀌지 않으므로 [세그먼트 트리](../segment-tree/)보다 희소 배열이 질의 시간이 짧습니다([README](README.md#5-복잡도와-입력-크기-가이드)의 측정값). [테스트](test_solution.py)가 모든 구간을 직접 계산한 값과 비교합니다.
- 3번은 투 포인터마다 `max`와 `min`의 희소 배열로 `O(1)`에 확인하면 전체 `O(n log n)` 구축 + `O(n)` 탐색입니다.
- 4번과 5번은 "구간에서 최솟값의 위치를 기준으로 왼쪽/오른쪽으로 나눈다"는 같은 분할 정복입니다. `RangeArgmin`이 이 위치를 `O(1)`에 줍니다.
- 6번에서 `table[k][x]`를 `table[k−1][table[k−1][x]]`로 만드는 방식은 [희소 배열](README.md#2-핵심-아이디어)의 `table[k] = f(table[k−1], …)`와 같은 아이디어입니다.
