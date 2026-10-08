---
level: 1
order: 1
tags: [graph, data-structure]
prerequisites: [array]
status: migrated
---

# Graph (그래프)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

> **알려진 이슈** — 인접 리스트 예제의 리스트 리터럴에 쉼표가 빠져 있어, `solution.py`를 그대로 실행하면 `TypeError`가 발생합니다.

## 개요 (기존 주석에서 옮김)

- 아주 중요한 자료구조 중 하나로, 정점(Node 혹은 Vertex)과 그 정점 사이를 잇는 간선(Edge)들로 이루어진 자료구조
- 정점을 이어주는 간선이 방향성이 있냐 없냐에 따라 유향 그래프(Directed Graph), 무향 그래프(Undirected Graph)
- 등으로 나눌 수 있음
- 간선이 특정 수치를 가질 수 있는데, 이럴 경우 이를 가중치(Weighted Value)라고 함
- 응용 방식이 무궁무진하고, 구현하는 방식도 여러 가지가 있고, 여기서는 그 중 몇가지를 작성

## 코드

- [solution.py](solution.py)
