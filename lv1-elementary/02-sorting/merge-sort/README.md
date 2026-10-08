---
level: 1
order: 4
tags: [sorting, comparison-sort, divide-and-conquer]
prerequisites: [array]
time: O(n log n)
space: O(n)
status: migrated
---

# Merge Sort (병합 정렬)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

> **알려진 이슈** — 병합 단계에서 `<`로 비교해 값이 같을 때 오른쪽 원소를 먼저 넣으므로 안정 정렬이 아닙니다. `<=`로 바꾸면 안정 정렬이 됩니다.

## 개요 (기존 주석에서 옮김)

- 분할 정복을 이용한 재귀 정렬 알고리즘으로 O(nlogn)의 시간 복잡도를 가짐
- 주어진 리스트를 먼저 길이가 1이 될 때까지 절반으로 쪼갠 뒤 합치는 과정에서 순서에 맞게 정렬
- 쪼갠 데이터를 보관할 메모리가 필요하므로, 메모리 측면에선 비효율적

## 코드

- [solution.py](solution.py)
