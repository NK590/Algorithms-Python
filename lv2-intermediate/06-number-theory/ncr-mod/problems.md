# 연습문제 — 조합 nCr mod p

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Binomial Coefficients](https://cses.fi/problemset/task/1079) | 핵심 연습 | 팩토리얼과 역팩토리얼을 전처리한다 |
| 2 | [CSES — Distributing Apples](https://cses.fi/problemset/task/1716) | 핵심 연습 | 중복 조합을 일반 이항계수로 바꾼다 |
| 3 | [CSES — Creating Strings II](https://cses.fi/problemset/task/1715) | 핵심 연습 | 중복 문자의 팩토리얼을 분모로 나눈다 |
| 4 | [LeetCode 62 Unique Paths](https://leetcode.com/problems/unique-paths/) | 격자 경로 | 오른쪽·아래로만 가는 경로 수 = `C(m + n − 2, m − 1)`. `grid_paths_mod`와 같은 식 |
| 5 | [LeetCode 96 Unique Binary Search Trees](https://leetcode.com/problems/unique-binary-search-trees/) | 카탈란 수 | 노드 `n`개 이진 탐색 트리의 모양 수. `catalan_mod`. DP로도 풀 수 있으니 두 방법을 비교 |
| 6 | [AtCoder ABC145 D - Knight](https://atcoder.jp/contests/abc145/tasks/abc145_d) | 식 세우기 + 조합 | 두 가지 이동의 횟수를 연립방정식으로 구한 뒤 `C(a + b, a)`. 정수 해가 없으면 0 |
| 7 | [LeetCode 1569 Number of Ways to Reorder Array to Get Same BST](https://leetcode.com/problems/number-of-ways-to-reorder-array-to-get-same-bst/) | 재귀 + 조합 | 루트 이후의 왼쪽·오른쪽 서브트리 원소들을 섞는 방법 `C(l + r, l)`을 재귀로 곱한다. 원래 배열 자신은 세지 않으므로 마지막에 1을 뺀다 |
| 8 | [LeetCode 1735 Count Ways to Make Array With Product](https://leetcode.com/problems/count-ways-to-make-array-with-product/) | 소인수분해 + 별과 막대 | 곱이 `k`인 길이 `n`의 배열 수. `k`를 소인수분해해 소인수마다 중복 조합으로 지수를 나누고 곱한다 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
