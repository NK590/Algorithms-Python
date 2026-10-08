---
level: 0
order: 1
tags: [number-theory, prime]
prerequisites: []
time: O(√n)
space: O(1)
status: migrated
---

# Naive Prime Number Check (단순 소수 판별)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

## 개요 (기존 주석에서 옮김)

- 어떤 주어진 수 a가 소수인지 판별하는 가장 단순한 방법은, 2에서 a-1까지 모든 수로 나눠보면서
- 나누어 떨어지는 수가 있는지 알아보고, 나누어 떨어지는 수가 하나라도 있으면 소수가 아니고,
- 하나도 없으면 소수라고 할 수 있음
- 여기서, 만약 a가 i로 나누어 떨어진다면 a는 a/i로도 나누어 떨어진다는 점을 생각해보면,
- 2부터 sqrt(a)까지의 수만 체크해보면 됨

## 코드

- [solution.py](solution.py)
