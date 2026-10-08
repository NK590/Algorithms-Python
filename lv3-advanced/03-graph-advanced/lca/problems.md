# 연습문제 — 최소 공통 조상 (LCA)

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [LeetCode 235 Lowest Common Ancestor of a Binary Search Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) | BST의 LCA | 값의 대소만으로 내려가며 갈라지는 곳이 LCA. 표가 필요 없는 가장 쉬운 경우 |
| 2 | [LeetCode 236 Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | 이진 트리의 LCA | 질의가 한 번이면 DFS 한 번으로 충분하다. 두 노드를 서브트리에서 각각 찾았는지 올려 보낸다 |
| 3 | [백준 3584 가장 가까운 공통 조상](https://www.acmicpc.net/problem/3584) | 루트 찾기 + LCA | 루트가 주어지지 않는다(부모가 없는 정점). 테스트 케이스가 여러 개 |
| 4 | [백준 11437 LCA](https://www.acmicpc.net/problem/11437) | 기본형 | `N ≤ 5만`. 순진한 방법도 통과할 수 있다. [solution.py](solution.py)의 `main()`이 같은 형태 |
| 5 | [백준 11438 LCA 2](https://www.acmicpc.net/problem/11438) | 기본형 (큰 입력) | `N ≤ 10만`, 질의 10만. 이진 리프팅이 필요하고 사슬 입력에서 재귀 DFS는 깊이 제한에 걸린다 |
| 6 | [LeetCode 1483 Kth Ancestor of a Tree Node](https://leetcode.com/problems/kth-ancestor-of-a-tree-node/) | `k`번째 조상 | `kth_ancestor`. 루트를 넘어가면 -1을 돌려주는 규칙에 주의 |
| 7 | [백준 1761 정점들의 거리](https://www.acmicpc.net/problem/1761) | 가중치 거리 | 간선 가중치의 누적 거리 `dist[v]`를 두고 `dist[u] + dist[v] − 2·dist[lca]` |
| 8 | [백준 3176 도로 네트워크](https://www.acmicpc.net/problem/3176) | 경로 위의 최솟값·최댓값 | 리프팅 표에 "2^k칸 위까지의 최소·최대 간선"을 함께 저장해 점프하며 합친다 |
| 9 | [백준 13511 트리와 쿼리 2](https://www.acmicpc.net/problem/13511) | 경로의 합 + `k`번째 정점 | 거리 합과 경로 위의 `k`번째 정점. `lca`로 두 구간으로 나눈다 |
| 10 | [백준 15480 LCA와 쿼리](https://www.acmicpc.net/problem/15480) | 루트가 바뀜 | 질의마다 루트가 다르다. 세 정점의 `lca`들 중 가장 깊은 것이 답 |

## 풀이 메모

- 4번은 순진한 방법으로도 풀리지만 5번은 안 됩니다. 같은 문제를 [README](README.md#2-핵심-아이디어)의 세 방법으로 풀어 보고 속도를 비교해 보세요.
- 5번의 사슬 입력에서는 [테스트](test_solution.py)의 `test_deep_chain_does_not_recurse`처럼 깊이 10만짜리 트리에서 재귀 없이 동작하는지 확인해야 합니다.
- 7번, 8번은 "정점마다 루트에서의 누적 값"이나 "표에 값을 함께 저장"하는 두 가지 방식을 모두 써 보세요. 합은 누적 값의 차로, 최솟값·최댓값은 표에 저장해야 합니다(빼기가 불가능).
- 10번은 `lca(a, b)`, `lca(a, r)`, `lca(b, r)` 세 값 중 가장 깊은 것이 루트를 `r`로 바꿨을 때의 `lca(a, b)`입니다. 왜 그런지 그림을 그려 보세요.
