---
level: 2
name: 중급
tier: Gold
summary: 최단 경로·위상 정렬 같은 그래프 알고리즘과 DP 심화를 익힌다
---

# Lv2 · 중급 (Gold)

알고리즘 이름보다 "이 문제의 구조가 어떤 알고리즘에 대응하는가"를 알아보는 능력이 중요해지는 단계입니다. 그래프, DP, 정수론, 문자열의 대표 알고리즘을 다룹니다.

- **solved.ac 기준**: Gold 난이도의 문제 (알고리즘별 난이도는 문제에 따라 달라 대략적인 기준입니다)
- **선수 지식**: Lv1 내용 (특히 그래프 탐색, 우선순위 큐, DP 기초)
- **이 레벨을 마치면**: 문제의 조건에서 알고리즘을 골라 제한 시간 안에 구현할 수 있다

## 개념 목록

<!-- INDEX:START -->
### [최단 경로 (Shortest Path)](01-shortest-path/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Dijkstra's Algorithm (다익스트라 알고리즘)](01-shortest-path/dijkstra/) | `done` | O((V+E) log V) | [bfs](../lv1-elementary/05-graph-basics/bfs/), [priority-queue](../lv1-elementary/01-data-structures/priority-queue/) |
| [Bellman-Ford Algorithm (벨만-포드 알고리즘)](01-shortest-path/bellman-ford/) | `migrated` | O(VE) | [graph](../lv1-elementary/05-graph-basics/graph/) |
| [Floyd-Warshall Algorithm (플로이드-워셜 알고리즘)](01-shortest-path/floyd-warshall/) | `migrated` | O(V^3) | [graph](../lv1-elementary/05-graph-basics/graph/) |
| [0-1 BFS (0-1 너비 우선 탐색)](01-shortest-path/zero-one-bfs/) | `stub` | O(V+E) | [bfs](../lv1-elementary/05-graph-basics/bfs/), [deque](../lv1-elementary/01-data-structures/deque/) |

### [그래프 알고리즘 (Graph Algorithms)](02-graph-algorithms/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Union-Find (유니온 파인드, Disjoint Set - 서로소 집합)](02-graph-algorithms/union-find/) | `migrated` | 연산당 거의 O(1) (분할 상환 O(α(n))) | [tree](../lv1-elementary/05-graph-basics/tree/) |
| [Topological Sort (위상 정렬)](02-graph-algorithms/topological-sort/) | `migrated` | O(V+E) | [graph](../lv1-elementary/05-graph-basics/graph/), [bfs](../lv1-elementary/05-graph-basics/bfs/) |

### [트리 (Trees)](03-trees/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Binary Search Tree (이진 탐색 트리)](03-trees/binary-search-tree/) | `stub` | 평균 O(log n), 최악 O(n) | [tree](../lv1-elementary/05-graph-basics/tree/), [binary-search](../lv1-elementary/03-binary-search/binary-search/) |

### [다이나믹 프로그래밍 (Dynamic Programming)](04-dynamic-programming/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Knapsack Problem (배낭 문제)](04-dynamic-programming/knapsack/) | `migrated` | O(NK) | [dynamic-programming](../lv1-elementary/07-algorithm-paradigms/dynamic-programming/) |

### [분할 정복 (Divide and Conquer)](05-divide-and-conquer/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Divide and Conquer (분할 정복)](05-divide-and-conquer/divide-and-conquer/) | `migrated` | - | [tower-of-hanoi](../lv1-elementary/08-recursion/tower-of-hanoi/), [merge-sort](../lv1-elementary/02-sorting/merge-sort/) |

### [정수론 (Number Theory)](06-number-theory/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Euler's Phi Function (오일러 피 함수, Euler's Totient Function)](06-number-theory/euler-phi/) | `migrated` | O(√n) | [prime-factorization](../lv1-elementary/06-number-theory/prime-factorization/), [relatively-prime](../lv1-elementary/06-number-theory/relatively-prime/) |
| [Fermat's Little Theorem (페르마의 소정리)](06-number-theory/fermat-little-theorem/) | `migrated` | - | [euclidean-algorithm](../lv1-elementary/06-number-theory/euclidean-algorithm/), [relatively-prime](../lv1-elementary/06-number-theory/relatively-prime/) |

### [문자열 (Strings)](07-strings/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [KMP Algorithm (KMP 알고리즘)](07-strings/kmp/) | `migrated` | O(n+m) | - |
| [Rabin-Karp Algorithm (라빈-카프 알고리즘)](07-strings/rabin-karp/) | `stub` | 평균 O(n+m), 최악 O(nm) | [hash-table](../lv1-elementary/01-data-structures/hash-table/) |
<!-- INDEX:END -->

이 레벨에서 다룰 예정인 주제는 [ROADMAP](../ROADMAP.md)에서 볼 수 있습니다.
