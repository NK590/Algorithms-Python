---
level: 1
order: 5
tags: [tree, traversal]
prerequisites: [tree, dfs]
time: O(n)
space: O(h)
status: migrated
---

# Tree Traversal (트리 순회)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

## 개요 (기존 주석에서 옮김)

- 트리 자료구조에서 각 노드를 한 번만 방문하는 방법
- 일반적으로 이진 노드를 기준으로 정의하지만, 일반적인 트리에서도 똑같이 적용 가능
- 수많은 탐색 방법이 있지만, 여기서는 전위, 중위, 후위 순회 세 가지를 작성함
- 자식 노드를 기점으로 하는 서브트리도 트리의 성질을 재귀적으로 가지고 있다는 점에 착안하면,
- 모든 순회 방법을 재귀를 통해 손쉽게 구현 가능

- 전위 순회(Preoder Traversal)
- 노드 -> 왼쪽 서브트리 -> 오른쪽 서브트리 순으로 방문

- 중위 순회(Inorder Traversal)
- 왼쪽 서브트리 -> 노드 -> 오른쪽 서브트리 순으로 방문

- 후위 순회(Postorder Traversal)
- 왼쪽 서브트리 -> 오른쪽 서브트리 -> 노드 순으로 방문

## 코드

- [solution.py](solution.py)
