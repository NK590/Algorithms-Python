---
level: 1
order: 6
tags: [data-structure, heap, priority-queue]
prerequisites: [queue]
time: push·pop O(log n)
status: stub
---

# Priority Queue (우선순위 큐)

> **상태: `stub`** — 개념 설명만 있고 구현 코드는 아직 없습니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

## 개요 (기존 주석에서 옮김)

- 큐의 특수한 형태로, 큐와 같이 push, pop, top 연산이 존재하는 자료구조이나
- 선입선출을 따르는 큐와 달리 pop을 할 시 넣은 순서와 상관없이 데이터의 '우선순위'에 따라 나오는 자료구조
- 보통 pop 시에 데이터값에 따라 나오도록 구현
- 일반적인 큐와 달리 push, pop을 전부 시간복잡도 O(logn) 안에 수헹할 수 있어서 매우 효율적
- 구현 시에 힙 트리를 사용하나, Python에서는 heapq 라이브러리를 통해 손쉽게 사용 가능

## 코드

구현은 아직 없습니다. [solution.py](solution.py)에는 설명 주석만 있습니다.
