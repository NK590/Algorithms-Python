---
level: 2
order: 2
tags: [number-theory, modular, prime]
prerequisites: [euclidean-algorithm, relatively-prime]
status: migrated
---

# Fermat's Little Theorem (페르마의 소정리)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

## 개요 (기존 주석에서 옮김)

- 정수 a, 소수 p가 있고 a가 p의 배수가 아닐 시, a^p를 p로 나눈 나머지는 a임이 알려져 있음
- 혹은, a^(p-1)를 p로 나눈 나머지가 1이라는 식으로도 표현 가능
- 이 정리의 역은 일반적으로 성립하지 않음

- 모듈로 곱셈의 역원을 양의 정수로 돌려놓을 때 이 정리가 사용됨

## 코드

- [solution.py](solution.py)
