# 연습문제 — LCS와 편집 거리

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [AtCoder — LCS](https://atcoder.jp/contests/dp/tasks/dp_f) | 핵심 연습 | 두 문자열의 접두 길이를 상태로 두고 수열을 복원한다 |
| 2 | [CSES — Edit Distance](https://cses.fi/problemset/task/1639) | 핵심 연습 | 삽입·삭제·대체를 포함하는 편집 거리로 확장한다 |
| 3 | [LeetCode 1143 Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) | 기본형 | 같은 문제. 두 행으로 공간 줄이기 (`lcs_length`) |
| 4 | [LeetCode 72 Edit Distance](https://leetcode.com/problems/edit-distance/) | 편집 거리 | 삽입·삭제·교체. `edit_distance` |
| 5 | [LeetCode 1092 Shortest Common Supersequence](https://leetcode.com/problems/shortest-common-supersequence/) | 복원 응용 | LCS 표를 따라가며 공통 글자는 한 번, 나머지는 각각 넣는다. `shortest_common_supersequence` |
| 6 | [LeetCode 583 Delete Operation for Two Strings](https://leetcode.com/problems/delete-operation-for-two-strings/) | 응용 | 삭제만 허용한 편집 거리 = `len(a) + len(b) − 2·LCS` |
| 7 | [LeetCode 516 Longest Palindromic Subsequence](https://leetcode.com/problems/longest-palindromic-subsequence/) | 변환 | 문자열과 그 뒤집은 문자열의 LCS. 또는 [구간 DP](../interval-dp/) |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
