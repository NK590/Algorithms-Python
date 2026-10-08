---
level: 2
order: 2
tags: [string, pattern-matching, hash]
prerequisites: [hash-table]
time: 평균 O(n+m), 최악 O(nm)
status: stub
---

# Rabin-Karp Algorithm (라빈-카프 알고리즘)

> **상태: `stub`** — 개념 설명만 있고 구현 코드는 아직 없습니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

## 개요 (기존 주석에서 옮김)

- 주어진 문자열(이하 word)에 어떤 문자열(이하 test)이 있는지 검색하는 탐색 알고리즘
- 해시 함수를 이용하는 것이 특징으로, test 문자열의 해시 값과 word 문자열의 부분 문자열의 해시 값을
- 비교하여 해시 값이 같은 부분 문자열을 찾아냄
- 해시 함수를 적절하게 설정하여 해시 충돌을 줄이면 탐색 시간을 효율적으로 줄일 수 있음

## 코드

구현은 아직 없습니다. [solution.py](solution.py)에는 설명 주석만 있습니다.
