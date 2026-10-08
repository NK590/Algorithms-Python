---
level: 1
order: 2
tags: [number-theory, gcd, coprime]
prerequisites: [euclidean-algorithm]
time: O(log min(a, b))
status: migrated
---

# Relatively Prime (서로소, Coprime)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

## 개요 (기존 주석에서 옮김)

- 두 수가 주어졌을 때, 두 수의 공약수가 1 이외에 없을 경우 두 수는 서로소라고 함
- 두 수가 주어졌을 떄, 두 수의 최소공배수가 두 수의 곱일 경우와 동치임
- 유클리드 호제법을 이용하여 최대공약수가 1임을 확인함으로서 찾을 수 있음

## 코드

- [solution.py](solution.py)
