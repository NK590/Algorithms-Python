---
level: 2
order: 1
tags: [graph, shortest-path, heap, greedy]
prerequisites: [bfs, priority-queue]
time: O((V+E) log V)
space: O(V+E)
status: migrated
---

# Dijkstra's Algorithm (다익스트라 알고리즘)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

## 개요 (기존 주석에서 옮김)

- 정점 V개와 그 정점들을 잇는 가중치가 있는 변 E개로 이루어진 가중 그래프가 주어졌을 떄,
- 그 그래프 내에서 특정 정점에서 다른 정점까지의 최단경로를 찾는 알고리즘
- 시작 정점에서부터 인접한 정점을 하나씩 확인하여 해당 정점까지의 거리를 갱신해 나가며
- 경로를 찾는 알고리즘으로, 벨만-포드 알고리즘의 특수한 버전이라고 볼 수 있음
- 음의 가중치 간선이 있을 때는 사용이 불가능하지만, 플로이드-워셜이나 벨만-포드 알고리즘에 비해
- 매우 빠른 알고리즘이라 자주 사용됨
- 구현 시 우선순위 큐를 사용하고, 시간 복잡도는 일반적으로 O((V+E)logV)임

## 코드

- [solution.py](solution.py)
