# 연습문제 — 확장 유클리드 호제법

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [AtCoder — Throne](https://atcoder.jp/contests/abc186/tasks/abc186_e) | 핵심 연습 | 선형 합동식의 해 존재 조건과 역원을 구한다 |
| 2 | [LeetCode 1250 Check If It Is a Good Array](https://leetcode.com/problems/check-if-it-is-a-good-array/) | 베주 항등식 | 정수 결합으로 1을 만들 수 있는가 ⟺ 전체 gcd가 1. 구현 없이 항등식만 알아도 풀린다 |
| 3 | [LeetCode 365 Water and Jug Problem](https://leetcode.com/problems/water-and-jug-problem/) | 베주 항등식 | 두 물통으로 `z`리터를 만들 수 있는가 ⟺ `z`가 두 용량의 `gcd`의 배수이고 `z ≤ x + y` |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
