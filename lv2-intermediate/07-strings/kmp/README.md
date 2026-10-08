---
level: 2
order: 1
tags: [string, pattern-matching]
prerequisites: []
time: O(n+m)
space: O(m)
status: migrated
---

# KMP Algorithm (KMP 알고리즘)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

## 개요 (기존 주석에서 옮김)

- 주어진 문자열(이하 word)에 어떤 문자열(이하 test)이 있는지 검색하는 대표적인 문자열 탐색 알고리즘
- 먼저 test 문자열의 접두사와 접미사 중에 같은 문자열이 있는지 확인하여 LPS(Longest Prefix & Suffix)
- 리스트를 작성함
- word 문자열의 처음부터 부분 문자열이 test 문자열과 일치하는 지 확인한 뒤, 일치할 경우 문제 조건에 따라
- 적당한 값을 출력하고 일치하지 않을 경우 위 LPS 리스트 값에 따라 word 문자열에서 체크할 값을 '건너뛰어서'
- 건너뛴 값 이후로 위 탐색을 반복함

- word의 길이를 n, test의 길이를 m이라고 하면 일반적인 이중 반복문 탐색은 시간 복잡도가 O(n\*m)이지만,
- KMP 알고리즘을 사용하면 시간 복잡도를 O(n+m)으로 획기적으로 줄일 수 있음

## 코드

- [solution.py](solution.py)
