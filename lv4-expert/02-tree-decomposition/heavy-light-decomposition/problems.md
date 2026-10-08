# 연습문제 — 헤비-라이트 분할

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES 1137 Subtree Queries](https://cses.fi/problemset/task/1137) | 점 갱신 + 서브트리 합 | 서브트리가 연속 구간이 되는 전위 번호만으로 풀린다. HLD의 `pos`와 `size`를 이해하는 출발점 |
| 2 | [백준 2820 자동차 공장](https://www.acmicpc.net/problem/2820) | 서브트리 더하기 + 점 질의 | 전위 번호 + 펜윅 트리(구간 더하기, 점 질의). 자기 자신은 빼고 부하들만 올린다 |
| 3 | [CSES 1138 Path Queries](https://cses.fi/problemset/task/1138) | 루트까지 경로 합 + 점 갱신 | 루트에서 시작하는 경로만이면 HLD 없이 오일러 투어 + 펜윅 트리. "루트 경로" 와 "임의 경로" 의 차이 |
| 4 | [백준 3176 도로 네트워크](https://www.acmicpc.net/problem/3176) | 경로 간선 최솟값·최댓값 (갱신 없음) | 갱신이 없으면 이진 올리기로 충분. HLD와 둘 다 짜서 결과를 비교 |
| 5 | [Library Checker - Vertex Add Path Sum](https://judge.yosupo.jp/problem/vertex_add_path_sum) | 점 더하기 + 경로 합 | HLD의 가장 기본형. `PathQuery`/`PathAddSubtreeSum` 그대로 |
| 6 | [CSES 2134 Path Queries II](https://cses.fi/problemset/task/2134) | 점 갱신 + 경로 최댓값 | 합 대신 최댓값. 구간 트리의 `combine`만 바꾸면 된다 |
| 7 | [백준 13510 트리와 쿼리 1](https://www.acmicpc.net/problem/13510) | 간선 갱신 + 경로 간선 최댓값 | [solution.py](solution.py)의 `main()`이 같은 형태. 간선 → 아래쪽 정점, LCA 제외 |
| 8 | [SPOJ QTREE - Query on a tree](https://www.spoj.com/problems/QTREE/) | 7번과 같은 유형, 테스트 케이스 여러 개 | 입력 형식만 다른 고전. 케이스마다 전부 초기화하는 습관 |
| 9 | [Codeforces 343D Water Tree](https://codeforces.com/problemset/problem/343/D) | 서브트리 채우기 + 루트 경로 비우기 + 점 질의 | 서브트리 연산과 경로 연산이 한 배열에서 섞인다. 시각(타임스탬프)으로 "더 최근에 한 연산" 을 비교하는 발상 |
| 10 | [백준 13512 트리와 쿼리 3](https://www.acmicpc.net/problem/13512) | 색 뒤집기 + 루트에서 `v`까지 처음 만나는 검은 정점 | 사슬마다 집합(또는 구간 트리)을 두고, 경로의 사슬을 위에서부터 훑는다 |
| 11 | [Library Checker - Vertex Set Path Composite](https://judge.yosupo.jp/problem/vertex_set_path_composite) | 정점의 일차함수를 경로 순서대로 합성 | **교환 법칙이 안 되는** 연산: `u` 쪽 구간과 `v` 쪽 구간을 따로 모아서 방향을 맞춰야 한다 |

## 풀이 메모

- 1번~3번은 HLD 없이 풀립니다. "서브트리 연산만" 이거나 "루트에서의 경로만" 이면 오일러 투어(전위 번호)로 충분하고, HLD는 **임의의 두 점 사이 경로** 가 나올 때 필요합니다. 어떤 문제에 어느 도구가 필요한지 판단하는 연습이 됩니다.
- 4번은 갱신이 없어서 이진 올리기가 더 짧습니다. 같은 입력을 두 방식으로 풀어 답이 같은지 비교하면 HLD의 간선 모드(LCA 제외)가 맞는지 확인됩니다.
- 5번~8번은 구현을 그대로 옮기는 문제입니다. 입력이 크면 `sys.stdin.buffer.read().split()` 하나로 읽고, 재귀 대신 반복문 DFS를 씁니다 (사슬 모양 트리).
- 9번은 "채우기" 와 "비우기" 의 순서가 중요한 문제입니다. 각 정점이 마지막으로 채워진 시각과 마지막으로 비워진 시각을 따로 구간(서브트리 구간, 경로 구간)에 새겨 두고, 점 질의에서 두 시각을 비교하는 방식으로 풀 수 있습니다.
- 10번은 한 사슬에서 가장 위의 검은 정점을 찾는 구조가 필요합니다. 루트에서 `v`로 가는 경로의 사슬들을 *위에서부터* 확인해야 "처음 나오는" 정점을 찾습니다 (`path_segments`는 아래에서 위로 구간을 돌려주므로 순서를 뒤집어 처리).
- 11번은 합성 `f_v ∘ … ∘ f_u`의 순서를 맞추는 문제입니다. `u`에서 `lca`까지 올라가는 쪽은 *역방향*, `lca`에서 `v`로 내려가는 쪽은 *정방향* 으로 합성해야 해서, 구간 트리에 정방향 합성과 역방향 합성을 함께 저장하는 것이 흔한 해법입니다.
