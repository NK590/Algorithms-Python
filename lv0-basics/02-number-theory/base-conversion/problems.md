# 연습문제 — 진법 변환

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [AOJ — Sum of Numbers](https://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_8_B) | 선행 연습 | 십진수의 각 자릿수를 추출하고 합한다 |
| 2 | [LeetCode 504 — Base 7](https://leetcode.com/problems/base-7/) | 핵심 연습 | 7로 나눈 나머지를 뒤집어 읽고 0과 음수의 부호를 처리한다 |
| 3 | [LeetCode 405 — Convert a Number to Hexadecimal](https://leetcode.com/problems/convert-a-number-to-hexadecimal/) | 심화·응용 | 16진 자릿수와 음수의 32비트 2의 보수 표현을 구분한다 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
