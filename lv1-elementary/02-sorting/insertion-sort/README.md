---
level: 1
order: 3
tags: [sorting, comparison-sort]
prerequisites: [array]
time: O(n^2)
space: O(1)
status: migrated
---

# Insertion Sort (삽입 정렬)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

## 개요 (기존 주석에서 옮김)

- k번째 원소를 1 ~ k-1번째 원소와 비교해서 정렬 순서에 맞는 적절한 위치에 끼위넣는 알고리즘
- 시간복잡도는 O(n^2)이나, n이 작을 떄는 매우 좋은 퍼포먼스를 보여줌
- 단, 자료 구조에 따라 원소를 끼워넣는 과정에서 다른 원소를 밀어내는 데 많은 시간이 걸릴 수 있음

## 코드

- [solution.py](solution.py)
