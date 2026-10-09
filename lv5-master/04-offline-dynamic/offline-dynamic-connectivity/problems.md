# 연습문제 — 오프라인 동적 연결성

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [Library Checker — Dynamic Graph Vertex Add Component Sum](https://judge.yosupo.jp/problem/dynamic_graph_vertex_add_component_sum) | 핵심 연습 | 간선의 생존 시간과 롤백 DSU를 결합한다 |
| 2 | [CSES — Road Construction](https://cses.fi/problemset/task/1676) | 선행 연습 | 선행으로 삭제가 없는 온라인 연결성 문제를 비교한다 |
| 3 | [Codeforces 813F - Bipartite Checking](https://codeforces.com/problemset/problem/813/F) | 간선을 넣고 빼며 매번 이분 그래프인지 | 홀짝(색) 유니온 파인드를 롤백하기 (`("bipartite",)` 질의) |
| 4 | [Codeforces 1140F - Extending Set of Points](https://codeforces.com/problemset/problem/1140/F) | 점 `(x, y)`의 추가·삭제와 매번 닫힌 집합의 크기 | 성분마다 `(행의 수) × (열의 수)`를 합산. 유니온 파인드의 루트에 값을 얹고 롤백 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
