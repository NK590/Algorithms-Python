---
level: 3
order: 1
tags: [data-structure, tree, range-query, divide-and-conquer]
prerequisites: [tree, divide-and-conquer, prefix-sum]
time: 구축 O(n), 쿼리·갱신 O(log n)
space: O(n)
status: migrated
---

# Segment Tree (세그먼트 트리, 구간 트리)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

## 개요 (기존 주석에서 옮김)

- 트리의 특수한 케이스로, 각각의 노드가 특정 '구간값'을 보존하고 있는 이진 트리 자료구조
- 특정 구간의 구간값이 수시로 변경되며 임의의 구간값을 구해야 되는 쿼리에 유리하며,
- 특정 구간값의 갱신과 계산을 각각 시간복잡도 O(logn)으로 수행할 수 있음

## 코드

- [solution.py](solution.py)
