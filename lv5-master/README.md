---
level: 5
name: 마스터
tier: Ruby
summary: 링크-컷 트리, 블로섬, 다항식 연산 등 논문·대회 해설 수준의 최상위 알고리즘을 다룬다
---

# Lv5 · 마스터 (Ruby)

논문이나 대회 해설 수준의 알고리즘을 다루는 단계입니다. 모든 개념에 파이썬 참고 구현이 있고, 순진한 방법·전수 탐색·최적성 증명서와 비교하는 테스트로 정확성을 확인했습니다. 대회 제한 시간을 맞추기 어려운 주제가 많아서 각 개념의 "복잡도와 입력 크기 가이드"에 이 환경에서 측정한 한계(파이썬으로 현실적인 입력 크기)를 솔직하게 적었습니다. 제한이 빡빡한 대회에서는 같은 알고리즘의 C++ 구현이 필요합니다.

- **solved.ac 기준**: Ruby 난이도의 문제 (알고리즘별 난이도는 문제에 따라 달라 대략적인 기준입니다)
- **선수 지식**: Lv4 내용
- **이 레벨을 마치면**: 최상위 알고리즘의 핵심 아이디어와 적용 조건을 설명하고, 참고 구현을 읽고 검증할 수 있다

## 개념 목록

<!-- INDEX:START -->
### [동적 트리 (Dynamic Trees)](01-dynamic-trees/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [링크-컷 트리 (Link-Cut Tree)](01-dynamic-trees/link-cut-tree/) | `done` | 분할 상환 O(log n) (access, link, cut, 경로 질의 모두) | [splay-tree](../lv4-expert/03-advanced-data-structures/splay-tree/), [heavy-light-decomposition](../lv4-expert/02-tree-decomposition/heavy-light-decomposition/), [lca](../lv3-advanced/03-graph-advanced/lca/) |
| [탑 트리 (Top Tree) — 정적 탑 트리](01-dynamic-trees/top-tree/) | `done` | 구성 O(n), 정점 값 갱신 O(log n) (클러스터 트리의 깊이) | [heavy-light-decomposition](../lv4-expert/02-tree-decomposition/heavy-light-decomposition/), [link-cut-tree](01-dynamic-trees/link-cut-tree/), [tree-dp](../lv2-intermediate/03-trees/tree-dp/) |

### [매칭과 매트로이드 (Matching & Matroids)](02-matching-matroid/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [블로섬 알고리즘 (Blossom Algorithm, Edmonds)](02-matching-matroid/blossom/) | `done` | O(V³) (정점마다 증가 경로 탐색 한 번, 탐색 하나가 O(V² + E)) | [bipartite-matching](../lv3-advanced/03-graph-advanced/bipartite-matching/), [bfs](../lv1-elementary/05-graph-basics/bfs/) |
| [매트로이드 교집합 (Matroid Intersection)](02-matching-matroid/matroid-intersection/) | `done` | 증가마다 O(r·n) 번의 독립성 오라클 호출 (r: 답의 크기), 전체 O(r²·n) 호출 | [bipartite-matching](../lv3-advanced/03-graph-advanced/bipartite-matching/), [bellman-ford](../lv2-intermediate/01-shortest-path/bellman-ford/), [union-find](../lv2-intermediate/02-graph-algorithms/union-find/) |

### [대수와 수열 (Algebra & Sequences)](03-algebra/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [벌레캠프–매시 (Berlekamp–Massey)](03-algebra/berlekamp-massey/) | `done` | O(n²) (n: 항의 개수), n 번째 항은 O(L² log k) | [kitamasa](../lv4-expert/06-misc/kitamasa/), [modular-inverse](../lv2-intermediate/06-number-theory/modular-inverse/), [matrix-exponentiation](../lv3-advanced/07-dp-advanced/matrix-exponentiation/) |
| [다항식 연산 (Polynomial Operations)](03-algebra/polynomial-operations/) | `done` | 곱셈 M(n) 이면 역수·로그·지수·거듭제곱·제곱근·나눗셈 O(M(n)), 다점 계산·보간 O(M(n) log n) | [fft-ntt](../lv4-expert/01-number-theory/fft-ntt/), [modular-inverse](../lv2-intermediate/06-number-theory/modular-inverse/), [kitamasa](../lv4-expert/06-misc/kitamasa/) |
| [민-25 체 (Min_25 Sieve)](03-algebra/min-25-sieve/) | `done` | O(n^{3/4}) (소수 테이블) + 재귀 (경험적으로 n^{3/4}/log n 부근), 메모리 O(√n) | [sieve-of-eratosthenes](../lv1-elementary/06-number-theory/sieve-of-eratosthenes/), [euler-phi](../lv2-intermediate/06-number-theory/euler-phi/), [mobius-inversion](../lv4-expert/01-number-theory/mobius-inversion/) |

### [오프라인과 동적 최적화 (Offline & Dynamic Optimization)](04-offline-dynamic/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [오프라인 동적 연결성 (Offline Dynamic Connectivity)](04-offline-dynamic/offline-dynamic-connectivity/) | `done` | O((T + E) log T · log n) (T: 연산 수, E: 간선 구간 수) | [union-find](../lv2-intermediate/02-graph-algorithms/union-find/), [segment-tree](../lv3-advanced/01-range-query-structures/segment-tree/), [divide-and-conquer](../lv2-intermediate/05-divide-and-conquer/divide-and-conquer/) |
| [기울기 트릭 (Slope Trick)](04-offline-dynamic/slope-trick/) | `done` | 연산마다 O(log n), 함수 평가는 O(n) | [priority-queue](../lv1-elementary/01-data-structures/priority-queue/), [dynamic-programming](../lv1-elementary/07-algorithm-paradigms/dynamic-programming/), [convex-hull-trick](../lv3-advanced/07-dp-advanced/convex-hull-trick/) |
<!-- INDEX:END -->

전체 커리큘럼과 개념 사이의 선행 관계는 [ROADMAP](../ROADMAP.md)에서 볼 수 있습니다.
