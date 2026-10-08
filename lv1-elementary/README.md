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
| [Stack (스택)](01-data-structures/stack/) | `done` | push·pop O(1) | [array](../lv0-basics/01-data-structures/array/) |
| [Queue (큐)](01-data-structures/queue/) | `done` | enqueue·dequeue O(1) | [array](../lv0-basics/01-data-structures/array/) |
| [Deque (덱, Double-ended Queue)](01-data-structures/deque/) | `done` | 양끝 push·pop O(1) | [queue](01-data-structures/queue/), [stack](01-data-structures/stack/) |
| [Linked List (연결 리스트)](01-data-structures/linked-list/) | `done` | 앞에 삽입 O(1), 탐색 O(n) | [array](../lv0-basics/01-data-structures/array/) |
| [Hash Table (해시 테이블)](01-data-structures/hash-table/) | `done` | 평균 O(1), 최악 O(n) | [array](../lv0-basics/01-data-structures/array/) |
| [Priority Queue (우선순위 큐)와 힙](01-data-structures/priority-queue/) | `done` | push·pop O(log n), 최솟값 보기 O(1) | [queue](01-data-structures/queue/) |
| [Set and Dict (집합과 딕셔너리 활용)](01-data-structures/set-and-dict/) | `done` | 평균 O(1) 연산 | [hash-table](01-data-structures/hash-table/) |

### [정렬 (Sorting)](02-sorting/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Bubble Sort (버블 정렬)](02-sorting/bubble-sort/) | `done` | 최악 O(n^2), 이미 정렬되어 있으면 O(n) | [array](../lv0-basics/01-data-structures/array/) |
| [Selection Sort (선택 정렬)](02-sorting/selection-sort/) | `done` | O(n^2) | [array](../lv0-basics/01-data-structures/array/) |
| [Insertion Sort (삽입 정렬)](02-sorting/insertion-sort/) | `done` | 최악 O(n^2), 이미 정렬되어 있으면 O(n) | [array](../lv0-basics/01-data-structures/array/) |
| [Merge Sort (병합 정렬)](02-sorting/merge-sort/) | `done` | O(n log n) | [array](../lv0-basics/01-data-structures/array/) |
| [Quick Sort (퀵 정렬)](02-sorting/quick-sort/) | `done` | 평균 O(n log n), 최악 O(n^2) | [array](../lv0-basics/01-data-structures/array/) |
| [Heap Sort (힙 정렬)](02-sorting/heap-sort/) | `done` | O(n log n) | [priority-queue](01-data-structures/priority-queue/) |
| [Sorting in Practice (정렬 활용)](02-sorting/sort-with-key/) | `done` | 정렬 O(n log n), 계수 정렬 O(n + k) | [merge-sort](02-sorting/merge-sort/), [set-and-dict](01-data-structures/set-and-dict/) |

### [이분 탐색 (Binary Search)](03-binary-search/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Binary Search (이분 탐색)](03-binary-search/binary-search/) | `done` | O(log n) | [array](../lv0-basics/01-data-structures/array/) |
| [Lower Bound / Upper Bound (하한과 상한)](03-binary-search/lower-upper-bound/) | `done` | O(log n) | [binary-search](03-binary-search/binary-search/) |

### [구간 다루기 (Range Techniques)](04-range-techniques/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Prefix Sum (누적 합)](04-range-techniques/prefix-sum/) | `done` | 전처리 O(n), 구간 합 쿼리 O(1) | [array](../lv0-basics/01-data-structures/array/) |
| [Two-dimensional Prefix Sum (2차원 누적 합)](04-range-techniques/two-dimensional-prefix-sum/) | `done` | 전처리 O(R×C), 쿼리 O(1) | [prefix-sum](04-range-techniques/prefix-sum/), [two-dimensional-array](../lv0-basics/01-data-structures/two-dimensional-array/) |
| [Two Pointers (투 포인터)](04-range-techniques/two-pointers/) | `done` | O(n) | [array](../lv0-basics/01-data-structures/array/) |

### [그래프 기초 (Graph Basics)](05-graph-basics/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Graph (그래프)](05-graph-basics/graph/) | `done` | 표현에 따라 다름 (표 참고) | [array](../lv0-basics/01-data-structures/array/) |
| [Tree (트리)](05-graph-basics/tree/) | `done` | O(V) | [graph](05-graph-basics/graph/) |
| [DFS (Depth-First Search, 깊이 우선 탐색)](05-graph-basics/dfs/) | `done` | O(V+E) | [graph](05-graph-basics/graph/), [stack](01-data-structures/stack/) |
| [BFS (Breadth-First Search, 너비 우선 탐색)](05-graph-basics/bfs/) | `done` | O(V+E) | [graph](05-graph-basics/graph/), [queue](01-data-structures/queue/) |
| [Tree Traversal (트리 순회)](05-graph-basics/tree-traversal/) | `done` | O(n) | [tree](05-graph-basics/tree/), [dfs](05-graph-basics/dfs/) |
| [Grid Search (격자 탐색)](05-graph-basics/grid-search/) | `done` | O(행 × 열) | [two-dimensional-array](../lv0-basics/01-data-structures/two-dimensional-array/), [dfs](05-graph-basics/dfs/), [bfs](05-graph-basics/bfs/) |
| [Connected Components (연결 요소)](05-graph-basics/connected-components/) | `done` | O(V+E) | [dfs](05-graph-basics/dfs/), [bfs](05-graph-basics/bfs/) |

### [정수론 기초 (Number Theory)](06-number-theory/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Euclidean Algorithm (유클리드 호제법)](06-number-theory/euclidean-algorithm/) | `done` | O(log min(a, b)) | [divisors-and-multiples](../lv0-basics/02-number-theory/divisors-and-multiples/), [modular-arithmetic](../lv0-basics/02-number-theory/modular-arithmetic/) |
| [Relatively Prime (서로소, Coprime)](06-number-theory/relatively-prime/) | `done` | O(log min(a, b)) | [euclidean-algorithm](06-number-theory/euclidean-algorithm/) |
| [Sieve of Eratosthenes (에라토스테네스의 체)](06-number-theory/sieve-of-eratosthenes/) | `done` | O(n log log n) | [naive-prime-check](../lv0-basics/02-number-theory/naive-prime-check/) |
| [Prime Factorization (소인수분해)](06-number-theory/prime-factorization/) | `done` | O(√n) | [naive-prime-check](../lv0-basics/02-number-theory/naive-prime-check/), [sieve-of-eratosthenes](06-number-theory/sieve-of-eratosthenes/) |
| [Divisor Sieve (약수 체)](06-number-theory/divisor-sieve/) | `done` | O(n log n) | [divisors-and-multiples](../lv0-basics/02-number-theory/divisors-and-multiples/), [sieve-of-eratosthenes](06-number-theory/sieve-of-eratosthenes/) |

### [알고리즘 설계 기법 (Paradigms)](07-algorithm-paradigms/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Greedy Algorithm (그리디 알고리즘, 탐욕적 기법)](07-algorithm-paradigms/greedy/) | `done` | O(n log n) | [sort-with-key](02-sorting/sort-with-key/) |
| [Backtracking (백트래킹)](07-algorithm-paradigms/backtracking/) | `done` | O(경우의 수, 가지치기로 줄어듦) | [brute-force](../lv0-basics/03-brute-force/brute-force/), [dfs](05-graph-basics/dfs/), [recursion-basics](../lv0-basics/06-recursion/recursion-basics/) |
| [Dynamic Programming (다이나믹 프로그래밍, 동적 계획법)](07-algorithm-paradigms/dynamic-programming/) | `done` | O(상태 수 × 전이 수) | [array](../lv0-basics/01-data-structures/array/), [recursion-basics](../lv0-basics/06-recursion/recursion-basics/), [brute-force](../lv0-basics/03-brute-force/brute-force/) |
| [Greedy Patterns (대표 그리디 유형)](07-algorithm-paradigms/greedy-patterns/) | `done` | O(n log n) | [greedy](07-algorithm-paradigms/greedy/), [priority-queue](01-data-structures/priority-queue/), [stack](01-data-structures/stack/) |
| [DP Practice (1차원·2차원 DP 연습)](07-algorithm-paradigms/dp-practice/) | `done` | O(n) ~ O(n²) | [dynamic-programming](07-algorithm-paradigms/dynamic-programming/) |

### [재귀 (Recursion)](08-recursion/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Tower of Hanoi (하노이의 탑)](08-recursion/tower-of-hanoi/) | `done` | O(2^n) | [recursion-basics](../lv0-basics/06-recursion/recursion-basics/) |

### [비트 연산 (Bit Manipulation)](09-bit-manipulation/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Bitwise Operators (비트 연산자)](09-bit-manipulation/bitwise-operators/) | `done` | O(1) | [base-conversion](../lv0-basics/02-number-theory/base-conversion/) |
| [Bitmask (비트마스킹)](09-bit-manipulation/bitmask/) | `done` | O(2ⁿ) | [bitwise-operators](09-bit-manipulation/bitwise-operators/), [brute-force](../lv0-basics/03-brute-force/brute-force/) |
<!-- INDEX:END -->

이 레벨에서 다룰 예정인 주제는 [ROADMAP](../ROADMAP.md)에서 볼 수 있습니다.
