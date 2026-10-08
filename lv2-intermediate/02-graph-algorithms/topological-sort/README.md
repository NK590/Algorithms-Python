---
level: 2
order: 2
tags: [graph, dag, sorting]
prerequisites: [graph, bfs]
time: O(V+E)
space: O(V)
status: migrated
---

# Topological Sort (위상 정렬)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

## 개요 (기존 주석에서 옮김)

- 주어진 비순환 유향 그래프에서 각 정점을 특정 방향으로 맞춰서 정렬하는 방법
- 정의에서 알 수 있듯이 그래프 내 사이클이 존재하거나, 무향 그래프일 경우 위상 정렬이 불가능함
- 역으로, 이 성질을 이용하여 주어진 그래프 내 사이클이 존재하는지 위상 정렬로 찾아낼 수 있음

- 특정 데이터와 그 데이터 세그먼트들 사이의 '방향'이 주어졌을 때,
- 그 데이터들을 주어진 '방향'에 맞춰서 한 줄로 '정렬'하는 경우에 사용이 됨
- 진입 차수(Indegree), 진출 차수(Outdegree)를 이용해 큐를 이용하는 BFS 구현법과
- 스택을 이용한 DFS 구현법 등이 있음

## 코드

- [solution.py](solution.py)
