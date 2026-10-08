# 연습문제 — 단절점과 단절선

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [AtCoder ABC075 C - Bridge](https://atcoder.jp/contests/abc075/tasks/abc075_c) | 단절선의 수 | 정점 50개라 간선을 하나씩 지워 보는 완전탐색도 되지만 `find_cut_vertices_and_bridges`로 풀어 보자 |
| 2 | [백준 11400 단절선](https://www.acmicpc.net/problem/11400) | 기본형 | 단절선의 수와 목록(각 간선은 작은 번호가 앞, 전체는 사전순). [solution.py](solution.py)의 `main()`이 같은 형태 |
| 3 | [백준 11266 단절점](https://www.acmicpc.net/problem/11266) | 기본형 | 단절점의 수와 목록. 루트는 자식이 둘 이상일 때만 단절점 |
| 4 | [LeetCode 1192 Critical Connections in a Network](https://leetcode.com/problems/critical-connections-in-a-network/) | 단절선 | `n ≤ 10⁵`. 재귀 DFS는 파이썬에서 깊이 제한에 걸리니 반복문 구현이 필요 |
| 5 | [Codeforces 118E Bertown roads](https://codeforces.com/problemset/problem/118/E) | 방향 부여 | 단절선이 있으면 불가능, 없으면 DFS 트리의 간선은 내려가는 방향, 역방향 간선은 올라가는 방향으로 |

## 풀이 메모

- 1번, 2번은 평행 간선이 입력에 있을 수 있는지 확인해야 합니다. 간선 번호로 부모 간선을 건너뛰는 구현([README](README.md#2-핵심-아이디어))은 평행 간선에도 맞습니다. [테스트](test_solution.py)가 자기 루프와 평행 간선이 섞인 무작위 그래프에서 모든 정점과 간선을 하나씩 지워 본 결과와 비교합니다.
- 3번은 `find_cut_vertices_and_bridges(n, edges)[0]`이 그대로 답입니다. 정점 번호가 1부터이면 읽고 쓸 때 바꿔 주세요.
- 5번은 단절선이 하나라도 있으면 답이 없습니다. 먼저 `find_cut_vertices_and_bridges`로 단절선이 비었는지 확인하고, 그다음 DFS를 한 번 더 돌며 트리 간선은 내려가는 방향, 역방향 간선은 올라가는 방향으로 기록하면 됩니다.
