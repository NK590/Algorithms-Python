# 연습문제 — LCS와 편집 거리

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 9251 LCS](https://www.acmicpc.net/problem/9251) | 기본형 | LCS의 길이. [solution.py](solution.py)의 `main()`이 같은 형태를 처리한다 |
| 2 | [LeetCode 1143 Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) | 기본형 | 같은 문제. 두 행으로 공간 줄이기 (`lcs_length`) |
| 3 | [백준 9252 LCS 2](https://www.acmicpc.net/problem/9252) | 복원 | 길이와 문자열을 모두 출력. `lcs_string` |
| 4 | [LeetCode 72 Edit Distance](https://leetcode.com/problems/edit-distance/) | 편집 거리 | 삽입·삭제·교체. `edit_distance` |
| 5 | [백준 5582 공통 부분 문자열](https://www.acmicpc.net/problem/5582) | 부분 문자열 | 연속해야 한다. 다르면 0으로 끊긴다. `longest_common_substring` |
| 6 | [LeetCode 1092 Shortest Common Supersequence](https://leetcode.com/problems/shortest-common-supersequence/) | 복원 응용 | LCS 표를 따라가며 공통 글자는 한 번, 나머지는 각각 넣는다. `shortest_common_supersequence` |
| 7 | [LeetCode 583 Delete Operation for Two Strings](https://leetcode.com/problems/delete-operation-for-two-strings/) | 응용 | 삭제만 허용한 편집 거리 = `len(a) + len(b) − 2·LCS` |
| 8 | [백준 17218 비밀번호 만들기](https://www.acmicpc.net/problem/17218) | 복원 | 두 문자열의 LCS 하나를 출력 |
| 9 | [LeetCode 516 Longest Palindromic Subsequence](https://leetcode.com/problems/longest-palindromic-subsequence/) | 변환 | 문자열과 그 뒤집은 문자열의 LCS. 또는 [구간 DP](../interval-dp/) |

## 풀이 메모

- 1번과 3번에서 `dp[i][j]`의 정의를 한 문장으로 써 두고 점화식을 유도하세요.
- 5번은 점화식에서 `max(위, 왼쪽)` 부분이 **0**으로 바뀝니다. 이 차이가 부분 수열과 부분 문자열을 가릅니다. 정답은 표 전체의 최댓값입니다.
- 4번의 세 연산(교체/삭제/삽입)이 표의 대각선/위/왼쪽에 대응하는 것을 [README](README.md)의 표(kitten → sitting)로 직접 확인하세요.
- 9번을 LCS로 풀면 O(n²) 공간입니다. n이 크면 두 행으로 줄이고 길이만 구하세요.
