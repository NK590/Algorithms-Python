# 연습문제 — 이분 그래프

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 1707 이분 그래프](https://www.acmicpc.net/problem/1707) | 기본형 | 연결되지 않은 그래프, 여러 테스트 케이스. [solution.py](solution.py)의 `main()`이 같은 형태를 처리한다 |
| 2 | [LeetCode 785 Is Graph Bipartite?](https://leetcode.com/problems/is-graph-bipartite/) | 기본형 | 인접 리스트가 이미 주어진다. `is_bipartite` |
| 3 | [LeetCode 886 Possible Bipartition](https://leetcode.com/problems/possible-bipartition/) | 응용 | "서로 싫어하는 사람"을 간선으로 만들어 두 그룹으로 나눌 수 있는가 |
| 4 | [백준 13265 색칠하기](https://www.acmicpc.net/problem/13265) | 2-색칠 | 이웃하는 원이 서로 다른 색이어야 한다. 테스트 케이스 여러 개 |
| 5 | [백준 2188 축사 배정](https://www.acmicpc.net/problem/2188) | 다음 단계 (이분 매칭) | 소와 축사의 관계는 이분 그래프. 최대 몇 마리가 들어갈 수 있는가는 [이분 매칭](../../../lv3-advanced/03-graph-advanced/bipartite-matching/) |
| 6 | [백준 11375 열혈강호](https://www.acmicpc.net/problem/11375) | 다음 단계 (이분 매칭) | 직원과 일의 이분 그래프에서 최대로 짝짓기 |

## 풀이 메모

- 1번에서 정점 수가 크면 재귀 DFS는 `RecursionError`가 납니다. 이 폴더의 BFS가 안전합니다.
- 3번은 "싫어하는 쌍"이 무방향 간선이라는 점, 정점 번호가 1부터라는 점을 주의하세요.
- 이분 그래프임을 확인한 뒤의 단계(최대 매칭)는 [이분 매칭](../../../lv3-advanced/03-graph-advanced/bipartite-matching/)에서 다룹니다.
- 홀수 사이클 자체가 필요한 문제(`odd_cycle`)를 직접 만들어 풀어 보는 것도 좋습니다.
