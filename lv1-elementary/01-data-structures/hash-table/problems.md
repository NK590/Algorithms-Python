# 연습문제 — 해시 테이블

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Sum of Two Values](https://cses.fi/problemset/task/1640) | 핵심 연습 | 현재 수의 보수를 이전 원소의 해시에서 찾는다 |
| 2 | [CSES — Subarray Sums II](https://cses.fi/problemset/task/1661) | 핵심 연습 | 누적 합의 등장 횟수를 사전에 저장한다 |
| 3 | [CSES — Distinct Numbers](https://cses.fi/problemset/task/1621) | 핵심 연습 | 중복 제거와 해시 충돌의 영향을 구분한다 |
| 4 | [LeetCode 1 Two Sum](https://leetcode.com/problems/two-sum/) | 보수 찾기 | 이미 본 값을 기록하고 `target − x`가 있는지 본다 (`two_sum`) |
| 5 | [LeetCode 49 Group Anagrams](https://leetcode.com/problems/group-anagrams/) | 키 설계 | 글자를 정렬한 문자열을 키로 써서 같은 구성끼리 묶는다 (`group_anagrams`) |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
