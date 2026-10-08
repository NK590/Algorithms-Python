---
level: 2
order: 2
tags: [graph, shortest-path, dp]
prerequisites: [graph]
time: O(VE)
space: O(V)
status: migrated
---

# Bellman-Ford Algorithm (벨만-포드 알고리즘)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

## 개요 (기존 주석에서 옮김)

- 정점 V개와 그 정점들을 잇는 가중치가 있는 변 E개로 이루어진 가중 그래프가 주어졌을 떄,
- 그 그래프 내에서 특정 정점에서 다른 정점까지의 최단경로를 찾는 알고리즘
- 변이 음의 가중치를 가지고 있을 때도 사용이 가능하고, 응용해서 음의 사이클을 찾아내는 데 응용이 가능
- 인접 간선을 검사하고 가중치 합을 갱신하는 과정을 제한하여, 특정 회수 이상 반복 시에도 루프가 발생하면
- 음의 사이클이 존재한다고 판정
- 모든 정점에 대해 그 정점에서 나오는 간선을 전부 검사하는 이중 반복문으로 구현되고, 시간복잡도는 O(VE)

## 코드

- [solution.py](solution.py)
