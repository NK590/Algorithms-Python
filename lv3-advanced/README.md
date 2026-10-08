---
level: 3
name: 고급
tier: Platinum
summary: 구간 질의 자료구조, 고급 그래프(SCC·플로우), 문자열·기하 도구를 익힌다
---

# Lv3 · 고급 (Platinum)

여러 알고리즘을 조합하거나 자료구조를 직접 설계해야 풀리는 문제들이 나오는 단계입니다. Python으로는 시간 제한이 빠듯해지므로 구현 최적화도 함께 다룹니다.

- **solved.ac 기준**: Platinum 난이도의 문제 (알고리즘별 난이도는 문제에 따라 달라 대략적인 기준입니다)
- **선수 지식**: Lv2 내용 (트리, 분할 정복, 모듈러 연산)
- **이 레벨을 마치면**: 세그먼트 트리 같은 자료구조를 직접 구현해 쿼리 문제를 풀 수 있다

## 개념 목록

<!-- INDEX:START -->
### [구간 질의 자료구조 (Range Query Structures)](01-range-query-structures/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Segment Tree (세그먼트 트리, 구간 트리)](01-range-query-structures/segment-tree/) | `migrated` | 구축 O(n), 쿼리·갱신 O(log n) | [tree](../lv1-elementary/05-graph-basics/tree/), [divide-and-conquer](../lv2-intermediate/05-divide-and-conquer/divide-and-conquer/), [prefix-sum](../lv1-elementary/04-range-techniques/prefix-sum/) |

### [정수론 (Number Theory)](02-number-theory/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Extended Euclidean Algorithm (확장 유클리드 호제법)](02-number-theory/extended-euclidean-algorithm/) | `migrated` | O(log min(a, b)) | [euclidean-algorithm](../lv1-elementary/06-number-theory/euclidean-algorithm/) |
<!-- INDEX:END -->

이 레벨에서 다룰 예정인 주제는 [ROADMAP](../ROADMAP.md)에서 볼 수 있습니다.
