# 연습문제 — 스위핑

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Restaurant Customers](https://cses.fi/problemset/task/1619) | 핵심 연습 | 입장·퇴장 이벤트의 같은 시각 처리 규칙을 정한다 |
| 2 | [CSES — Movie Festival](https://cses.fi/problemset/task/1629) | 핵심 연습 | 끝 시각 정렬과 구간 선택을 연결한다 |
| 3 | [LeetCode 56 Merge Intervals](https://leetcode.com/problems/merge-intervals/) | 구간 합치기 | 시작점 정렬 + 끝은 `max`. 맞닿은 구간(`[1,4]`, `[4,5]`)도 합친다 |
| 4 | [LeetCode 57 Insert Interval](https://leetcode.com/problems/insert-interval/) | 구간 삽입 | 이미 정렬·병합된 목록에 하나를 넣는 `O(n)` 스위핑 |
| 5 | [LeetCode 986 Interval List Intersections](https://leetcode.com/problems/interval-list-intersections/) | 두 목록의 교집합 | 정렬된 두 목록을 투 포인터로 훑기 |
| 6 | [LeetCode 218 The Skyline Problem](https://leetcode.com/problems/the-skyline-problem/) | 스카이라인 | 같은 `x`의 시작/끝 이벤트 순서와 힙 지연 삭제 |
| 7 | [LeetCode 850 Rectangle Area II](https://leetcode.com/problems/rectangle-area-ii/) | 직사각형 합집합 | 직사각형 최대 200개. 띠 방법(`rectangle_union_area`)으로 풀리고 `mod 10⁹+7` 출력 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
