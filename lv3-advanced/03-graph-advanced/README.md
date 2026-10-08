# 고급 그래프 (Advanced Graph)

Lv2의 그래프 알고리즘(최단 경로, 유니온 파인드, 위상 정렬, MST)을 넘어, **트리의 조상 관계, 방향 그래프의 순환 구조, 무방향 그래프의 약한 고리, 용량이 있는 흐름, 이분 그래프의 짝짓기**를 다룹니다. 모두 DFS/BFS 한두 번으로 구조를 파악한다는 공통점이 있습니다.

## 한눈에 비교

| 개념 | 대상 | 구하는 것 | 시간 |
|---|---|---|---|
| [LCA](lca/) | 루트 있는 트리 | 두 정점의 가장 깊은 공통 조상, 거리, `k`번째 조상 | 구축 O(n log n), 질의 O(log n) 또는 O(1) |
| [SCC](scc/) | 방향 그래프 | 서로 오갈 수 있는 정점의 묶음, 축약 DAG | O(V + E) |
| [2-SAT](two-sat/) | 논리식 (절당 2개의 리터럴) | 만족하는 값 배정 | O(N + M) |
| [단절점과 단절선](articulation-and-bridges/) | 무방향 그래프 | 지우면 쪼개지는 정점·간선 | O(V + E) |
| [디닉 (네트워크 플로우)](dinic/) | 용량 있는 방향 그래프 | 최대 유량 = 최소 컷 | O(V²E) (실제로는 훨씬 빠름) |
| [이분 매칭](bipartite-matching/) | 이분 그래프 | 최대 매칭, 최소 정점 덮개, DAG 경로 덮개 | 쿠온 O(VE), 호프크로프트-카프 O(E√V) |

## 문제 신호로 고르기

| 문제의 신호 | 선택 |
|---|---|
| 트리에서 "두 정점의 공통 조상", "두 정점 사이 거리/경로" | [LCA](lca/) |
| 방향 그래프에서 "서로 오갈 수 있는 그룹", "최소 몇 개를 시작점으로", "간선을 몇 개 더하면 강하게 연결" | [SCC](scc/) |
| "각 항목이 두 선택지 중 하나, 쌍마다 제약" | [2-SAT](two-sat/) (SCC로 판정) |
| "도로/노드 하나가 끊기면 둘로 쪼개지는가" | [단절점과 단절선](articulation-and-bridges/) |
| "용량이 있고 `s`에서 `t`로 최대 얼마를", "최소 비용으로 끊기", "서로소 경로의 최대 개수" | [디닉](dinic/) |
| "한쪽 원소를 다른 쪽 원소에 하나씩 배정", "격자에서 서로 영향 없는 최대 개수" | [이분 매칭](bipartite-matching/) |

## 개념 사이의 관계

- [2-SAT](two-sat/)은 [SCC](scc/)의 응용입니다. 함의 그래프의 SCC로 판정합니다.
- 단절점·단절선은 무방향 그래프의 DFS 트리와 `low`로, SCC는 방향 그래프의 DFS와 `low`로 풉니다. 같은 `low` 개념의 두 가지 쓰임입니다.
- [이분 매칭](bipartite-matching/)은 용량이 모두 1인 [디닉](dinic/)의 특수한 경우이고, 전용 알고리즘이 더 빠릅니다. 최대 매칭 = 최소 정점 덮개(쾨니그)는 최대 유량 = 최소 컷의 특수한 경우입니다.
- [LCA](lca/)의 이진 리프팅 표는 [희소 배열](../01-range-query-structures/sparse-table/)과 같은 "2의 거듭제곱 표" 아이디어입니다.

## 파이썬에서의 주의

- 정점이 10⁵개를 넘는 문제에서 **재귀 DFS는 깊이 제한(약 1000)**에 걸립니다. 이 단원의 모든 구현은 명시적 스택/큐를 씁니다.
- 입력이 크면 `sys.stdin.buffer.read().split()`로 한 번에 읽고 결과를 모아 한 번에 출력합니다.
- 이분 매칭은 쿠온이 입력에 따라 매우 느릴 수 있습니다 (같은 입력에서 618초 vs 1.4초, [README](bipartite-matching/README.md#5-복잡도와-입력-크기-가이드)). 호프크로프트-카프를 기본으로 쓰세요.

## 읽는 순서

1. [LCA](lca/): 트리 위에서 표를 만들어 점프하기
2. [SCC](scc/): 방향 그래프의 순환 구조
3. [2-SAT](two-sat/): SCC로 논리식 풀기
4. [단절점과 단절선](articulation-and-bridges/): `low` 값의 무방향 버전
5. [디닉](dinic/): 최대 유량과 최소 컷
6. [이분 매칭](bipartite-matching/): 특수한 흐름과 쾨니그의 정리

선행: [DFS/BFS](../../lv1-elementary/05-graph-basics/dfs/), [트리](../../lv1-elementary/05-graph-basics/tree/), [위상 정렬](../../lv2-intermediate/02-graph-algorithms/topological-sort/), [이분 그래프](../../lv2-intermediate/02-graph-algorithms/bipartite-graph/), [Union-Find](../../lv2-intermediate/02-graph-algorithms/union-find/). 이후: Lv4의 HLD, 센트로이드 분해, 최소 비용 최대 유량.
