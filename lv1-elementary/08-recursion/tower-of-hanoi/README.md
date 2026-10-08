---
level: 1
order: 1
tags: [recursion, classic]
prerequisites: []
time: O(2^n)
status: migrated
---

# Tower of Hanoi (하노이의 탑)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

## 개요 (기존 주석에서 옮김)

- 세 개의 장대가 있고 첫 번째 장대에는 반경이 서로 다른 n개의 원판이 쌓여 있다.
- 각 원판은 반경이 큰 순서대로 쌓여있다.
- 이제 수도승들이 다음 규칙에 따라 첫 번째 장대에서 세 번째 장대로 옮기려 한다.

- 한 번에 한 개의 원판만을 다른 탑으로 옮길 수 있다.
- 쌓아 놓은 원판은 항상 위의 것이 아래의 것보다 작아야 한다.
- 이 작업을 수행하는데 필요한 이동 순서를 출력하는 프로그램을 작성하라.
- 단, 이동 횟수는 최소가 되어야 한다.

## 코드

- [solution.py](solution.py)
