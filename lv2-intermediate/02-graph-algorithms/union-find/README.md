---
level: 2
order: 1
tags: [data-structure, disjoint-set, graph]
prerequisites: [tree]
time: 연산당 거의 O(1) (분할 상환 O(α(n)))
space: O(n)
status: migrated
---

# Union-Find (유니온 파인드, Disjoint Set - 서로소 집합)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

## 개요 (기존 주석에서 옮김)

- 상호 배타적으로 이루어진(=교집합이 없는) 집합을 관리하는 트리 형태의 자료 구조
- 서로 다른 두 집합을 병합하는 Union 연산, 특정 원소가 어떤 집합에 속해있는지 판단하는 Find 연산을 지원

## 코드

- [solution.py](solution.py)
