# 문제 신호 → 알고리즘 가이드

PS에서 어려운 부분은 구현보다 **"이 문제는 어떤 알고리즘으로 푸는 문제인가"를 알아보는 것**입니다. 문제 조건에 나오는 신호로 후보를 떠올려 보세요. 모든 항목은 이 저장소의 개념 문서로 연결됩니다. 어느 수준의 도구까지 필요한지는 개념 앞의 레벨(Lv0~Lv5)로 가늠할 수 있습니다.

## 풀기 전에

1. **입력 크기**를 보고 허용되는 복잡도를 가늠합니다. → [복잡도 치트시트](complexity-cheatsheet.md)
2. 작은 예제를 **손으로** 풀어 보고, 그 과정을 일반화할 수 있는지 봅니다.
3. 느리더라도 맞는 풀이(브루트 포스)를 먼저 떠올립니다. 나중에 최적화한 풀이를 검증하는 기준이 됩니다.
4. 경계 조건을 확인합니다. N = 1, 빈 입력, 최댓값, 음수, 중복, 이미 정렬된 입력.

## 신호별 후보

### 탐색 / 완전 탐색

| 문제의 신호 | 후보 |
|---|---|
| N이 작다 (N ≤ 10~20), 모든 경우를 확인해도 된다 | [브루트 포스](../lv0-basics/03-brute-force/brute-force/), [백트래킹](../lv1-elementary/07-algorithm-paradigms/backtracking/), [비트마스크](../lv1-elementary/09-bit-manipulation/bitmask/) |
| N ≤ 40이라 2^N은 크지만 2^(N/2)은 된다 | [중간에서 만나기](../lv3-advanced/06-query-techniques/meet-in-the-middle/) |
| 정렬된 데이터에서 값을 찾는다 | [이분 탐색](../lv1-elementary/03-binary-search/binary-search/), [lower/upper bound](../lv1-elementary/03-binary-search/lower-upper-bound/) |
| "조건을 만족하는 최솟값/최댓값"이고 답을 정하면 가능한지 판정할 수 있다 | [매개변수 탐색](../lv2-intermediate/08-search-techniques/parametric-search/) |
| 격자·그래프에서 갈 수 있는지, 영역이 몇 개인지 | [DFS](../lv1-elementary/05-graph-basics/dfs/), [BFS](../lv1-elementary/05-graph-basics/bfs/), [연결 요소](../lv1-elementary/05-graph-basics/connected-components/) |
| 가중치 없는 그래프에서 최소 이동 횟수 | [BFS](../lv1-elementary/05-graph-basics/bfs/) |

### 그래프

| 문제의 신호 | 후보 |
|---|---|
| 최단 거리 / 최소 비용 경로 | [최단 경로 비교표](../lv2-intermediate/01-shortest-path/)에서 가중치 조건으로 선택 ([다익스트라](../lv2-intermediate/01-shortest-path/dijkstra/), [벨만-포드](../lv2-intermediate/01-shortest-path/bellman-ford/), [플로이드-워셜](../lv2-intermediate/01-shortest-path/floyd-warshall/)) |
| 가중치가 0 또는 1 | [0-1 BFS](../lv2-intermediate/01-shortest-path/zero-one-bfs/) |
| 같은 그룹인지 / 그룹 합치기 | [Union-Find](../lv2-intermediate/02-graph-algorithms/union-find/) |
| 작업의 선후 관계, 순서 정하기, 사이클 판정 | [위상 정렬](../lv2-intermediate/02-graph-algorithms/topological-sort/) |
| 모든 정점을 최소 비용으로 연결 | [크루스칼](../lv2-intermediate/02-graph-algorithms/kruskal/), [프림](../lv2-intermediate/02-graph-algorithms/prim/) |
| 두 집합으로 나눌 수 있는가 (이분 그래프 판정) | [이분 그래프](../lv2-intermediate/02-graph-algorithms/bipartite-graph/) |
| 서로 갈 수 있는 정점끼리의 묶음 (방향 그래프) | [강한 연결 요소](../lv3-advanced/03-graph-advanced/scc/) |
| 변수의 참/거짓 제약 (`A 이거나 B`) | [2-SAT](../lv3-advanced/03-graph-advanced/two-sat/) |
| 없애면 그래프가 끊기는 정점/간선 | [단절점과 단절선](../lv3-advanced/03-graph-advanced/articulation-and-bridges/) |
| 네트워크의 최대 유량, 최소 컷 | [디닉](../lv3-advanced/03-graph-advanced/dinic/) |
| 비용이 있는 유량 / 비용이 있는 배정 | [최소 비용 최대 유량](../lv4-expert/04-flow-matching/min-cost-max-flow/), [헝가리안](../lv4-expert/04-flow-matching/hungarian-algorithm/) |
| 이분 그래프의 최대 짝짓기 | [이분 매칭](../lv3-advanced/03-graph-advanced/bipartite-matching/) |
| 이분이 아닌 그래프의 최대 짝짓기 | [블로섬](../lv5-master/02-matching-matroid/blossom/) |
| "사이클 없이" + "색마다 하나씩" 같은 두 가지 독립 제약 | [매트로이드 교집합](../lv5-master/02-matching-matroid/matroid-intersection/) |
| 간선이 추가·삭제되는 그래프의 연결성 (입력을 다 알고 있다) | [오프라인 동적 연결성](../lv5-master/04-offline-dynamic/offline-dynamic-connectivity/) |

### 트리

| 문제의 신호 | 후보 |
|---|---|
| 트리 순회, 부모·깊이·서브트리 | [트리](../lv1-elementary/05-graph-basics/tree/), [트리 순회](../lv1-elementary/05-graph-basics/tree-traversal/) |
| 서브트리별 값을 합쳐 답을 구한다 | [트리 DP](../lv2-intermediate/03-trees/tree-dp/) |
| 가장 먼 두 정점 | [트리의 지름](../lv2-intermediate/03-trees/tree-diameter/) |
| 두 정점의 공통 조상, 경로의 정점 | [LCA](../lv3-advanced/03-graph-advanced/lca/) |
| 트리의 경로·서브트리에 갱신과 질의 | [HLD](../lv4-expert/02-tree-decomposition/heavy-light-decomposition/) |
| 트리에서 거리가 `k`인 쌍 세기 / 가장 가까운 표시된 정점 | [센트로이드 분해](../lv4-expert/02-tree-decomposition/centroid-decomposition/) |
| 트리의 간선이 바뀌며 경로 질의 | [링크-컷 트리](../lv5-master/01-dynamic-trees/link-cut-tree/) |
| 트리 모양은 고정이고 정점 값이 바뀌며 트리 DP 전체 값 | [탑 트리](../lv5-master/01-dynamic-trees/top-tree/) |

### 구간 / 자료구조

| 문제의 신호 | 후보 |
|---|---|
| 구간 합을 여러 번 묻는다 (값이 바뀌지 않는다) | [누적 합](../lv1-elementary/04-range-techniques/prefix-sum/), [2차원 누적 합](../lv1-elementary/04-range-techniques/two-dimensional-prefix-sum/) |
| 구간 합/최솟값을 묻고 값도 계속 바뀐다 | [세그먼트 트리](../lv3-advanced/01-range-query-structures/segment-tree/), [펜윅 트리](../lv3-advanced/01-range-query-structures/fenwick-tree/) |
| 구간 전체에 같은 값을 더하거나 바꾼다 | [느리게 갱신되는 세그먼트 트리](../lv3-advanced/01-range-query-structures/lazy-propagation/) |
| 값이 바뀌지 않는 배열의 구간 최솟값 | [희소 배열](../lv3-advanced/01-range-query-structures/sparse-table/) |
| 구간의 `k`번째 수 / 구간 안의 값 개수 | [웨이블릿 트리](../lv4-expert/03-advanced-data-structures/wavelet-tree/), [퍼시스턴트 세그먼트 트리](../lv4-expert/03-advanced-data-structures/persistent-segment-tree/), [머지 소트 트리](../lv4-expert/03-advanced-data-structures/merge-sort-tree/) |
| 구간 질의가 많고 구간 이동 비용이 작다 (오프라인) | [모스 알고리즘](../lv3-advanced/06-query-techniques/mos-algorithm/), [제곱근 분할](../lv3-advanced/06-query-techniques/sqrt-decomposition/) |
| 수열의 중간 삽입·삭제·구간 뒤집기 | [트립](../lv4-expert/03-advanced-data-structures/treap/), [스플레이 트리](../lv4-expert/03-advanced-data-structures/splay-tree/) |
| 값의 범위가 크다 (좌표만 쓰인다) | [좌표 압축](../lv2-intermediate/08-search-techniques/coordinate-compression/) |
| 가장 최근에 넣은 것부터 처리 | [스택](../lv1-elementary/01-data-structures/stack/), [단조 스택](../lv2-intermediate/08-search-techniques/monotonic-stack/) |
| 먼저 들어온 것부터 처리 | [큐](../lv1-elementary/01-data-structures/queue/) |
| 양쪽 끝에서 넣고 빼야 한다 | [덱](../lv1-elementary/01-data-structures/deque/), [슬라이딩 윈도우](../lv2-intermediate/08-search-techniques/sliding-window/) |
| 가장 큰/작은 값을 반복해서 꺼낸다 | [우선순위 큐](../lv1-elementary/01-data-structures/priority-queue/) |
| 존재 여부·개수를 빠르게 확인 | [해시 테이블](../lv1-elementary/01-data-structures/hash-table/) |
| 연속 부분 배열에 조건이 있다 | [투 포인터](../lv1-elementary/04-range-techniques/two-pointers/), [슬라이딩 윈도우](../lv2-intermediate/08-search-techniques/sliding-window/) |
| 이벤트를 좌표 순서대로 훑는다 (구간 겹침, 선분) | [스위핑](../lv2-intermediate/08-search-techniques/sweeping/) |

### 최적화 패러다임 / DP

| 문제의 신호 | 후보 |
|---|---|
| 같은 부분 문제가 반복되고, 최댓값/최솟값/경우의 수를 묻는다 | [다이나믹 프로그래밍](../lv1-elementary/07-algorithm-paradigms/dynamic-programming/), [배낭 문제](../lv2-intermediate/04-dynamic-programming/knapsack/) |
| 매 순간 가장 좋아 보이는 선택이 전체 최적이 된다 (증명 필요) | [그리디](../lv1-elementary/07-algorithm-paradigms/greedy/) |
| 수열의 증가하는 부분, 두 문자열의 공통 부분 | [LIS](../lv2-intermediate/04-dynamic-programming/lis/), [LCS](../lv2-intermediate/04-dynamic-programming/lcs/) |
| 구간을 합치며 최적을 구한다 | [구간 DP](../lv2-intermediate/04-dynamic-programming/interval-dp/) |
| 집합의 상태를 외판원처럼 방문 | [비트마스크 DP](../lv2-intermediate/04-dynamic-programming/bitmask-dp/) |
| 문제를 반으로 나눠 같은 문제로 풀 수 있다 | [분할 정복](../lv2-intermediate/05-divide-and-conquer/divide-and-conquer/) |
| 자릿수마다 제약이 있는 수의 개수 | [자릿수 DP](../lv3-advanced/07-dp-advanced/digit-dp/) |
| 기댓값을 구하고 상태 전이가 확률로 주어진다 | [기댓값 DP](../lv3-advanced/07-dp-advanced/expected-value-dp/) |
| `dp[i] = min(dp[j] + cost(j, i))`, 최적 `j`가 단조 | [분할 정복 최적화](../lv3-advanced/07-dp-advanced/divide-and-conquer-optimization/) |
| `dp[i] = min(dp[j] + b[j]·a[i])` 처럼 직선의 최솟값 | [볼록 껍질 트릭](../lv3-advanced/07-dp-advanced/convex-hull-trick/), [리 차오 트리](../lv4-expert/03-advanced-data-structures/li-chao-tree/) |
| "정확히 `k`개 고르기"의 비용이 볼록이다 | [에일리언 트릭](../lv4-expert/06-misc/aliens-trick/) |
| 수열을 정렬/단조하게 만드는 최소 비용(값 범위가 크다), 이웃 차 제한 | [기울기 트릭](../lv5-master/04-offline-dynamic/slope-trick/) |
| 점화식이 선형이고 `n`이 10^18 | [행렬 거듭제곱](../lv3-advanced/07-dp-advanced/matrix-exponentiation/), [키타마사](../lv4-expert/06-misc/kitamasa/) |
| 수열의 앞부분만 있고 점화식을 모른다 | [벌레캠프–매시](../lv5-master/03-algebra/berlekamp-massey/) |

### 수학

| 문제의 신호 | 후보 |
|---|---|
| 최대공약수, 최소공배수, 서로소 | [유클리드 호제법](../lv1-elementary/06-number-theory/euclidean-algorithm/), [서로소](../lv1-elementary/06-number-theory/relatively-prime/) |
| 소수 판별, 소수 목록, 소인수분해 | [소수 판별](../lv0-basics/02-number-theory/naive-prime-check/), [에라토스테네스의 체](../lv1-elementary/06-number-theory/sieve-of-eratosthenes/), [소인수분해](../lv1-elementary/06-number-theory/prime-factorization/) |
| 약수를 모든 수에 대해 | [약수 체](../lv1-elementary/06-number-theory/divisor-sieve/) |
| 10^18 이하 수의 소수 판별 / 소인수분해 | [밀러-라빈](../lv4-expert/01-number-theory/miller-rabin/), [폴라드 로](../lv4-expert/01-number-theory/pollard-rho/) |
| 큰 수의 나머지, 모듈러 역원 | [페르마의 소정리](../lv2-intermediate/06-number-theory/fermat-little-theorem/), [모듈러 역원](../lv2-intermediate/06-number-theory/modular-inverse/), [확장 유클리드](../lv3-advanced/02-number-theory/extended-euclidean-algorithm/) |
| 조합의 나머지 (`nCr mod p`) | [조합 mod 소수](../lv2-intermediate/06-number-theory/ncr-mod/), 모듈러가 작으면 [뤼카 정리](../lv4-expert/01-number-theory/lucas-theorem/) |
| 서로 다른 모듈러의 연립 합동식 | [중국인의 나머지 정리](../lv3-advanced/02-number-theory/chinese-remainder-theorem/) |
| 약수/배수에 대한 합을 뒤집기, 서로소인 쌍의 개수 | [뫼비우스 반전](../lv4-expert/01-number-theory/mobius-inversion/) |
| 회전·뒤집기를 같은 것으로 보는 경우의 수 | [번사이드 보조정리](../lv4-expert/01-number-theory/burnside-lemma/) |
| 큰 수의 곱, 다항식의 곱, 합성곱 | [FFT/NTT](../lv4-expert/01-number-theory/fft-ntt/) |
| 생성함수의 역수·로그·지수·거듭제곱, 다점 계산 | [다항식 연산](../lv5-master/03-algebra/polynomial-operations/) |
| `n ≤ 10^10`의 소수 개수, `Σφ`, `Σσ` 같은 곱셈적 함수의 누적합 | [민-25 체](../lv5-master/03-algebra/min-25-sieve/) |
| 돌 게임·승패 판정(합 게임) | [스프라그-그런디](../lv4-expert/06-misc/sprague-grundy/) |
| 정수의 이진 표현, XOR | [비트 연산자](../lv1-elementary/09-bit-manipulation/bitwise-operators/) |

### 문자열

| 문제의 신호 | 후보 |
|---|---|
| 문자열에서 패턴 찾기 | [KMP](../lv2-intermediate/07-strings/kmp/), [라빈-카프](../lv2-intermediate/07-strings/rabin-karp/), [Z 알고리즘](../lv3-advanced/05-strings-advanced/z-algorithm/) |
| 접두사 검색, 사전 | [트라이](../lv2-intermediate/07-strings/trie/) |
| 여러 패턴을 한 번에 찾기 | [아호-코라식](../lv3-advanced/05-strings-advanced/aho-corasick/) |
| 가장 긴 팰린드롬 부분 문자열 | [매내처](../lv3-advanced/05-strings-advanced/manacher/) |
| 부분 문자열의 개수·사전순·가장 긴 공통 부분 | [접미사 배열과 LCP](../lv3-advanced/05-strings-advanced/suffix-array-lcp/), [접미사 자동자](../lv4-expert/05-strings/suffix-automaton/) |

### 기하

| 문제의 신호 | 후보 |
|---|---|
| 세 점의 방향, 선분이 겹치는지 | [CCW](../lv3-advanced/04-geometry/ccw/), [선분 교차](../lv3-advanced/04-geometry/segment-intersection/) |
| 점들을 모두 감싸는 가장 작은 볼록 다각형 | [볼록 껍질](../lv3-advanced/04-geometry/convex-hull/) |
| 반평면들의 공통 영역, 2차원 선형 계획 | [반평면 교집합](../lv4-expert/06-misc/half-plane-intersection/) |

## 풀리지 않을 때

- 제한을 다시 읽습니다. 입력 크기가 풀이를 알려 주는 경우가 많습니다.
- 문제를 **그래프 / DP / 정렬 후 탐색** 중 하나로 바꿔서 볼 수 없는지 생각합니다.
- 작은 입력에서 브루트 포스 결과와 내 풀이를 비교하는 **스트레스 테스트**를 만들어 반례를 찾습니다. 이 저장소의 `test_solution.py`가 같은 방식입니다.
