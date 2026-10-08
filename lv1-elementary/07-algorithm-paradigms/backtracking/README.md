---
level: 1
order: 2
tags: [paradigm, backtracking, search]
prerequisites: [brute-force, dfs]
status: migrated
---

# Backtracking (백트래킹)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

## 개요 (기존 주석에서 옮김)

- 특정 조건을 만족하는 해답을 찾기위한 일련의 탐색 과정
- 주어진 조건에 맞게 탐색을 하다 해답이 아니면 도중에 되돌아가서 다른 경로를 탐색하는 방식으로,
- 그 특성상 DFS가 주로 사용되나, 제한적으로 BFS가 사용될 수도 있음
- 전수조사를 하게 되면 탐색해야 되는 경우의 수가 일반적으로 매우 커지므로,
- 문제에서 주어지는 각종 제약 조건을 잘 활용하여 탐색하는 가지수를 줄여나가는 게 중요

## 코드

- [solution.py](solution.py)
