---
level: 1
order: 3
tags: [graph, search, dfs]
prerequisites: [graph, stack]
time: O(V+E)
space: O(V)
status: migrated
---

# DFS (Depth-First Search, 깊이 우선 탐색)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

## 개요 (기존 주석에서 옮김)

- 주어진 트리에서, 루트에서부터 제일 말단 노드까지 탐색 후, 더 이상 자식 노드가 없을 시
- 다른 자식 노드가 있을 떄까지 돌아와서 다시 다른 노드를 따라 말단까지 반복해서 탐색하는 방식
- 트리가 아닌 사이클이 존재하는 그래프에서도 알고리즘을 개량하여 사용이 가능함
- 단순 검색보단 모든 데이터를 순회하는 경우에 유리하며, 백트래킹 등에 자주 응용됨

## 코드

- [solution.py](solution.py)
