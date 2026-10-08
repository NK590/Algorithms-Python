---
level: 1
order: 3
tags: [number-theory, prime, sieve]
prerequisites: [naive-prime-check]
time: O(n log log n)
space: O(n)
status: migrated
---

# Sieve of Eratosthenes (에라토스테네스의 체)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

> **알려진 이슈** — 아래 개요는 시간 복잡도를 `O(nlogn)`이라고 하지만, 올바른 값은 `O(n log log n)`입니다.

## 개요 (기존 주석에서 옮김)

- 특정 수 범위 내의 소수를 구하는 알고리즘
- 작은 수부터 차근차근 그 수의 배수들을 지워나가는 모습이 마치 체로 숫자를 걸러내는 듯하여 이런 이름이 붙음
- 시간 복잡도는 일반적으로 O(nlogn)이나, 조금 더 개선된 알고리즘이 존재함

## 코드

- [solution.py](solution.py)
