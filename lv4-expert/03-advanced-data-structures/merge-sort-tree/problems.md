# 연습문제 — 머지 소트 트리

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 13537 수열과 쿼리 1](https://www.acmicpc.net/problem/13537) | 구간에서 `k`보다 큰 수의 개수 | 가장 기본형. `(길이) − count_at_most`. 오프라인(펜윅)으로도 풀리니 둘 다 짜서 비교 |
| 2 | [SPOJ KQUERY - K-Query](https://www.spoj.com/problems/KQUERY/) | 구간에서 `k`보다 큰 수의 개수 | 1번과 같은 유형. 질의 수가 많을 때 파이썬 상수를 가늠 |
| 3 | [백준 13544 수열과 쿼리 3](https://www.acmicpc.net/problem/13544) | 1번과 같은 질의 + 이전 답으로 복원(온라인) | [solution.py](solution.py)의 `main()`이 같은 형태. 오프라인 풀이가 막혀 있어서 머지 소트 트리가 맞는 도구 |
| 4 | [Library Checker - Static Range Frequency](https://judge.yosupo.jp/problem/static_range_frequency) | 구간에서 값 `x`가 나오는 횟수 | `count_in_value_range(l, r, x, x)`. 값별 위치 리스트에 이분 탐색하는 풀이와 비교 |
| 5 | [SPOJ GIVEAWAY - Give Away](https://www.spoj.com/problems/GIVEAWAY/) | **갱신이 있는** 구간에서 `x` 이상의 수의 개수 | `update`가 필요한 문제. 정렬된 블록(제곱근 분할)과 구현·속도 비교 |
| 6 | [백준 7469 K번째 수](https://www.acmicpc.net/problem/7469) | 구간 `k`번째로 작은 수 | `kth_smallest`는 `O(log³ n)`이라 느리다. [퍼시스턴트](../persistent-segment-tree/)·[웨이블릿](../wavelet-tree/) `O(log n)`과 시간을 비교 |
| 7 | [Library Checker - Range Kth Smallest](https://judge.yosupo.jp/problem/range_kth_smallest) | 구간 `k`번째 (큰 입력) | 머지 소트 트리로는 느릴 수 있다. 어떤 크기에서 구조를 바꿔야 하는지 직접 확인 |

## 풀이 메모

- 1번~3번은 같은 질의의 세 가지 얼굴입니다. 1번과 2번은 질의를 먼저 읽어 정렬할 수 있어 오프라인 펜윅 트리로도 풀리지만, 3번은 이전 답으로 질의가 정해지므로 구조 자체가 온라인이어야 합니다.
- 4번은 `[l, r)`에서 값이 `[x, x]` 범위인 개수이므로 `count_in_value_range`를 그대로 씁니다. 다른 풀이로 "값마다 위치를 정렬한 리스트를 만들고 `bisect`로 `[l, r)` 안의 개수를 센다" 가 있습니다 (메모리 `O(n)`).
- 5번은 갱신이 있는 거의 유일한 이 단원 문제입니다. 머지 소트 트리의 `update`는 최악 `O(n)`이지만 리스트 이동이 C 속도라 파이썬에서도 통합니다. 정렬된 블록을 쓰는 제곱근 분할과 비교하면 어느 쪽이 파이썬에서 유리한지 알 수 있습니다.
- 6번과 7번은 `kth_smallest`가 값에 대한 이분 탐색(`O(log n)`번) × `count_at_most`(`O(log² n)`)이라 입력이 크면 느립니다. 질의가 `10⁵` 이상이면 웨이블릿 트리나 퍼시스턴트 세그먼트 트리로 바꾸는 것이 맞습니다.
