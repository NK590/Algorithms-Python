---
level: 1
order: 6
tags: [sorting, comparison-sort, heap]
prerequisites: [priority-queue]
time: O(n log n)
space: O(1)
status: migrated
---

# Heap Sort (힙 정렬)

> **상태: `migrated`** — 기존 `solution.py` 상단 주석의 설명을 그대로 옮긴 초안입니다. [문서 템플릿](../../../docs/TEMPLATE/README.md)에 맞춰 다시 쓸 예정입니다.

> **알려진 이슈** — `Heapify`가 0-based 배열에서 자식 인덱스를 `2*i`, `2*i+1`로 계산합니다(올바른 값은 `2*i+1`, `2*i+2`). 그 결과 `[1, 2, 3, 4, 5, 6, 7]`이 `[1, 2, 3, 4, 5, 7, 6]`으로 정렬되는 등 일부 입력에서 틀린 결과가 나옵니다. 또한 주석의 'min heap'은 실제로는 max heap입니다.

## 개요 (기존 주석에서 옮김)

- 힙 트리(Heap Tree) 자료 구조를 이용한 정렬 방식으로, 주어진 리스트를 힙 트리 형태로 만든 뒤,
- 이를 바탕으로 원소를 정렬하는 방식. 시간복잡도는 O(nlogn)으로 퀵 정렬과 동일하나,
- 실제로는 퀵 정렬이 빠른 경우가 많고 반면 힙 정렬은 비교적 편차가 적은 안정적인 성능을 보여줌
- 선택 정렬의 최적화 버전이라고도 볼 수 있음

## 코드

- [solution.py](solution.py)
