# 연습문제 — SCC (강한 연결 요소)

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [LeetCode 802 Find Eventual Safe States](https://leetcode.com/problems/find-eventual-safe-states/) | 사이클에 닿지 않는 정점 | 사이클에 속하거나 사이클로 이어지는 정점을 제외. 간선을 뒤집은 위상 정렬이나 SCC로 풀린다 |
| 2 | [백준 2150 Strongly Connected Component](https://www.acmicpc.net/problem/2150) | 기본형 | SCC의 수와 각 SCC의 정점을 정렬해 출력. [solution.py](solution.py)의 `main()`이 같은 형태 |
| 3 | [백준 4196 도미노](https://www.acmicpc.net/problem/4196) | 진입 차수 0인 SCC의 수 | 직접 쓰러뜨려야 하는 최소 개수. `condensation`으로 줄인 DAG에서 소스를 센다 |
| 4 | [백준 3977 축구 전술](https://www.acmicpc.net/problem/3977) | 출발점이 될 수 있는 정점 | 모든 정점에 도달할 수 있는 정점들 = 소스 SCC가 하나일 때 그 SCC. 아니면 `Confused` |
| 5 | [백준 2152 여행 계획 세우기](https://www.acmicpc.net/problem/2152) | SCC + DAG DP | SCC의 크기를 가중치로, 시작 도시에서 끝 도시까지 최대 방문 도시 수 |
| 6 | [백준 4013 ATM](https://www.acmicpc.net/problem/4013) | SCC + DAG DP | 지나는 SCC의 ATM 돈을 모두 합할 수 있다. 레스토랑이 있는 SCC에서 끝나는 경로 중 최대 |
| 7 | [백준 11280 2-SAT - 3](https://www.acmicpc.net/problem/11280) | SCC로 2-SAT 판정 | 함의 그래프에서 변수와 그 부정이 같은 SCC인지. [2-SAT](../two-sat/)로 이어진다 |

## 풀이 메모

- 3번은 `condensation(n, edges)`로 얻은 DAG에서 들어오는 간선이 없는 SCC의 수를 세는 문제입니다. [README](README.md#3-손으로-따라가기)의 "간선 몇 개 더?"와 같은 소스/싱크 개념입니다.
- 5번, 6번은 SCC의 번호가 위상 정렬 순서(코사라주)나 그 역순(타잔)인 점을 이용해 번호 순서대로 DP를 돌립니다. 이 저장소의 `condensation`은 코사라주 순서(소스가 먼저)입니다.
- 정점이 10⁵개를 넘는 문제는 파이썬에서 재귀 DFS를 쓰면 안 됩니다. [테스트](test_solution.py)의 사슬 입력(`test_deep_graphs_do_not_recurse`)과 같은 상황입니다.
- 1번을 SCC로 풀면 "크기가 1이고 자기 루프가 없는 SCC에서 나가는 모든 경로가 안전한 SCC로만 향하는가"를 확인합니다.
