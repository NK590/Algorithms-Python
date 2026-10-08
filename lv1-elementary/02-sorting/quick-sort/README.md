---
level: 1
order: 5
tags: [sorting, comparison-sort, divide-and-conquer]
prerequisites: [array]
time: 평균 O(n log n), 최악 O(n^2)
status: migrated
---

# Quick Sort (퀵 소트)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

> **알려진 이슈** — `Quick_Sort`(예시 코드 1)는 값이 중복된 입력(예: `[5, 5]`)에서 `RecursionError`가 발생합니다. 기준값과 같은 원소들의 리스트(`pivot_li`)를 다시 재귀 호출하기 때문입니다.

## 개요 (기존 주석에서 옮김)

- 특정 축(Pivot)을 설정하여 그 축을 기준으로 축 앞쪽에서 축보다 큰 갚은 축 뒤로,
- 축 뒤쪽에서 축보다 작은 값은 축 뒤쪽으로 보내는 걸 반복해서 정렬하는 알고리즘.
- 이름에서 알 수 있듯이 평균적으로 빠른 정렬 알고리즘(O(nlogn))으로, 많은 언어에서
- 자체 제공하는 정렬 함수에서 사용하는 알고리즘임

## 코드

- [solution.py](solution.py)
