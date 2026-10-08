---
level: 4
name: 최상급
tier: Diamond
summary: 트리 분해, 영속·고급 자료구조, FFT, 정수론 심화 등 대회 상위권 도구를 다룬다
---

# Lv4 · 최상급 (Diamond)

대회 상위권에서 쓰이는 도구를 다루는 단계입니다. 모든 개념에 파이썬 참고 구현과, 순진한 방법·전수 탐색과 비교하는 테스트가 있습니다. 대회 제한 시간을 맞추기 어려운 주제는 각 개념의 "복잡도와 입력 크기 가이드"에 이 환경에서 측정한 한계를 적었습니다.

- **solved.ac 기준**: Diamond 난이도의 문제 (알고리즘별 난이도는 문제에 따라 달라 대략적인 기준입니다)
- **선수 지식**: Lv3 내용
- **이 레벨을 마치면**: 고급 알고리즘의 아이디어와 적용 조건을 설명하고 참고 구현을 읽을 수 있다

## 개념 목록

<!-- INDEX:START -->
### [정수론 심화 (Advanced Number Theory)](01-number-theory/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [밀러-라빈 소수 판정법 (Miller–Rabin Primality Test)](01-number-theory/miller-rabin/) | `done` | O(k log³ n) | [fermat-little-theorem](../lv2-intermediate/06-number-theory/fermat-little-theorem/), [fast-exponentiation](../lv2-intermediate/05-divide-and-conquer/fast-exponentiation/) |
| [폴라드 로 (Pollard's rho)](01-number-theory/pollard-rho/) | `done` | 기대 O(n^(1/4)) (약수 하나) | [miller-rabin](01-number-theory/miller-rabin/), [euclidean-algorithm](../lv1-elementary/06-number-theory/euclidean-algorithm/) |
| [FFT / NTT (고속 푸리에 변환, 수론 변환)](01-number-theory/fft-ntt/) | `done` | O(n log n) | [fast-exponentiation](../lv2-intermediate/05-divide-and-conquer/fast-exponentiation/), [modular-inverse](../lv2-intermediate/06-number-theory/modular-inverse/), [divide-and-conquer](../lv2-intermediate/05-divide-and-conquer/divide-and-conquer/) |
| [뫼비우스 반전 (Möbius Inversion)](01-number-theory/mobius-inversion/) | `done` | 체 O(n), 변환 O(n log n), 서로소 쌍 O(√n) (메르텐스 표가 있을 때) | [euler-phi](../lv2-intermediate/06-number-theory/euler-phi/), [sieve-of-eratosthenes](../lv1-elementary/06-number-theory/sieve-of-eratosthenes/), [divisor-sieve](../lv1-elementary/06-number-theory/divisor-sieve/) |
| [뤼카 정리와 이항 계수의 일반화 (Lucas' Theorem)](01-number-theory/lucas-theorem/) | `done` | 소수 p: O(p + log_p n), 합성수 m: 소인수 p^e 마다 O(p^e + log n) | [ncr-mod](../lv2-intermediate/06-number-theory/ncr-mod/), [chinese-remainder-theorem](../lv3-advanced/02-number-theory/chinese-remainder-theorem/), [fermat-little-theorem](../lv2-intermediate/06-number-theory/fermat-little-theorem/) |
| [번사이드 보조정리 (Burnside's Lemma)](01-number-theory/burnside-lemma/) | `done` | 군의 원소 수 \|G\| × 자리 수 n (필요하면 약수만 O(d(n))) | [euler-phi](../lv2-intermediate/06-number-theory/euler-phi/), [permutations-and-combinations](../lv0-basics/03-brute-force/permutations-and-combinations/), [modular-inverse](../lv2-intermediate/06-number-theory/modular-inverse/) |

### [트리 분해 (Tree Decomposition)](02-tree-decomposition/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [헤비-라이트 분할 (Heavy-Light Decomposition, HLD)](02-tree-decomposition/heavy-light-decomposition/) | `done` | 전처리 O(n), 경로 질의 O(log² n) (구간 트리 사용 시), LCA O(log n) | [segment-tree](../lv3-advanced/01-range-query-structures/segment-tree/), [lazy-propagation](../lv3-advanced/01-range-query-structures/lazy-propagation/), [fenwick-tree](../lv3-advanced/01-range-query-structures/fenwick-tree/), [lca](../lv3-advanced/03-graph-advanced/lca/), [tree-dp](../lv2-intermediate/03-trees/tree-dp/) |
| [센트로이드 분해 (Centroid Decomposition)](02-tree-decomposition/centroid-decomposition/) | `done` | 분해 O(n log n), 거리 기반 쌍 세기 O(n log² n) (정렬) 또는 O(n log n) (해시), 질의·갱신 O(log n) | [tree-dp](../lv2-intermediate/03-trees/tree-dp/), [dfs](../lv1-elementary/05-graph-basics/dfs/), [bfs](../lv1-elementary/05-graph-basics/bfs/), [divide-and-conquer](../lv2-intermediate/05-divide-and-conquer/divide-and-conquer/), [two-pointers](../lv1-elementary/04-range-techniques/two-pointers/) |

### [고급 자료구조 (Advanced Data Structures)](03-advanced-data-structures/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [퍼시스턴트 세그먼트 트리 (Persistent Segment Tree)](03-advanced-data-structures/persistent-segment-tree/) | `done` | 갱신 O(log n), 질의 O(log n), 구간 k 번째 O(log n) | [segment-tree](../lv3-advanced/01-range-query-structures/segment-tree/), [coordinate-compression](../lv2-intermediate/08-search-techniques/coordinate-compression/), [prefix-sum](../lv1-elementary/04-range-techniques/prefix-sum/) |
| [머지 소트 트리 (Merge Sort Tree)](03-advanced-data-structures/merge-sort-tree/) | `done` | 준비 O(n log n), 질의 O(log² n), 갱신 O(n) (C 속도의 리스트 이동), 구간 k 번째 O(log³ n) | [segment-tree](../lv3-advanced/01-range-query-structures/segment-tree/), [binary-search](../lv1-elementary/03-binary-search/binary-search/), [lower-upper-bound](../lv1-elementary/03-binary-search/lower-upper-bound/), [sort-with-key](../lv1-elementary/02-sorting/sort-with-key/) |
| [웨이블릿 트리 (Wavelet Tree) / 웨이블릿 행렬 (Wavelet Matrix)](03-advanced-data-structures/wavelet-tree/) | `done` | 준비 O(n log σ), 질의 O(log σ) (σ = 서로 다른 값의 수) | [coordinate-compression](../lv2-intermediate/08-search-techniques/coordinate-compression/), [prefix-sum](../lv1-elementary/04-range-techniques/prefix-sum/), [bitwise-operators](../lv1-elementary/09-bit-manipulation/bitwise-operators/) |
| [리 차오 트리 심화 (Li Chao Tree: 선분·되돌리기·오프라인)](03-advanced-data-structures/li-chao-tree/) | `done` | 직선 추가·질의 O(log C), 선분 추가 O(log² C), 시간 구간이 있는 오프라인 O((L+Q) log Q log C) | [convex-hull-trick](../lv3-advanced/07-dp-advanced/convex-hull-trick/), [segment-tree](../lv3-advanced/01-range-query-structures/segment-tree/), [divide-and-conquer](../lv2-intermediate/05-divide-and-conquer/divide-and-conquer/) |
| [트립 (Treap)](03-advanced-data-structures/treap/) | `done` | split / merge / 삽입 / 삭제 / 구간 연산 기대 O(log n) | [binary-search-tree](../lv2-intermediate/03-trees/binary-search-tree/), [lazy-propagation](../lv3-advanced/01-range-query-structures/lazy-propagation/), [divide-and-conquer](../lv2-intermediate/05-divide-and-conquer/divide-and-conquer/) |
| [스플레이 트리 (Splay Tree)](03-advanced-data-structures/splay-tree/) | `done` | 분할 상환 O(log n) (한 번의 연산은 O(n)일 수 있다) | [binary-search-tree](../lv2-intermediate/03-trees/binary-search-tree/), [lazy-propagation](../lv3-advanced/01-range-query-structures/lazy-propagation/) |

### [흐름과 매칭 심화 (Flow & Matching)](04-flow-matching/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [최소 비용 최대 유량 (Min-Cost Max-Flow, MCMF)](04-flow-matching/min-cost-max-flow/) | `done` | O(F · E log V) (F = 증가 경로 횟수 ≤ 총 유량), SPFA는 O(F · VE) 최악 | [dinic](../lv3-advanced/03-graph-advanced/dinic/), [bellman-ford](../lv2-intermediate/01-shortest-path/bellman-ford/), [dijkstra](../lv2-intermediate/01-shortest-path/dijkstra/), [bipartite-matching](../lv3-advanced/03-graph-advanced/bipartite-matching/) |
| [헝가리안 알고리즘 (Hungarian Algorithm)](04-flow-matching/hungarian-algorithm/) | `done` | O(n² m) (n ≤ m, 행렬이 꽉 찬 경우), 정사각 O(n³) | [bipartite-matching](../lv3-advanced/03-graph-advanced/bipartite-matching/), [dijkstra](../lv2-intermediate/01-shortest-path/dijkstra/), [min-cost-max-flow](04-flow-matching/min-cost-max-flow/) |

### [문자열 심화 (Advanced Strings)](05-strings/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [접미사 자동자 (Suffix Automaton)](05-strings/suffix-automaton/) | `done` | 만들기 O(n) (알파벳 크기 상수), 부분 문자열 포함·횟수 질의 O(\|패턴\|) | [trie](../lv2-intermediate/07-strings/trie/), [kmp](../lv2-intermediate/07-strings/kmp/), [suffix-array-lcp](../lv3-advanced/05-strings-advanced/suffix-array-lcp/) |

### [기타 고급 기법 (Misc)](06-misc/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [키타마사 (Kitamasa) — 선형 점화식의 n 번째 항](06-misc/kitamasa/) | `done` | O(k² log n) (k = 점화식의 차수), 행렬 거듭제곱은 O(k³ log n) | [matrix-exponentiation](../lv3-advanced/07-dp-advanced/matrix-exponentiation/), [fast-exponentiation](../lv2-intermediate/05-divide-and-conquer/fast-exponentiation/) |
| [스프라그-그런디 정리 (Sprague–Grundy Theorem)](06-misc/sprague-grundy/) | `done` | 그런디 표 O(n · 수의 개수) (뺄셈 게임), 8진 게임 O(n²), 합의 승패는 O(성분 수) | [bitwise-operators](../lv1-elementary/09-bit-manipulation/bitwise-operators/), [dynamic-programming](../lv1-elementary/07-algorithm-paradigms/dynamic-programming/) |
| [에일리언 트릭 (Aliens trick, WQS 이분 탐색)](06-misc/aliens-trick/) | `done` | O(T · log C) (T = 벌점이 있는 완화 문제를 한 번 푸는 시간, C = 벌점의 탐색 범위) | [parametric-search](../lv2-intermediate/08-search-techniques/parametric-search/), [convex-hull-trick](../lv3-advanced/07-dp-advanced/convex-hull-trick/), [dynamic-programming](../lv1-elementary/07-algorithm-paradigms/dynamic-programming/) |
| [반평면 교집합 (Half-Plane Intersection)](06-misc/half-plane-intersection/) | `done` | O(n log n) (각도 정렬이 지배), 정렬된 입력이면 O(n) | [ccw](../lv3-advanced/04-geometry/ccw/), [convex-hull](../lv3-advanced/04-geometry/convex-hull/), [segment-intersection](../lv3-advanced/04-geometry/segment-intersection/) |
<!-- INDEX:END -->

전체 커리큘럼과 개념 사이의 선행 관계는 [ROADMAP](../ROADMAP.md)에서 볼 수 있습니다.
