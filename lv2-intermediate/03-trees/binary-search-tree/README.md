---
level: 2
order: 1
tags: [data-structure, tree, bst]
prerequisites: [tree, binary-search]
time: 평균 O(log n), 최악 O(n)
status: stub
---

# Binary Search Tree (이진 탐색 트리)

> **상태: `stub`** — 개념 설명만 있고 구현 코드는 아직 없습니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

## 개요 (기존 주석에서 옮김)

- 아래의 조건을 만족하는 특수한 이진 트리
1. 모든 노드에 대해서, 왼쪽에 자식이 있다면 왼쪽 자식의 키 값보다 자신의 키 값이 커야 됨
2. 모든 노드에 대해서, 오른쪽에 자식이 있다면 오른쪽 자식의 키 값보다 자신의 키 값이 작아야 됨
3. 자식의 키 값과 자신의 키 값이 같을 경우는 필요에 따라 왼쪽 자식에 넣을 수도 있고
- 오른쪽 자식에 넣을 수도 있지만, 왼쪽에서 오른쪽으로 가면서 값이 작아지면 안 됨
- 이진 탐색 트리를 순회할 때는 중위 순회(Inorder Traversal)를 사용하고, 중위 순회를 사용 시
- 트리 내의 모든 값을 정렬된 순서로 읽을 수 있음

## 코드

구현은 아직 없습니다. [solution.py](solution.py)에는 설명 주석만 있습니다.
