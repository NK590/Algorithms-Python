# 연습문제 — 트리의 지름

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [LeetCode 543 Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/) | 기본형 (간선 수) | 이진 트리. 각 노드에서 (왼쪽 깊이 + 오른쪽 깊이)의 최댓값 (트리 DP 방식) |
| 2 | [백준 1967 트리의 지름](https://www.acmicpc.net/problem/1967) | 기본형 | 루트가 있는 트리의 부모→자식 간선 입력. 무방향으로 읽어 BFS 두 번. [solution.py](solution.py)의 `main()`이 비슷한 형태(간선 `A B C`)를 처리한다 |
| 3 | [백준 1167 트리의 지름](https://www.acmicpc.net/problem/1167) | 기본형 | 정점마다 인접 정점·거리 목록이 한 줄로 주어진다(입력 파싱이 핵심). 정점 수 10⁵ |
| 4 | [백준 1240 노드사이의 거리](https://www.acmicpc.net/problem/1240) | 거리 질의 | 질의 쌍마다 BFS/DFS. n이 작으면 충분하고, 크면 LCA |
| 5 | [LeetCode 310 Minimum Height Trees](https://leetcode.com/problems/minimum-height-trees/) | 중심 | 가장 낮은 트리가 되는 루트 = 트리의 중심. `tree_centers` |

## 풀이 메모

- 3번은 입력이 `정점 (이웃 거리)* -1` 형식으로 한 줄에 여러 개 들어옵니다. 파싱만 맞으면 이 폴더의 `tree_diameter`가 그대로 동작합니다.
- 2번은 간선이 "부모 자식 가중치"로 주어지지만 트리의 지름은 방향과 무관하므로 무방향으로 읽습니다.
- 5번의 정답은 `tree_centers`가 돌려주는 한두 개의 정점입니다. 각 정점을 루트로 높이를 직접 구하는 O(n²)와 비교해 보세요.
- 가중치에 음수가 섞인 문제라면 BFS 두 번은 틀립니다. 트리 DP로 일반화해야 합니다.
