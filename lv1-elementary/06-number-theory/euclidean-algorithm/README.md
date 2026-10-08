---
level: 1
order: 1
tags: [number-theory, gcd]
prerequisites: []
time: O(log min(a, b))
status: migrated
---

# Euclidean Algorithm (유클리드 호제법)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

## 개요 (기존 주석에서 옮김)

- 두 양의 정수의 최대공약수(Great Common Divisor, GCD)를 구하는 알고리즘
- a, b를 각각 두 양의 정수라 하고, a = bq + r (0 <= r < b)라 하면,
- a, b의 최대공약수는 b, r의 최대공약수와 같은 성질을 이용, 두 수를 바꿔가며 서로를 나눠서
- 최대공약수를 구하는 방식으로 사용됨

## 코드

- [solution.py](solution.py)
