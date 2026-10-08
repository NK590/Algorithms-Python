---
level: 3
order: 1
tags: [number-theory, gcd, modular]
prerequisites: [euclidean-algorithm]
time: O(log min(a, b))
status: migrated
---

# Extended Euclidean Algorithm (확장 유클리드 호제법)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

## 개요 (기존 주석에서 옮김)

- 주어진 두 정수의 최대공약수를 찾아내는 유클리드 호제법의 확장형으로,
- 세 정수 a, b, c에 대해 ax + by = c를 만족하는 정수쌍 x, y를 찾아내는 알고리즘
- 이 방정식의 해가 존재하려면 c가 gcd(a, b)의 배수여야 하고, 특별히 c = 1일 때
- ax + by = 1의 형태로 자주 사용됨

## 코드

- [solution.py](solution.py)
