# 연습문제 — 다익스트라

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 1753 최단경로](https://www.acmicpc.net/problem/1753) | 기본형 | 가장 기본적인 단일 시작점 최단 거리. [solution.py](solution.py)의 `main()`이 이 문제의 입력 형식을 그대로 처리한다 |
| 2 | [백준 1916 최소비용 구하기](https://www.acmicpc.net/problem/1916) | 기본형 | 시작점과 도착점이 모두 정해진 경우. 1번과 같은 코드에서 출력만 달라진다 |
| 3 | [백준 5972 택배 배송](https://www.acmicpc.net/problem/5972) | 무방향 | 양방향 길은 간선을 양쪽에 모두 넣어야 한다 |
| 4 | [백준 11779 최소비용 구하기 2](https://www.acmicpc.net/problem/11779) | 경로 복원 | `prev`를 기록하고 도착점에서 거슬러 올라가 경로를 출력한다 |
| 5 | [백준 4485 녹색 옷 입은 애가 젤다지?](https://www.acmicpc.net/problem/4485) | 격자 | 칸을 정점으로 보고, 칸의 비용을 "들어가는 간선"의 가중치로 바꾼다 |
| 6 | [백준 1504 특정한 최단 경로](https://www.acmicpc.net/problem/1504) | 여러 번 실행 | 시작점을 바꿔 여러 번 실행해 구간별 거리를 이어 붙인다. 경유 순서가 두 가지다 |
| 7 | [백준 1238 파티](https://www.acmicpc.net/problem/1238) | 역방향 그래프 | "모두 → 한 곳"의 거리는 간선을 뒤집은 그래프에서 한 번만 실행하면 된다 |
| 8 | [백준 1162 도로포장](https://www.acmicpc.net/problem/1162) | 상태 확장 | 정점에 "포장한 도로 수"를 붙인 `dist[정점][k]`로 푼다 |

## 함께 보면 좋은 문제

- [백준 13549 숨바꼭질 3](https://www.acmicpc.net/problem/13549): 이동 비용이 0 또는 1이다. 다익스트라로도 풀리고 [0-1 BFS](../zero-one-bfs/)로 더 빠르게 풀 수 있어서 둘을 비교해 보기 좋다.
- [Codeforces 20C Dijkstra?](https://codeforces.com/problemset/problem/20/C): 경로를 출력하는 영어 문제. 경로가 없으면 `-1`을 출력한다.
- [LeetCode 743 Network Delay Time](https://leetcode.com/problems/network-delay-time/): 다익스트라의 가장 전형적인 형태. 모든 정점에 도달하는 데 걸리는 시간을 묻는다.

## 풀이 메모

- 1번은 [solution.py](solution.py)가 그대로 풀이입니다. 먼저 직접 짜 본 뒤 비교해 보세요.
- 4번은 `dijkstra_with_prev`와 `restore_path`를 그대로 쓰면 됩니다.
