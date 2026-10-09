# 연습문제 — 하노이의 탑과 재귀

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Tower of Hanoi](https://cses.fi/problemset/task/2165) | 핵심 연습 | 이동 횟수와 실제 이동 목록을 재귀로 구성한다 |
| 2 | [CSES — Creating Strings](https://cses.fi/problemset/task/1622) | 심화·응용 | 심화로 재귀 호출 트리를 서로 다른 열거 문제와 비교한다 |
| 3 | [LeetCode 779 K-th Symbol in Grammar](https://leetcode.com/problems/k-th-symbol-in-grammar/) | k번째만 | 전체를 만들지 않고 위 줄의 어느 칸에서 왔는지로 내려간다. `hanoi_kth_move`와 같은 발상 |
| 4 | [LeetCode 50 Pow(x, n)](https://leetcode.com/problems/powx-n/) | 반으로 줄이기 | `x^n = (x^(n/2))²`. 재귀 깊이가 log n → [빠른 거듭제곱](../../../lv2-intermediate/05-divide-and-conquer/fast-exponentiation/) |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
