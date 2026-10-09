# 연습문제 — 중간에서 만나기

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Apple Division](https://cses.fi/problemset/task/1623) | 핵심 연습 | 부분집합을 두 절반으로 나눠 합을 결합한다 |
| 2 | [CSES — Sum of Four Values](https://cses.fi/problemset/task/1642) | 핵심 연습 | 두 쌍의 합을 결합하되 인덱스 중복을 제외한다 |
| 3 | [LeetCode 1755 Closest Subsequence Sum](https://leetcode.com/problems/closest-subsequence-sum/) | 목표에 가장 가까운 합 | `n ≤ 40`, 음수 가능. `closest_subset_sum`의 기본형. 빈 부분수열이 허용된다 |
| 4 | [LeetCode 2035 Partition Array Into Two Arrays to Minimize Sum Difference](https://leetcode.com/problems/partition-array-into-two-arrays-to-minimize-sum-difference/) | 두 배열로 나눠 합의 차 최소화 | 원소 `2n ≤ 30`. 각 절반에서 *고른 개수별*로 합을 나열해 맞춘다 |
| 5 | [LeetCode 805 Split Array With Same Average](https://leetcode.com/problems/split-array-with-same-average/) | 평균이 같은 두 부분으로 나누기 | 개수별 합 집합 + 평균 조건을 정수로 바꾸는 법 |
| 6 | [Codeforces 1006F Xor-Paths](https://codeforces.com/problemset/problem/1006/F) | 격자 경로의 XOR | 출발점과 도착점에서 중간 대각선까지 각각 탐색해 대각선에서 만난다 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
