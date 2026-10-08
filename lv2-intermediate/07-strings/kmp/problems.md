# 연습문제 — KMP 알고리즘

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [LeetCode 28 Find the Index of the First Occurrence in a String](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/) | 기본형 | 첫 등장 위치. 내장 `find`로도 풀리지만 `kmp_search`의 첫 원소와 같다 |
| 2 | [백준 1786 찾기](https://www.acmicpc.net/problem/1786) | 모든 등장 위치 | 등장 횟수와 위치(1부터) 출력. 공백이 포함된 입력이라 줄 단위로 읽는다. [solution.py](solution.py)의 `main()`이 같은 형태 |
| 3 | [백준 16916 부분 문자열](https://www.acmicpc.net/problem/16916) | 포함 여부 | 길이 100만의 `S`에 `P`가 부분 문자열인가. `kmp_search`가 하나라도 찾으면 1 |
| 4 | [LeetCode 459 Repeated Substring Pattern](https://leetcode.com/problems/repeated-substring-pattern/) | 반복 단위 | `n − failure[n−1]`이 `n`을 나누는지. `smallest_period`가 `n`보다 작으면 참 |
| 5 | [LeetCode 1392 Longest Happy Prefix](https://leetcode.com/problems/longest-happy-prefix/) | 테두리 | 접두사이자 접미사인 가장 긴 부분 = `failure[n−1]` 그 자체 |
| 6 | [백준 4354 문자열 제곱](https://www.acmicpc.net/problem/4354) | 반복 횟수 | `s = aⁿ`인 최대 `n`. `n = len(s) / smallest_period(s)` |
| 7 | [백준 1305 광고](https://www.acmicpc.net/problem/1305) | 가장 짧은 길이 | 전광판에 보이는 문자열에서 광고의 최소 길이 = `n − failure[n−1]` (`shortest_prefix_covering`). 나누어떨어지지 않아도 된다는 점이 4번과 다르다 |
| 8 | [백준 1701 Cubeditor](https://www.acmicpc.net/problem/1701) | 반복 부분 문자열 | 두 번 이상 나오는 가장 긴 부분 문자열. 각 접미사의 실패 함수의 최댓값 (`O(n²)`) |
| 9 | [LeetCode 214 Shortest Palindrome](https://leetcode.com/problems/shortest-palindrome/) | 실패 함수 응용 | `s + '#' + reverse(s)`의 실패 함수 마지막 값이 가장 긴 회문 접두사의 길이 |
| 10 | [백준 10266 시계 사진 찍기](https://www.acmicpc.net/problem/10266) | 원형 매칭 | 원형 배열을 두 번 이어 붙이고 KMP. 문자열이 아닌 0/1 배열에도 같은 알고리즘이 적용된다 |
| 11 | [백준 13506 카멜레온 부분 문자열](https://www.acmicpc.net/problem/13506) | 테두리 사슬 | 접두사=접미사=중간에 나오는 부분 문자열. `failure`의 사슬을 따라가며 중간에 나오는지 확인 |

## 풀이 메모

- 3번은 내장 `P in S`가 훨씬 빠릅니다(README의 측정값). KMP로 직접 풀어 보는 것은 연습용이고, 실전에서는 내장을 쓰세요.
- 5번은 실패 함수의 정의가 곧 정답입니다. 4번, 6번, 7번은 같은 값 `n − failure[n−1]`을 어떻게 해석하는지만 다릅니다 (4, 6번은 나누어떨어져야 반복, 7번은 겹쳐도 되는 최소 길이).
- 8번은 실패 함수를 접미사마다 `n`번 만들어서 `O(n²)`입니다. 길이 5,000 정도까지 풀립니다. 더 길면 접미사 배열이 필요합니다. → [접미사 배열과 LCP](../../../lv3-advanced/05-strings-advanced/suffix-array-lcp/)
- 10번은 문자가 아니라 숫자 배열입니다. 구현의 `pattern[i] != pattern[k]` 비교는 어떤 같음 비교 가능한 원소에도 그대로 동작합니다.
- 11번은 `failure[n−1]`의 테두리가 중간에도 나오는지가 관건입니다. `failure` 값들 중에 `failure[n−1]`이 한 번 이상 나타나는지를 보거나 테두리 사슬을 따라 내려갑니다.
