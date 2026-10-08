# 연습문제 — 퍼시스턴트 세그먼트 트리

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [SPOJ MKTHNUM - K-th Number](https://www.spoj.com/problems/MKTHNUM/) | 구간 `k`번째로 작은 수 | 가장 기본형. 값 압축 + 앞의 `i`개를 넣은 버전 |
| 2 | [백준 7469 K번째 수](https://www.acmicpc.net/problem/7469) | 구간 `k`번째로 작은 수 | [solution.py](solution.py)의 `main()`이 같은 형태. 1번과 같은 문제 |
| 3 | [백준 13544 수열과 쿼리 3](https://www.acmicpc.net/problem/13544) | 구간에서 `k`보다 큰 수의 개수, 온라인(이전 답으로 질의 복원) | `count_at_most`로 `(길이) − 개수`. 오프라인 풀이가 막혀 있어서 퍼시스턴트·머지 소트 트리가 필요 |
| 4 | [백준 16978 수열과 쿼리 22](https://www.acmicpc.net/problem/16978) | "`k`번째 갱신 직후" 의 구간 합 | 갱신 이력에 접근. 버전 `k`가 곧 `k`번째 갱신 뒤. 오프라인(질의를 `k` 순으로 정렬)로도 풀리니 두 방식을 비교 |
| 5 | [백준 11932 트리와 K번째 수](https://www.acmicpc.net/problem/11932) | 트리 경로 위 `k`번째 수 | 정점마다 루트까지의 버전. 경로의 분포 = `u + v − lca − parent(lca)`. [LCA](../../../lv3-advanced/03-graph-advanced/lca/)와 결합 |
| 6 | [Codeforces 707D Persistent Bookcase](https://codeforces.com/problemset/problem/707/D) | 격자 위 연산들과 "`k`번째 연산 직후 상태로 돌아가기" | 버전이 트리처럼 분기. 오프라인 DFS + 되돌리기, 또는 퍼시스턴트 구조 |
| 7 | [Codeforces 484E Sign on Fence](https://codeforces.com/problemset/problem/484/E) | 구간 안에서 높이 `h` 이상이 이어진 가장 긴 구간 | 높이 순으로 버전을 쌓고 노드에 "왼쪽 연속, 오른쪽 연속, 최대 연속" 을 저장. 답에 대한 이분 탐색 |
| 8 | [Codeforces 464E The Classic Problem](https://codeforces.com/problemset/problem/464/E) | 간선 가중치가 `2^x`인 최단 경로 | 큰 수를 이진수 구간 트리로 표현하고 버전 비교(해시) — 퍼시스턴트 + 해시 + 다익스트라 |

## 풀이 메모

- 1번과 2번은 같은 문제입니다. 구현 후 [웨이블릿 트리](../wavelet-tree/)의 `main()`(Library Checker Range Kth Smallest)이나 [머지 소트 트리](../merge-sort-tree/)와 같은 답이 나오는지 비교해 보세요. 세 구조의 메모리와 시간 차이가 확인됩니다.
- 3번은 전부 온라인입니다. 이전 답과 xor 해서 질의를 복원하므로 질의를 먼저 읽을 수 없습니다. 구간에서 `k`보다 큰 수의 개수 = `(길이) − (k 이하인 수의 개수)`.
- 4번은 같은 입력을 오프라인(질의를 `k` 순으로 정렬해 펜윅 트리 하나로)으로도 풀 수 있습니다. 퍼시스턴트가 필요한 진짜 이유는 *분기* 나 *온라인* 입니다.
- 5번은 루트에서 정점까지의 버전을 `parent`의 버전에 자신의 값을 하나 갱신해서 만듭니다. 구현은 `KthSmallest`와 거의 같고, 차이를 네 버전의 가감으로 계산합니다.
- 6번은 격자의 한 줄을 비트셋으로 보고 구간 트리의 잎을 줄로 삼는 풀이와, 오프라인으로 버전 트리를 DFS 하며 되돌리는 풀이가 있습니다.
- 7번과 8번은 노드에 담는 *값* 이 합이 아니라 구조체(연속 길이 세 개, 해시)입니다. 두 자식을 합치는 규칙만 바꾸면 경로 복사 틀은 그대로입니다.
