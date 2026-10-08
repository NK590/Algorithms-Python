# 연습문제 — 매내처 알고리즘

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [LeetCode 5 Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) | 가장 긴 회문 | 길이 1000이라 `O(n²)` 넓히기로도 풀린다. 매내처와 결과를 비교하는 기준 문제 |
| 2 | [LeetCode 647 Palindromic Substrings](https://leetcode.com/problems/palindromic-substrings/) | 회문 개수 | `sum(odd) + sum(even)`. 위치가 다르면 같은 내용이어도 따로 센다 |
| 3 | [백준 11046 팰린드롬??](https://www.acmicpc.net/problem/11046) | 구간 회문 질의 (수열) | `N, M ≤ 10⁶`이라 질의당 `O(1)`이 필요하다. 수열(정수 리스트)에도 그대로 쓴다. [PalindromeChecker](solution.py) |
| 4 | [백준 10942 팰린드롬?](https://www.acmicpc.net/problem/10942) | 구간 회문 질의 | `N ≤ 2000`이라 `O(N²)` DP 표도 되지만 질의 100만 개의 입출력이 병목이다. 두 방법을 비교 |
| 5 | [백준 13275 가장 긴 팰린드롬 부분 문자열](https://www.acmicpc.net/problem/13275) | 가장 긴 회문 (큰 입력) | 길이 10⁵. [solution.py](solution.py)의 `main()`이 같은 형태(길이를 출력) |
| 6 | [LeetCode 132 Palindrome Partitioning II](https://leetcode.com/problems/palindrome-partitioning-ii/) | 최소 분할 | `min_palindrome_cuts`. 회문 판정 표 + 1차원 DP |
| 7 | [백준 1509 팰린드롬 분할](https://www.acmicpc.net/problem/1509) | 최소 분할 | 길이 2500. 잘라 낸 조각의 **개수**를 출력한다(자르는 횟수 + 1) |
| 8 | [LeetCode 1960 Maximum Product of the Length of Two Palindromic Substrings](https://leetcode.com/problems/maximum-product-of-the-length-of-two-palindromic-substrings/) | 겹치지 않는 두 회문 | 각 위치까지(부터) 가장 긴 홀수 회문을 반지름 배열에서 퍼뜨려 구한다 |

## 풀이 메모

- 1번, 2번은 먼저 `O(n²)` 중심 확장으로 풀고 [매내처](solution.py)로 다시 풀어 두 결과를 비교해 보세요. 테스트는 보통 `"aaaa…a"`와 무작위 문자열을 모두 시도해 보면 됩니다.
- 3번과 4번은 거의 같은 문제입니다. 4번은 `N ≤ 2000`이라서 `O(N²)` DP로 충분하지만, 3번은 `N ≤ 10⁶`이라 매내처가 필요합니다. 파이썬에서 질의 10⁶개를 처리하려면 입출력을 `sys.stdin.buffer.read().split()`와 한 번의 `print("\n".join(...))`로 묶으세요.
- 6번과 7번은 같은 DP이고 답이 `조각 수 − 1`인지 `조각 수`인지만 다릅니다. 출력이 무엇인지 읽고 시작하세요.
- 8번이 가장 어렵습니다. 반지름 배열을 "각 위치에서 끝나는(시작하는) 가장 긴 홀수 회문의 길이" 배열로 바꾸는 과정을 손으로 그려 보세요. 한 중심의 회문이 덮는 범위 안의 모든 위치가 후보가 됩니다.
