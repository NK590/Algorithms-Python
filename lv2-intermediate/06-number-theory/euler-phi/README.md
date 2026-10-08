---
level: 2
order: 1
tags: [number-theory, totient, factorization]
prerequisites: [prime-factorization, relatively-prime]
time: O(√n)
status: migrated
---

# Euler's Phi Function (오일러 피 함수, Euler's Totient Function)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

## 개요 (기존 주석에서 옮김)

- 어떤 양의 정수 N이 주어졌을 때, N 미만의 양의 정수에 대해 N과 서로소인 숫자의 개수를 세는 함수
- 단독으로 이용된다기보단 오일러 정리 등 다른 정수론 이론에 응용되어 사용됨

- N 미만의 모든 수를 N과 유클리드 호제법을 사용하여 구현할 수도 있지만 매우 비효율적이고,
- 일반적으로 구현 시 다음 피 함수의 성질들이 이용됨

1. p가 소수일 때, Phi(p) = p - 1
2. 1.의 일반화로, p가 소수이고 k가 1 이상의 정수일 때, Phi(p^k) = p^(k) - p^(k-1)
3. m과 n이 서로소일 때, Phi(m\*n) = Phi(m) \* Phi(n)

## 코드

- [solution.py](solution.py)
