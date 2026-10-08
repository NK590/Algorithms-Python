---
level: 1
order: 1
tags: [search, binary-search]
prerequisites: [array]
time: O(log n)
space: O(1)
status: migrated
---

# Binary Search (이진 탐색)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

## 개요 (기존 주석에서 옮김)

- 정렬되어 있는 리스트에서 특정 원소 값을 찾아내는 알고리즘
- 리스트를 절반씩 나눠가며 해당 값이 어느 쪽에 속해있는지 찾아가는 알고리즘으로,
- 리스트 내 극히 일부 데이터만 확인해도 탐색이 가능하며 시간복잡도가 O(logn)으로 매우 효율적
- 단, 단조증가(감소)하는 데이터에만 사용이 가능하고, 그 외에 경우에는 이분 탐색을 적용할 수 없음

## 코드

- [solution.py](solution.py)
