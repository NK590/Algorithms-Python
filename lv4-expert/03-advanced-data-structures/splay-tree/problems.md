# 연습문제 — 스플레이 트리

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [Library Checker — Range Reverse Range Sum](https://judge.yosupo.jp/problem/range_reverse_range_sum) | 핵심 연습 | 원하는 구간을 회전으로 드러내고 집계한다 |
| 2 | [Library Checker — Dynamic Sequence Range Affine Range Sum](https://judge.yosupo.jp/problem/dynamic_sequence_range_affine_range_sum) | 핵심 연습 | 아핀 갱신과 지연 표시를 동적 수열에 적용한다 |
| 3 | [SPOJ ORDERSET - Order statistic set](https://www.spoj.com/problems/ORDERSET/) | 삽입·삭제·`k`번째·순위 | `SplaySet`의 기본 연산. [트립](../treap/)의 `OrderedMultiset`과 같은 문제를 두 구조로 풀어 비교 |
| 4 | [Luogu P3369 【模板】普通平衡树](https://www.luogu.com.cn/problem/P3369) | 삽입·삭제(중복 허용)·순위·`k`번째·이전·다음 | 정렬된 **다중**집합. `SplaySet`은 중복을 허용하지 않으므로 키 옆에 개수를 두거나 `(값, 번호)` 쌍으로 만들어야 한다 |
| 5 | [Luogu P3391 【模板】文艺平衡树](https://www.luogu.com.cn/problem/P3391) | 구간 뒤집기 후 최종 배열 | [solution.py](solution.py)의 `main()`이 같은 형태. 보초 노드와 지연 뒤집기의 기본 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
