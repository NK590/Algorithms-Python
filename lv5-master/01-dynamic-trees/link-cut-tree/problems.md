# 연습문제 — 링크-컷 트리

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [Luogu P3690 【模板】Link Cut Tree (动态树)](https://www.luogu.com.cn/problem/P3690) | 경로 xor, 링크, 컷, 값 변경 | 가장 기본형. 집계를 합 대신 xor로 바꾸고 `link`/`cut`이 항상 유효하다고 가정하지 말고 연결 여부를 먼저 확인 |
| 2 | [Luogu P3203 弹飞绵羊](https://www.luogu.com.cn/problem/P3203) | 각 칸에서 `a_i`칸 앞으로 튕김, 몇 번 튕기면 나가는가, 값 변경 | 가상 정점 `n`(탈출)에 모두 이어 두고 "경로 길이". `cut`/`link`로 `i → i + a_i` 간선을 바꾼다 |
| 3 | [Library Checker - Dynamic Tree Vertex Add Path Sum](https://judge.yosupo.jp/problem/dynamic_tree_vertex_add_path_sum) | 정점 더하기, 경로 합, 간선 교체 | [solution.py](solution.py)의 `main()`이 같은 형태 |
| 4 | [SPOJ DYNACON1 - Dynamic Tree Connectivity](https://www.spoj.com/problems/DYNACON1/) | 간선 추가·삭제와 연결 질의 (삭제되는 간선은 항상 숲 안) | `connected`. 오프라인 동적 연결성(시간 구간 트리)과 둘 다 풀어 비교 |
| 5 | [Library Checker - Dynamic Tree Vertex Set Path Composite](https://judge.yosupo.jp/problem/dynamic_tree_vertex_set_path_composite) | 정점의 일차 함수를 경로 순서로 합성 | **비가환** 집계: 뒤집을 때 정방향·역방향 합성값을 맞바꿔야 한다 |
| 6 | [SPOJ QTREE6 - Query on a tree VI](https://www.spoj.com/problems/QTREE6/) | 정점 색 뒤집기, 같은 색으로 연결된 컴포넌트의 크기 | **가상 서브트리** 정보(경로 부모로 매달린 서브트리의 크기)를 함께 유지 |
| 7 | [Codeforces 1172E Nauuo and ODT](https://codeforces.com/problemset/problem/1172/E) | 정점 색 뒤집기, 단색 경로의 수 | 색마다 LCT를 두고 "같은 색 컴포넌트의 크기 제곱 합"을 가상 서브트리로 유지하는 고난도 응용 |

## 풀이 메모

- 1번과 3번은 같은 구조의 집계만 다릅니다. 두 번 모두 [test_solution.py](test_solution.py)처럼 DFS로 경로를 직접 구하는 순진한 숲과 무작위 비교하세요.
- 2번은 간선 방향이 고정(`i → i + a_i`)이라 LCT를 한 방향 트리로만 쓰는 연습입니다. `make_root`를 쓰지 않고도 되는 문제입니다 (`access`와 `find_root`만으로).
- 4번에서 간선 삭제 시 "이 간선이 정말 있는가" 를 입력이 보장하는지 확인하세요. `cut`은 없는 간선이면 `ValueError`를 냅니다.
- 5번은 합성 순서가 `f_v ∘ … ∘ f_u`라서 스플레이 노드가 두 방향의 합성값을 모두 들고 있어야 합니다. 뒤집기 표시를 내릴 때 두 값을 맞바꾸는 것이 포인트.
- 6번과 7번은 "경로 부모로 매달린 가상 서브트리" 정보를 정점마다 유지해야 합니다. `access` 중에 오른쪽 자식을 갈아 끼울 때 이전 오른쪽 서브트리의 집계를 가상 정보에 더하고 새 오른쪽을 뺍니다. 이 저장소의 구현에는 없는 확장이므로 직접 추가해 보는 것이 숙제입니다.
