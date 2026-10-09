# 연습문제 — 느리게 갱신되는 세그먼트 트리

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Range Updates and Sums](https://cses.fi/problemset/task/1735) | 핵심 연습 | 구간 대입과 더하기의 합성 순서를 구분한다 |
| 2 | [AtCoder — Range Affine Range Sum](https://atcoder.jp/contests/practice2/tasks/practice2_k) | 핵심 연습 | 아핀 변환을 갱신 연산으로 일반화한다 |
| 3 | [AOJ — Range Add Query](https://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=DSL_2_G) | 핵심 연습 | 구간 더하기와 구간 합을 구현한다 |
| 4 | [LeetCode 699 Falling Squares](https://leetcode.com/problems/falling-squares/) | 구간 대입 + 구간 최댓값 | 떨어진 사각형의 윗면이 구간의 높이가 된다. 좌표 압축 + 대입 갱신 |
| 5 | [LeetCode 732 My Calendar III](https://leetcode.com/problems/my-calendar-iii/) | 구간 더하기 + 전체 최댓값 | 겹치는 일정의 최대 개수. 동적 개설이거나 좌표 압축 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
