---
level: 2
order: 1
tags: [paradigm, divide-and-conquer, recursion]
prerequisites: [tower-of-hanoi, merge-sort]
status: migrated
---

# Divide and Conquer (분할 정복)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

## 개요 (기존 주석에서 옮김)

- 주어진 문제를 보다 작은 문제로 쪼개서, 그 작은 문제들을 해결하여 합쳐서 주어진 문제를 해결하는 패러다임
- 일반적으로 원래 문제와 구조는 동일하고, 더 풀기 쉬운 작은 문제로 분할하여 재귀적으로 풀어나감
- 병합 정렬, 퀵 정렬의 구현에서도 분할 정복 해법이 사용됨

## 코드

- [solution.py](solution.py)
