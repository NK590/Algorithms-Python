---
level: 3
name: 고급
tier: Platinum
summary: 구간 질의 자료구조, 고급 그래프(SCC·플로우), 문자열·기하 도구를 익힌다
---

# Lv3 · 고급 (Platinum)

여러 알고리즘을 조합하거나 자료구조를 직접 설계해야 풀리는 문제들이 나오는 단계입니다. Python으로는 시간 제한이 빠듯해지므로 구현 최적화도 함께 다룹니다.

- **solved.ac 기준**: Platinum 난이도의 문제 (알고리즘별 난이도는 문제에 따라 달라 대략적인 기준입니다)
- **선수 지식**: Lv2 내용 (트리, 분할 정복, 모듈러 연산)
- **이 레벨을 마치면**: 세그먼트 트리 같은 자료구조를 직접 구현해 쿼리 문제를 풀 수 있다

## 개념 목록

<!-- INDEX:START -->
### [구간 질의 자료구조 (Range Query Structures)](01-range-query-structures/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Fenwick Tree (펜윅 트리, Binary Indexed Tree)](01-range-query-structures/fenwick-tree/) | `done` | 갱신·질의 O(log n) | [prefix-sum](../lv1-elementary/04-range-techniques/prefix-sum/), [bitwise-operators](../lv1-elementary/09-bit-manipulation/bitwise-operators/), [coordinate-compression](../lv2-intermediate/08-search-techniques/coordinate-compression/) |
| [Segment Tree (세그먼트 트리, 구간 트리)](01-range-query-structures/segment-tree/) | `done` | 구축 O(n), 질의·갱신 O(log n) | [tree](../lv1-elementary/05-graph-basics/tree/), [divide-and-conquer](../lv2-intermediate/05-divide-and-conquer/divide-and-conquer/), [prefix-sum](../lv1-elementary/04-range-techniques/prefix-sum/) |
| [Lazy Propagation (느리게 갱신되는 세그먼트 트리)](01-range-query-structures/lazy-propagation/) | `done` | 구간 갱신·구간 질의 O(log n) | [segment-tree](01-range-query-structures/segment-tree/), [recursion-basics](../lv0-basics/06-recursion/recursion-basics/) |
| [Sparse Table (희소 배열)](01-range-query-structures/sparse-table/) | `done` | 구축 O(n log n), 질의 O(1) | [segment-tree](01-range-query-structures/segment-tree/), [bitwise-operators](../lv1-elementary/09-bit-manipulation/bitwise-operators/), [dynamic-programming](../lv1-elementary/07-algorithm-paradigms/dynamic-programming/) |

### [정수론 (Number Theory)](02-number-theory/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Extended Euclidean Algorithm (확장 유클리드 호제법)](02-number-theory/extended-euclidean-algorithm/) | `done` | O(log min(a, b)) | [euclidean-algorithm](../lv1-elementary/06-number-theory/euclidean-algorithm/), [modular-inverse](../lv2-intermediate/06-number-theory/modular-inverse/) |
| [Chinese Remainder Theorem (중국인의 나머지 정리)](02-number-theory/chinese-remainder-theorem/) | `done` | 식 하나를 합치는 데 O(log m) | [extended-euclidean-algorithm](02-number-theory/extended-euclidean-algorithm/), [modular-inverse](../lv2-intermediate/06-number-theory/modular-inverse/) |

### [고급 그래프 (Advanced Graph)](03-graph-advanced/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [LCA (최소 공통 조상, Lowest Common Ancestor)](03-graph-advanced/lca/) | `done` | 구축 O(n log n), 질의 O(log n) 또는 O(1) | [tree](../lv1-elementary/05-graph-basics/tree/), [bfs](../lv1-elementary/05-graph-basics/bfs/), [sparse-table](01-range-query-structures/sparse-table/) |
| [SCC (강한 연결 요소, Strongly Connected Components)](03-graph-advanced/scc/) | `done` | O(V+E) | [dfs](../lv1-elementary/05-graph-basics/dfs/), [topological-sort](../lv2-intermediate/02-graph-algorithms/topological-sort/) |
| [2-SAT](03-graph-advanced/two-sat/) | `done` | O(N + M) | [scc](03-graph-advanced/scc/), [graph](../lv1-elementary/05-graph-basics/graph/) |
| [단절점과 단절선 (Articulation Points & Bridges)](03-graph-advanced/articulation-and-bridges/) | `done` | O(V+E) | [dfs](../lv1-elementary/05-graph-basics/dfs/), [scc](03-graph-advanced/scc/) |
| [Dinic's Algorithm (디닉 알고리즘, 네트워크 플로우)](03-graph-advanced/dinic/) | `done` | O(V²E) | [bfs](../lv1-elementary/05-graph-basics/bfs/), [dfs](../lv1-elementary/05-graph-basics/dfs/), [graph](../lv1-elementary/05-graph-basics/graph/) |
| [Bipartite Matching (이분 매칭)](03-graph-advanced/bipartite-matching/) | `done` | Kuhn O(VE), 호프크로프트-카프 O(E√V) | [dfs](../lv1-elementary/05-graph-basics/dfs/), [bfs](../lv1-elementary/05-graph-basics/bfs/), [bipartite-graph](../lv2-intermediate/02-graph-algorithms/bipartite-graph/) |

### [기하 (Geometry)](04-geometry/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [CCW (반시계 판정)와 외적](04-geometry/ccw/) | `done` | 판정 O(1), 다각형 O(n) | [time-complexity](../lv0-basics/04-io-and-complexity/time-complexity/), [sort-with-key](../lv1-elementary/02-sorting/sort-with-key/) |
| [선분 교차 (Segment Intersection)](04-geometry/segment-intersection/) | `done` | 한 쌍 O(1), 모든 쌍 O(n²) | [ccw](04-geometry/ccw/), [union-find](../lv2-intermediate/02-graph-algorithms/union-find/) |
| [Convex Hull (볼록 껍질)](04-geometry/convex-hull/) | `done` | O(n log n) | [ccw](04-geometry/ccw/), [sort-with-key](../lv1-elementary/02-sorting/sort-with-key/) |

### [고급 문자열 (Advanced Strings)](05-strings-advanced/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Z 알고리즘 (Z-algorithm)](05-strings-advanced/z-algorithm/) | `done` | O(n) | [kmp](../lv2-intermediate/07-strings/kmp/), [time-complexity](../lv0-basics/04-io-and-complexity/time-complexity/) |
| [매내처 알고리즘 (Manacher's Algorithm)](05-strings-advanced/manacher/) | `done` | O(n) | [z-algorithm](05-strings-advanced/z-algorithm/), [two-pointers](../lv1-elementary/04-range-techniques/two-pointers/), [time-complexity](../lv0-basics/04-io-and-complexity/time-complexity/) |
| [아호-코라식 (Aho-Corasick)](05-strings-advanced/aho-corasick/) | `done` | 구축 O(패턴 길이의 합), 탐색 O(본문 + 찾은 개수) | [trie](../lv2-intermediate/07-strings/trie/), [kmp](../lv2-intermediate/07-strings/kmp/) |
| [접미사 배열과 LCP 배열 (Suffix Array, LCP Array)](05-strings-advanced/suffix-array-lcp/) | `done` | 구축 O(n log² n) (이 구현), LCP O(n) | [z-algorithm](05-strings-advanced/z-algorithm/), [sort-with-key](../lv1-elementary/02-sorting/sort-with-key/), [sparse-table](01-range-query-structures/sparse-table/) |

### [쿼리 기법 (Query Techniques)](06-query-techniques/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [모스 알고리즘 (Mo's Algorithm)](06-query-techniques/mos-algorithm/) | `done` | O((n + q)√n) | [two-pointers](../lv1-elementary/04-range-techniques/two-pointers/), [sort-with-key](../lv1-elementary/02-sorting/sort-with-key/), [coordinate-compression](../lv2-intermediate/08-search-techniques/coordinate-compression/) |
| [제곱근 분할 (Sqrt Decomposition)](06-query-techniques/sqrt-decomposition/) | `done` | 질의·갱신 O(√n) | [prefix-sum](../lv1-elementary/04-range-techniques/prefix-sum/), [lower-upper-bound](../lv1-elementary/03-binary-search/lower-upper-bound/), [time-complexity](../lv0-basics/04-io-and-complexity/time-complexity/) |
| [중간에서 만나기 (Meet in the Middle)](06-query-techniques/meet-in-the-middle/) | `done` | O(2^(n/2) · n) | [bitmask](../lv1-elementary/09-bit-manipulation/bitmask/), [binary-search](../lv1-elementary/03-binary-search/binary-search/), [lower-upper-bound](../lv1-elementary/03-binary-search/lower-upper-bound/) |

### [고급 DP (Advanced DP)](07-dp-advanced/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [자릿수 DP (Digit DP)](07-dp-advanced/digit-dp/) | `done` | O(자릿수 × 상태 수 × 진법) | [dynamic-programming](../lv1-elementary/07-algorithm-paradigms/dynamic-programming/), [prefix-sum](../lv1-elementary/04-range-techniques/prefix-sum/) |
| [기댓값 DP (Expected Value DP)](07-dp-advanced/expected-value-dp/) | `done` | DAG 위 DP는 O(상태 수 × 전이 수), 연립방정식은 O(상태 수³) | [dynamic-programming](../lv1-elementary/07-algorithm-paradigms/dynamic-programming/), [modular-inverse](../lv2-intermediate/06-number-theory/modular-inverse/) |
| [분할 정복 최적화 (Divide and Conquer Optimization)](07-dp-advanced/divide-and-conquer-optimization/) | `done` | O(k n log n) | [dynamic-programming](../lv1-elementary/07-algorithm-paradigms/dynamic-programming/), [divide-and-conquer](../lv2-intermediate/05-divide-and-conquer/divide-and-conquer/), [prefix-sum](../lv1-elementary/04-range-techniques/prefix-sum/) |
| [볼록 껍질 트릭 (Convex Hull Trick, CHT)](07-dp-advanced/convex-hull-trick/) | `done` | O(n) 또는 O(n log n) | [dynamic-programming](../lv1-elementary/07-algorithm-paradigms/dynamic-programming/), [ccw](04-geometry/ccw/), [binary-search](../lv1-elementary/03-binary-search/binary-search/) |
| [행렬 거듭제곱 (Matrix Exponentiation)](07-dp-advanced/matrix-exponentiation/) | `done` | O(k³ log n) | [fast-exponentiation](../lv2-intermediate/05-divide-and-conquer/fast-exponentiation/), [dynamic-programming](../lv1-elementary/07-algorithm-paradigms/dynamic-programming/) |
<!-- INDEX:END -->

전체 커리큘럼과 개념 사이의 선행 관계는 [ROADMAP](../ROADMAP.md)에서 볼 수 있습니다.
