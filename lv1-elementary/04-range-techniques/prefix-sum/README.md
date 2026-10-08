---
level: 1
order: 1
tags: [range-query, prefix-sum, dp]
prerequisites: [array]
time: 전처리 O(n), 구간 합 쿼리 O(1)
space: O(n)
status: migrated
---

# Prefix Sum (구간 합)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

## 개요 (기존 주석에서 옮김)

- 일반적으로 주어진 리스트의 특정 연속된 구간의 합을 구하는 데에 걸리는 시간 복잡도는 O(n)이지만,
- 리스트의 첫번째 원소부터 i번째 원소까지의 합을 DP를 이용하여 미리 구해놓는 전처리 작업을 해두면
- 임의의 연속된 구간의 합을 이 합 리스트의 두 원소를 빼는 식으로 O(1)만에 구할 수 있음
- 쿼리가 많아지면 많아질수록 효율적이고, 이와 같은 아이디어는 다양한 분야에 응용됨

## 코드

- [solution.py](solution.py)
