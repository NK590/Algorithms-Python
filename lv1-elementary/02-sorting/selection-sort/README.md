---
level: 1
order: 2
tags: [sorting, comparison-sort]
prerequisites: [array]
time: O(n^2)
space: O(1)
status: migrated
---

# Selection Sort (선택 정렬)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

## 개요 (기존 주석에서 옮김)

- 인접한 원소들끼리만 비교해서 교환하는 버블 정렬과 다르게 처음부터 끝까지 한번 훑은 다음,
- 제일 작은 원소를 맨 앞으로 보내는 것을 반복하는 알고리즘
- 버블 정렬과 비슷하게 시간 복잡도는 O(n^2)로 비효율적

## 코드

- [solution.py](solution.py)
