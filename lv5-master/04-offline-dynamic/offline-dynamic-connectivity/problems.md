# 연습문제 — 오프라인 동적 연결성

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [BOJ 16911 그래프와 쿼리](https://www.acmicpc.net/problem/16911) | 간선 추가·삭제, 연결 질의 | [solution.py](solution.py)의 `main()`이 같은 형식. 시간 구간 트리 + 롤백 유니온 파인드의 기본형 |
| 2 | [Codeforces 813F - Bipartite Checking](https://codeforces.com/problemset/problem/813/F) | 간선을 넣고 빼며 매번 이분 그래프인지 | 홀짝(색) 유니온 파인드를 롤백하기 (`("bipartite",)` 질의) |
| 3 | [Codeforces 1140F - Extending Set of Points](https://codeforces.com/problemset/problem/1140/F) | 점 `(x, y)`의 추가·삭제와 매번 닫힌 집합의 크기 | 성분마다 `(행의 수) × (열의 수)`를 합산. 유니온 파인드의 루트에 값을 얹고 롤백 |
| 4 | [Library Checker - Dynamic Graph Vertex Add Component Sum](https://judge.yosupo.jp/problem/dynamic_graph_vertex_add_component_sum) | 간선 추가·삭제, 정점 값 더하기, 성분 합 | 정점 값 변경도 "시간 구간" 으로 바꾸는 방법 (값을 더한 시각부터의 구간) |

## 풀이 메모

- 1번을 풀 때 `n`, `q`가 크면 질의 시각만 압축해 구간 트리를 작게 만들어 보세요 (README 6절의 마지막 항목).
- 2번은 이 저장소의 `bipartite` 질의를 간선 하나가 홀수 사이클을 만들 때마다 `odd_cycles`가 늘어나는 것으로 풀 수 있습니다.
- 3번과 4번은 유니온 파인드에 성분별 집계를 얹는 문제입니다. 합칠 때 두 집계를 더하고 롤백할 때 되돌리는 것이 전부입니다.
