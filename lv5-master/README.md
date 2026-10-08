---
level: 5
name: 마스터
tier: Ruby
summary: Link-Cut Tree, Blossom 등 소수만 쓰는 최상위 알고리즘을 다룬다
---

# Lv5 · 마스터 (Ruby)

논문이나 대회 해설 수준의 알고리즘을 다루는 단계입니다. 대부분 Python으로 제한 시간 안에 통과하기 어려워, 개념 설명과 C++ 참고 구현 중심으로 구성할 예정입니다.

- **solved.ac 기준**: Ruby 난이도의 문제 (알고리즘별 난이도는 문제에 따라 달라 대략적인 기준입니다)
- **선수 지식**: Lv4 내용
- **이 레벨을 마치면**: 최상위 알고리즘의 핵심 아이디어를 이해한다

## 개념 목록

<!-- INDEX:START -->
### [동적 트리 (Dynamic Trees)](01-dynamic-trees/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [링크-컷 트리 (Link-Cut Tree)](01-dynamic-trees/link-cut-tree/) | `done` | 분할 상환 O(log n) (access, link, cut, 경로 질의 모두) | [splay-tree](../lv4-expert/03-advanced-data-structures/splay-tree/), [heavy-light-decomposition](../lv4-expert/02-tree-decomposition/heavy-light-decomposition/), [lca](../lv3-advanced/03-graph-advanced/lca/) |
| [탑 트리 (Top Tree) — 정적 탑 트리](01-dynamic-trees/top-tree/) | `done` | 구성 O(n), 정점 값 갱신 O(log n) (클러스터 트리의 깊이) | [heavy-light-decomposition](../lv4-expert/02-tree-decomposition/heavy-light-decomposition/), [link-cut-tree](01-dynamic-trees/link-cut-tree/), [tree-dp](../lv2-intermediate/03-trees/tree-dp/) |
<!-- INDEX:END -->

이 레벨에서 다룰 예정인 주제는 [ROADMAP](../ROADMAP.md)에서 볼 수 있습니다.
