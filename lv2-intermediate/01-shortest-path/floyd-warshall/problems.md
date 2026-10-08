# 연습문제 — 플로이드-워셜

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 11404 플로이드](https://www.acmicpc.net/problem/11404) | 기본형 | 같은 쌍의 중복 간선은 최솟값. 닿지 않으면 0 출력. [solution.py](solution.py)의 `main()`이 같은 형태를 처리한다 |
| 2 | [백준 11403 경로 찾기](https://www.acmicpc.net/problem/11403) | 도달 가능성 | 거리 대신 갈 수 있는지(전이적 폐쇄). `transitive_closure` |
| 3 | [백준 1389 케빈 베이컨의 6단계 법칙](https://www.acmicpc.net/problem/1389) | 거리 합 | 모든 쌍의 거리를 구한 뒤 한 사람의 거리 합이 최소인 사람 |
| 4 | [LeetCode 1334 Find the City With the Smallest Number of Neighbors at a Threshold Distance](https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/) | 모든 쌍 + 조건 | 임계 거리 이내의 도시 수. 동점이면 번호가 큰 도시 |
| 5 | [백준 1613 역사](https://www.acmicpc.net/problem/1613) | 전후 관계 | 사건의 선후 관계를 전이적으로 닫아 두 사건의 순서를 질의에 답한다 |
| 6 | [백준 1956 운동](https://www.acmicpc.net/problem/1956) | 가장 짧은 사이클 | 자기 자신으로의 거리를 INF에서 시작. `shortest_cycle` |
| 7 | [백준 11780 플로이드 2](https://www.acmicpc.net/problem/11780) | 경로 복원 | 거리와 함께 경로(`next_hop`)를 출력한다. `restore_path` |
| 8 | [백준 2610 회의준비](https://www.acmicpc.net/problem/2610) | 응용 | 위원회(연결 요소)를 나누고 각 위원회에서 가장 먼 사람까지의 거리가 최소인 대표를 뽑는다 |
| 9 | [백준 1507 궁금한 민호](https://www.acmicpc.net/problem/1507) | 역추적 | 모든 쌍의 최단 거리 표가 주어졌을 때 그래프에 꼭 필요한 간선만 남긴다 |

## 풀이 메모

- 1번에서 **같은 쌍의 간선이 여러 개**라는 점이 초보의 가장 흔한 오답입니다. `init_matrix`가 최솟값만 남기는 이유를 확인하세요.
- 2번과 5번은 가중치 없이 **갈 수 있다/없다**만 보면 되므로, 정수 비트마스크 행을 써서 `rows[i] |= rows[k]` 한 줄로 안쪽 반복을 대체할 수 있습니다.
- 6번은 `dist[i][i]`를 0이 아닌 INF로 시작해야 `i`를 지나 다시 `i`로 돌아오는 가장 짧은 경로가 남습니다. 구현 차이를 `init_matrix`와 `shortest_cycle`에서 비교하세요.
- 7번은 경로 복원 방식(`next_hop`)이 `prev`(마지막 직전 정점)와 어떻게 다른지, 출력할 때 정점 목록을 어떻게 만드는지 비교해 보세요.
- V가 400을 넘으면 CPython에서는 시간 초과 위험이 큽니다. 입력 범위를 먼저 확인하세요.
