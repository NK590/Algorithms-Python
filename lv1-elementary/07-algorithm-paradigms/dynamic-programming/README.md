---
level: 1
order: 3
tags: [paradigm, dp]
prerequisites: [array, brute-force]
status: migrated
---

# Dynamic Programming (다이나믹 프로그래밍, 동적 계획법)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

## 개요 (기존 주석에서 옮김)

- 기존의 해법을 이용하여 새로운 문제를 해결하는 패러다임
- 같은 풀이를 지속적으로 사용하여 다른 문제를 해결해야 하는 상황에서, 기존의 데이터를 재활용하여
- 새로운 문제에 접목시켜 푸는 시간을 줄일 수 있음
- 주로 하위 문제의 답 데이터를 따로 저장하여, 같은 문제를 반복해서 풀지 않고 필요할 때마다
- 그 데이터를 참조하여 상위 문제를 푸는 형식으로 응용

## 코드

- [solution.py](solution.py)
