---
level: 2
order: 3
tags: [graph, shortest-path, dp]
prerequisites: [graph]
time: O(V^3)
space: O(V^2)
status: migrated
---

# Floyd-Warshall Algorithm (플로이드-워셜 알고리즘)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

## 개요 (기존 주석에서 옮김)

- 정점 V개와 그 정점들을 잇는 가중치가 있는 변 E개로 이루어진 가중 그래프가 주어졌을 떄,
- 그 그래프 내에서 최단경로를 찾는 알고리즘
- 한 번의 계산으로 모든 정점 쌍 사이의 최단 거리를 구해내고, 변이 음의 가중치일 때도 계산 가능
- 3중 반복문 DP로 구현하며, 시간복잡도는 O(V^3)로 다소 좋지 않은 편이라 상황에 따라 다른 알고리즘 도입이 필요

## 코드

- [solution.py](solution.py)
