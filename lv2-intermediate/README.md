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
| [Bellman-Ford Algorithm (벨만-포드 알고리즘)](01-shortest-path/bellman-ford/) | `done` | O(VE) | [graph](../lv1-elementary/05-graph-basics/graph/) |
| [Floyd-Warshall Algorithm (플로이드-워셜 알고리즘)](01-shortest-path/floyd-warshall/) | `done` | O(V³) | [graph](../lv1-elementary/05-graph-basics/graph/), [dynamic-programming](../lv1-elementary/07-algorithm-paradigms/dynamic-programming/) |
| [0-1 BFS (0-1 너비 우선 탐색)](01-shortest-path/zero-one-bfs/) | `done` | O(V+E) | [bfs](../lv1-elementary/05-graph-basics/bfs/), [deque](../lv1-elementary/01-data-structures/deque/) |

### [그래프 알고리즘 (Graph Algorithms)](02-graph-algorithms/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Union-Find (유니온 파인드, Disjoint Set - 서로소 집합)](02-graph-algorithms/union-find/) | `done` | 연산당 거의 O(1) (분할 상환 O(α(n))) | [tree](../lv1-elementary/05-graph-basics/tree/), [array](../lv0-basics/01-data-structures/array/) |
| [Topological Sort (위상 정렬)](02-graph-algorithms/topological-sort/) | `done` | O(V+E) | [graph](../lv1-elementary/05-graph-basics/graph/), [bfs](../lv1-elementary/05-graph-basics/bfs/) |
| [Kruskal's Algorithm (크루스칼 알고리즘, 최소 스패닝 트리)](02-graph-algorithms/kruskal/) | `done` | O(E log E) | [union-find](02-graph-algorithms/union-find/), [sort-with-key](../lv1-elementary/02-sorting/sort-with-key/), [greedy](../lv1-elementary/07-algorithm-paradigms/greedy/) |
| [Prim's Algorithm (프림 알고리즘, 최소 스패닝 트리)](02-graph-algorithms/prim/) | `done` | O(E log V) | [priority-queue](../lv1-elementary/01-data-structures/priority-queue/), [graph](../lv1-elementary/05-graph-basics/graph/) |
| [Bipartite Graph (이분 그래프)](02-graph-algorithms/bipartite-graph/) | `done` | O(V+E) | [bfs](../lv1-elementary/05-graph-basics/bfs/), [connected-components](../lv1-elementary/05-graph-basics/connected-components/) |

### [트리 (Trees)](03-trees/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Binary Search Tree (이진 탐색 트리)](03-trees/binary-search-tree/) | `done` | 평균 O(log n), 최악 O(n) | [tree](../lv1-elementary/05-graph-basics/tree/), [binary-search](../lv1-elementary/03-binary-search/binary-search/), [tree-traversal](../lv1-elementary/05-graph-basics/tree-traversal/) |
| [Tree DP (트리 DP)](03-trees/tree-dp/) | `done` | O(n) | [tree](../lv1-elementary/05-graph-basics/tree/), [dynamic-programming](../lv1-elementary/07-algorithm-paradigms/dynamic-programming/), [dp-practice](../lv1-elementary/07-algorithm-paradigms/dp-practice/) |
| [Tree Diameter (트리의 지름)](03-trees/tree-diameter/) | `done` | O(n) | [tree](../lv1-elementary/05-graph-basics/tree/), [bfs](../lv1-elementary/05-graph-basics/bfs/) |

### [다이나믹 프로그래밍 (Dynamic Programming)](04-dynamic-programming/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Knapsack Problem (배낭 문제)](04-dynamic-programming/knapsack/) | `done` | O(NK) | [dynamic-programming](../lv1-elementary/07-algorithm-paradigms/dynamic-programming/), [dp-practice](../lv1-elementary/07-algorithm-paradigms/dp-practice/), [greedy](../lv1-elementary/07-algorithm-paradigms/greedy/) |
| [LIS (가장 긴 증가하는 부분 수열)](04-dynamic-programming/lis/) | `done` | O(n log n) | [dp-practice](../lv1-elementary/07-algorithm-paradigms/dp-practice/), [binary-search](../lv1-elementary/03-binary-search/binary-search/), [lower-upper-bound](../lv1-elementary/03-binary-search/lower-upper-bound/) |
| [LCS (최장 공통 부분 수열)와 편집 거리](04-dynamic-programming/lcs/) | `done` | O(nm) | [dp-practice](../lv1-elementary/07-algorithm-paradigms/dp-practice/), [string-basics](../lv0-basics/01-data-structures/string-basics/) |
| [Interval DP (구간 DP)](04-dynamic-programming/interval-dp/) | `done` | O(n³) | [dp-practice](../lv1-elementary/07-algorithm-paradigms/dp-practice/), [prefix-sum](../lv1-elementary/04-range-techniques/prefix-sum/) |
| [Bitmask DP (비트마스크 DP)](04-dynamic-programming/bitmask-dp/) | `done` | O(2ⁿ·n²) | [bitmask](../lv1-elementary/09-bit-manipulation/bitmask/), [dp-practice](../lv1-elementary/07-algorithm-paradigms/dp-practice/) |

### [분할 정복 (Divide and Conquer)](05-divide-and-conquer/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Divide and Conquer (분할 정복)](05-divide-and-conquer/divide-and-conquer/) | `done` | O(n log n) (문제마다 다름) | [tower-of-hanoi](../lv1-elementary/08-recursion/tower-of-hanoi/), [merge-sort](../lv1-elementary/02-sorting/merge-sort/), [recursion-basics](../lv0-basics/06-recursion/recursion-basics/) |
| [Fast Exponentiation (빠른 거듭제곱)](05-divide-and-conquer/fast-exponentiation/) | `done` | O(log b) | [divide-and-conquer](05-divide-and-conquer/divide-and-conquer/), [modular-arithmetic](../lv0-basics/02-number-theory/modular-arithmetic/), [bitwise-operators](../lv1-elementary/09-bit-manipulation/bitwise-operators/) |

### [정수론 (Number Theory)](06-number-theory/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Euler's Phi Function (오일러 피 함수, Euler's Totient Function)](06-number-theory/euler-phi/) | `done` | O(√n) | [prime-factorization](../lv1-elementary/06-number-theory/prime-factorization/), [relatively-prime](../lv1-elementary/06-number-theory/relatively-prime/), [sieve-of-eratosthenes](../lv1-elementary/06-number-theory/sieve-of-eratosthenes/) |
| [Fermat's Little Theorem (페르마의 소정리)](06-number-theory/fermat-little-theorem/) | `done` | O(log p) | [fast-exponentiation](05-divide-and-conquer/fast-exponentiation/), [modular-arithmetic](../lv0-basics/02-number-theory/modular-arithmetic/), [relatively-prime](../lv1-elementary/06-number-theory/relatively-prime/) |
| [Modular Inverse (모듈러 역원)](06-number-theory/modular-inverse/) | `done` | O(log m) | [fermat-little-theorem](06-number-theory/fermat-little-theorem/), [euler-phi](06-number-theory/euler-phi/), [euclidean-algorithm](../lv1-elementary/06-number-theory/euclidean-algorithm/), [modular-arithmetic](../lv0-basics/02-number-theory/modular-arithmetic/) |
| [nCr mod p (조합 mod 소수)](06-number-theory/ncr-mod/) | `done` | 전처리 O(n), 질의 O(1) | [modular-inverse](06-number-theory/modular-inverse/), [fermat-little-theorem](06-number-theory/fermat-little-theorem/), [fast-exponentiation](05-divide-and-conquer/fast-exponentiation/), [permutations-and-combinations](../lv0-basics/03-brute-force/permutations-and-combinations/) |

### [문자열 (Strings)](07-strings/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [KMP Algorithm (KMP 알고리즘)](07-strings/kmp/) | `done` | O(n+m) | [string-basics](../lv0-basics/01-data-structures/string-basics/), [time-complexity](../lv0-basics/04-io-and-complexity/time-complexity/) |
| [Rabin-Karp Algorithm (라빈-카프 알고리즘)](07-strings/rabin-karp/) | `done` | 평균 O(n+m), 최악 O(nm) | [hash-table](../lv1-elementary/01-data-structures/hash-table/), [modular-arithmetic](../lv0-basics/02-number-theory/modular-arithmetic/), [binary-search](../lv1-elementary/03-binary-search/binary-search/) |
| [Trie (트라이, 접두사 트리)](07-strings/trie/) | `done` | 삽입·질의 O(L) | [tree](../lv1-elementary/05-graph-basics/tree/), [hash-table](../lv1-elementary/01-data-structures/hash-table/), [set-and-dict](../lv1-elementary/01-data-structures/set-and-dict/) |

### [탐색 기법 (Search Techniques)](08-search-techniques/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Parametric Search (매개변수 탐색)](08-search-techniques/parametric-search/) | `done` | O(판정 비용 · log 범위) | [binary-search](../lv1-elementary/03-binary-search/binary-search/), [lower-upper-bound](../lv1-elementary/03-binary-search/lower-upper-bound/), [greedy](../lv1-elementary/07-algorithm-paradigms/greedy/) |
| [Monotonic Stack (모노톤 스택)](08-search-techniques/monotonic-stack/) | `done` | O(n) | [stack](../lv1-elementary/01-data-structures/stack/), [time-complexity](../lv0-basics/04-io-and-complexity/time-complexity/) |
| [Sliding Window (슬라이딩 윈도우)](08-search-techniques/sliding-window/) | `done` | O(n) | [two-pointers](../lv1-elementary/04-range-techniques/two-pointers/), [deque](../lv1-elementary/01-data-structures/deque/), [monotonic-stack](08-search-techniques/monotonic-stack/) |
| [Coordinate Compression (좌표 압축)](08-search-techniques/coordinate-compression/) | `done` | O(n log n) | [sort-with-key](../lv1-elementary/02-sorting/sort-with-key/), [lower-upper-bound](../lv1-elementary/03-binary-search/lower-upper-bound/), [set-and-dict](../lv1-elementary/01-data-structures/set-and-dict/) |
| [Sweep Line (스위핑)](08-search-techniques/sweeping/) | `done` | O(n log n) | [sort-with-key](../lv1-elementary/02-sorting/sort-with-key/), [priority-queue](../lv1-elementary/01-data-structures/priority-queue/), [coordinate-compression](08-search-techniques/coordinate-compression/) |
<!-- INDEX:END -->

전체 커리큘럼과 개념 사이의 선행 관계는 [ROADMAP](../ROADMAP.md)에서 볼 수 있습니다.
