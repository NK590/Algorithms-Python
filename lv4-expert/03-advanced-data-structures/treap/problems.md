# 연습문제 — 트립

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [Library Checker — Range Reverse Range Sum](https://judge.yosupo.jp/problem/range_reverse_range_sum) | 핵심 연습 | 위치 기반 분할·병합과 뒤집기 지연 표시를 결합한다 |
| 2 | [Library Checker — Dynamic Sequence Range Affine Range Sum](https://judge.yosupo.jp/problem/dynamic_sequence_range_affine_range_sum) | 핵심 연습 | 합성 가능한 구간 갱신으로 확장한다 |
| 3 | [SPOJ ORDERSET - Order statistic set](https://www.spoj.com/problems/ORDERSET/) | 삽입·삭제·`k`번째·순위 | `OrderedMultiset`의 기본 연산. 중복을 허용하지 않는 집합이므로 `count`로 먼저 확인하고 넣는다 |
| 4 | [Codeforces 863D Yet Another Array Queries Problem](https://codeforces.com/problemset/problem/863/D) | 구간 순환 이동·뒤집기 후 몇 개 위치의 값 | 순환 이동은 `move`(잘라 붙이기)로. 질의 수가 적으면 거꾸로 위치를 추적하는 `O(q)` 풀이도 있다 |
| 5 | [Codeforces 702F T-Shirts](https://codeforces.com/problemset/problem/702/F) | 사람마다 가진 돈 안에서 티셔츠를 사는 시뮬레이션 | 값(남은 돈)을 키로 하는 트립에 구간 빼기 태그. 값이 변한 뒤 순서가 어긋나는 부분을 떼어 다시 삽입하는 고난도 응용 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
