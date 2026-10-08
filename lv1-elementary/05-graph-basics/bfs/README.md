---
level: 1
order: 4
tags: [graph, search, bfs]
prerequisites: [graph, queue]
time: O(V+E)
space: O(V)
status: migrated
---

# BFS (Breadth-First Search, 너비 우선 탐색)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

## 개요 (기존 주석에서 옮김)

- 주어진 트리에서, 루트로부터 같은 레벨만큼 떨어져 있는 노드들을 순차적으로 탐색하는 알고리즘
- DFS에 비해 사이클이 있는 그래프의 경우도 안정적으로 탐색이 가능하고, 순차적으로 탐색하는 특성 덕분에
- 시작점과 끝 점 사이의 최단 경로를 찾는 데 응용할 수 있음

## 코드

- [solution.py](solution.py)
