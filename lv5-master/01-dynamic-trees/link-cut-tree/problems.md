# 연습문제 — 링크-컷 트리

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [Library Checker — Dynamic Tree Vertex Add Path Sum](https://judge.yosupo.jp/problem/dynamic_tree_vertex_add_path_sum) | 핵심 연습 | link·cut·경로 합을 보조 스플레이 트리로 구현한다 |
| 2 | [Luogu P3690 【模板】Link Cut Tree (动态树)](https://www.luogu.com.cn/problem/P3690) | 경로 xor, 링크, 컷, 값 변경 | 가장 기본형. 집계를 합 대신 xor로 바꾸고 `link`/`cut`이 항상 유효하다고 가정하지 말고 연결 여부를 먼저 확인 |
| 3 | [Luogu P3203 弹飞绵羊](https://www.luogu.com.cn/problem/P3203) | 각 칸에서 `a_i`칸 앞으로 튕김, 몇 번 튕기면 나가는가, 값 변경 | 가상 정점 `n`(탈출)에 모두 이어 두고 "경로 길이". `cut`/`link`로 `i → i + a_i` 간선을 바꾼다 |
| 4 | [SPOJ DYNACON1 - Dynamic Tree Connectivity](https://www.spoj.com/problems/DYNACON1/) | 간선 추가·삭제와 연결 질의 (삭제되는 간선은 항상 숲 안) | `connected`. 오프라인 동적 연결성(시간 구간 트리)과 둘 다 풀어 비교 |
| 5 | [Library Checker - Dynamic Tree Vertex Set Path Composite](https://judge.yosupo.jp/problem/dynamic_tree_vertex_set_path_composite) | 정점의 일차 함수를 경로 순서로 합성 | **비가환** 집계: 뒤집을 때 정방향·역방향 합성값을 맞바꿔야 한다 |
| 6 | [SPOJ QTREE6 - Query on a tree VI](https://www.spoj.com/problems/QTREE6/) | 정점 색 뒤집기, 같은 색으로 연결된 컴포넌트의 크기 | **가상 서브트리** 정보(경로 부모로 매달린 서브트리의 크기)를 함께 유지 |
| 7 | [Codeforces 1172E Nauuo and ODT](https://codeforces.com/problemset/problem/1172/E) | 정점 색 뒤집기, 단색 경로의 수 | 색마다 LCT를 두고 "같은 색 컴포넌트의 크기 제곱 합"을 가상 서브트리로 유지하는 고난도 응용 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
