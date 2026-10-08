---
level: 1
name: 기초
tier: Silver
summary: 기본 자료구조와 정렬·탐색, DFS/BFS, DP·그리디 입문을 익힌다
---

# Lv1 · 기초 (Silver)

거의 모든 문제에서 쓰이는 도구를 갖추는 단계입니다. 자료구조를 상황에 맞게 고르고, 탐색과 정렬, 간단한 DP·그리디로 문제를 풀 수 있게 됩니다.

- **solved.ac 기준**: Silver 난이도의 문제 (알고리즘별 난이도는 문제에 따라 달라 대략적인 기준입니다)
- **선수 지식**: Lv0 내용, 시간 복잡도 읽는 법
- **이 레벨을 마치면**: 자료구조를 골라 쓰고, 이분 탐색·DFS/BFS·누적 합·간단한 DP로 풀리는 문제를 알아볼 수 있다

## 개념 목록

<!-- INDEX:START -->
### [기본 자료구조 (Data Structures)](01-data-structures/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Stack (스택)](01-data-structures/stack/) | `stub` | push·pop O(1) | [array](../lv0-basics/01-data-structures/array/) |
| [Queue (큐)](01-data-structures/queue/) | `stub` | push·pop O(1) | [array](../lv0-basics/01-data-structures/array/) |
| [Deque (Double-ended Queue, 덱, 쌍방향 큐)](01-data-structures/deque/) | `stub` | 양끝 push·pop O(1) | [queue](01-data-structures/queue/), [stack](01-data-structures/stack/) |
| [Linked List (연결 리스트)](01-data-structures/linked-list/) | `migrated` | 삽입·삭제 O(1)(위치를 안다면), 탐색 O(n) | [array](../lv0-basics/01-data-structures/array/) |
| [Hash Table (해시 테이블)](01-data-structures/hash-table/) | `stub` | 평균 O(1), 최악 O(n) | [array](../lv0-basics/01-data-structures/array/) |
| [Priority Queue (우선순위 큐)](01-data-structures/priority-queue/) | `stub` | push·pop O(log n) | [queue](01-data-structures/queue/) |

### [정렬 (Sorting)](02-sorting/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Bubble Sort (버블 정렬)](02-sorting/bubble-sort/) | `done` | 최악 O(n^2), 이미 정렬되어 있으면 O(n) | [array](../lv0-basics/01-data-structures/array/) |
| [Selection Sort (선택 정렬)](02-sorting/selection-sort/) | `done` | O(n^2) | [array](../lv0-basics/01-data-structures/array/) |
| [Insertion Sort (삽입 정렬)](02-sorting/insertion-sort/) | `done` | 최악 O(n^2), 이미 정렬되어 있으면 O(n) | [array](../lv0-basics/01-data-structures/array/) |
| [Merge Sort (병합 정렬)](02-sorting/merge-sort/) | `done` | O(n log n) | [array](../lv0-basics/01-data-structures/array/) |
| [Quick Sort (퀵 정렬)](02-sorting/quick-sort/) | `done` | 평균 O(n log n), 최악 O(n^2) | [array](../lv0-basics/01-data-structures/array/) |
| [Heap Sort (힙 정렬)](02-sorting/heap-sort/) | `done` | O(n log n) | [priority-queue](01-data-structures/priority-queue/) |

### [이분 탐색 (Binary Search)](03-binary-search/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Binary Search (이진 탐색)](03-binary-search/binary-search/) | `migrated` | O(log n) | [array](../lv0-basics/01-data-structures/array/) |

### [구간 다루기 (Range Techniques)](04-range-techniques/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Prefix Sum (구간 합)](04-range-techniques/prefix-sum/) | `migrated` | 전처리 O(n), 구간 합 쿼리 O(1) | [array](../lv0-basics/01-data-structures/array/) |

### [그래프 기초 (Graph Basics)](05-graph-basics/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Graph (그래프)](05-graph-basics/graph/) | `migrated` | - | [array](../lv0-basics/01-data-structures/array/) |
| [Tree (트리)](05-graph-basics/tree/) | `stub` | - | [graph](05-graph-basics/graph/) |
| [DFS (Depth-First Search, 깊이 우선 탐색)](05-graph-basics/dfs/) | `migrated` | O(V+E) | [graph](05-graph-basics/graph/), [stack](01-data-structures/stack/) |
| [BFS (Breadth-First Search, 너비 우선 탐색)](05-graph-basics/bfs/) | `migrated` | O(V+E) | [graph](05-graph-basics/graph/), [queue](01-data-structures/queue/) |
| [Tree Traversal (트리 순회)](05-graph-basics/tree-traversal/) | `migrated` | O(n) | [tree](05-graph-basics/tree/), [dfs](05-graph-basics/dfs/) |

### [정수론 기초 (Number Theory)](06-number-theory/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Euclidean Algorithm (유클리드 호제법)](06-number-theory/euclidean-algorithm/) | `migrated` | O(log min(a, b)) | - |
| [Relatively Prime (서로소, Coprime)](06-number-theory/relatively-prime/) | `migrated` | O(log min(a, b)) | [euclidean-algorithm](06-number-theory/euclidean-algorithm/) |
| [Sieve of Eratosthenes (에라토스테네스의 체)](06-number-theory/sieve-of-eratosthenes/) | `migrated` | O(n log log n) | [naive-prime-check](../lv0-basics/02-number-theory/naive-prime-check/) |
| [Prime Factorization (소인수분해)](06-number-theory/prime-factorization/) | `migrated` | O(√n) | [naive-prime-check](../lv0-basics/02-number-theory/naive-prime-check/) |

### [알고리즘 설계 기법 (Paradigms)](07-algorithm-paradigms/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Greedy Algorithm (그리디 알고리즘, 탐욕적 기법)](07-algorithm-paradigms/greedy/) | `migrated` | - | - |
| [Backtracking (백트래킹)](07-algorithm-paradigms/backtracking/) | `migrated` | - | [brute-force](../lv0-basics/03-brute-force/brute-force/), [dfs](05-graph-basics/dfs/) |
| [Dynamic Programming (다이나믹 프로그래밍, 동적 계획법)](07-algorithm-paradigms/dynamic-programming/) | `migrated` | - | [array](../lv0-basics/01-data-structures/array/), [brute-force](../lv0-basics/03-brute-force/brute-force/) |

### [재귀 (Recursion)](08-recursion/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Tower of Hanoi (하노이의 탑)](08-recursion/tower-of-hanoi/) | `migrated` | O(2^n) | - |

### [비트 연산 (Bit Manipulation)](09-bit-manipulation/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Bitwise Operators (비트 연산자)](09-bit-manipulation/bitwise-operators/) | `migrated` | - | - |
| [Bitmask (비트마스킹)](09-bit-manipulation/bitmask/) | `migrated` | - | [bitwise-operators](09-bit-manipulation/bitwise-operators/), [brute-force](../lv0-basics/03-brute-force/brute-force/) |
<!-- INDEX:END -->

이 레벨에서 다룰 예정인 주제는 [ROADMAP](../ROADMAP.md)에서 볼 수 있습니다.
