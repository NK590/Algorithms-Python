# 연습문제 — 0-1 BFS

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 1261 알고스팟](https://www.acmicpc.net/problem/1261) | 기본형 | 벽을 부수는 최소 횟수. [solution.py](solution.py)의 `main()`이 같은 형태를 처리한다 |
| 2 | [LeetCode 2290 Minimum Obstacle Removal to Reach Corner](https://leetcode.com/problems/minimum-obstacle-removal-to-reach-corner/) | 기본형 | 알고스팟과 같은 문제. `grid_min_walls` |
| 3 | [백준 13549 숨바꼭질 3](https://www.acmicpc.net/problem/13549) | 순간이동 | `x−1`, `x+1`은 비용 1, `2x`는 비용 0. 범위 밖으로 나가지 않게 주의 |
| 4 | [백준 14497 주난의 난(難)](https://www.acmicpc.net/problem/14497) | 격자 | 친구 위치까지 점프 횟수의 최솟값. 번진 칸의 비용을 0/1로 모델링 |
| 5 | [백준 1584 게임](https://www.acmicpc.net/problem/1584) | 격자 | 위험 구역은 비용 1, 죽음 구역은 이동 불가. 직사각형 영역으로 격자를 먼저 만든다 |
| 6 | [LeetCode 1368 Minimum Cost to Make at Least One Valid Path in a Grid](https://leetcode.com/problems/minimum-cost-to-make-at-least-one-valid-path-in-a-grid/) | 방향 비용 | 칸의 화살표 방향으로 가면 비용 0, 다른 방향은 1(화살표를 바꾼다) |

## 풀이 메모

- 1번과 2번은 같은 문제입니다. 먼저 [다익스트라](../dijkstra/)로 풀고 0-1 BFS로 바꿔서 같은 답이 나오는지, 시간이 줄어드는지 비교하세요.
- 3번은 정점이 `0..100000`의 수이고 이웃이 `x−1`, `x+1`, `2x`입니다. `2x`는 비용 0이므로 `appendleft`입니다. 범위 검사를 빠뜨리지 마세요.
- 5번처럼 "구역"이 직사각형으로 주어지면 격자 배열에 먼저 표시한 뒤 탐색합니다.
- 6번은 칸의 정점마다 네 방향 간선이 있고, 화살표와 같은 방향이 가중치 0, 나머지 세 방향이 1입니다.
