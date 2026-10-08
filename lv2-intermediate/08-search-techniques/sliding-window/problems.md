# 연습문제 — 슬라이딩 윈도우

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 2559 수열](https://www.acmicpc.net/problem/2559) | 고정 길이 합 | 연속 `K`일의 합의 최댓값. `max_sum_of_k_consecutive`. 음수가 있어 `best`의 초기값에 주의 |
| 2 | [백준 21921 블로그](https://www.acmicpc.net/problem/21921) | 고정 길이 + 개수 | 최댓값과 그 최댓값을 만드는 창의 개수를 함께 센다 |
| 3 | [백준 12891 DNA 비밀번호](https://www.acmicpc.net/problem/12891) | 고정 길이 + 글자 수 | 창 안의 글자별 개수를 들어오는/나가는 글자로 갱신 |
| 4 | [LeetCode 209 Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/) | 가변 길이 (짧은) | 합이 `target` 이상인 가장 짧은 구간. `shortest_subarray_sum_at_least` |
| 5 | [백준 1806 부분합](https://www.acmicpc.net/problem/1806) | 가변 길이 (짧은) | 위와 같은 문제. 불가능하면 0 출력 |
| 6 | [LeetCode 3 Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | 가변 길이 (긴) | `longest_unique_substring`. `last_seen[ch] >= left` 검사 |
| 7 | [LeetCode 904 Fruit Into Baskets](https://leetcode.com/problems/fruit-into-baskets/) | 종류 `K = 2` | 서로 다른 값이 2개 이하인 가장 긴 구간. `longest_with_at_most_k_distinct` |
| 8 | [백준 13144 List of Unique Numbers](https://www.acmicpc.net/problem/13144) | 구간 개수 세기 | 중복 없는 연속 구간의 개수. 각 `right`마다 `right − left + 1`을 더한다 |
| 9 | [백준 15961 회전 초밥](https://www.acmicpc.net/problem/15961) | 원형 고정 창 | 배열을 이어 붙이거나 `% n`으로 원형 처리. 쿠폰 초밥은 항상 있다고 보고 종류를 센다 |
| 10 | [LeetCode 424 Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) | 창 크기 − 최빈 글자 | `창 길이 − 최빈 글자 수 ≤ k`가 조건. 최빈값을 줄이지 않아도 정답이 맞는 이유를 생각 |
| 11 | [LeetCode 239 Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) | 모노톤 덱 | `window_max(numbers, k)[k-1:]` |
| 12 | [백준 11003 최솟값 찾기](https://www.acmicpc.net/problem/11003) | 모노톤 덱 | `N`이 500만. [solution.py](solution.py)의 `main()`이 같은 형태이지만 파이썬에서는 입출력 최적화가 필요 |
| 13 | [LeetCode 76 Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) | 포함 조건 | `min_window_covering`. 부족한 글자 수 `missing`으로 만족 여부를 `O(1)`에 판단 |
| 14 | [LeetCode 862 Shortest Subarray with Sum at Least K](https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/) | 음수 + 덱 | 원소에 음수가 있어 투 포인터가 안 된다. 접두사 합에 모노톤 덱 |

## 풀이 메모

- 1번부터 3번은 "나가는 값을 빼고 들어오는 값을 더한다"가 전부입니다. [테스트](test_solution.py)의 `test_max_sum_of_k_consecutive`처럼 모든 구간을 직접 합해 본 값과 비교해 보세요.
- 4번, 5번은 원소가 양수라는 조건 덕에 `left`를 줄이면 합이 줄어듭니다. 14번에서는 그 단조성이 깨지므로 다른 방법이 필요하다는 점을 비교하세요.
- 8번은 구간의 **개수**를 세는 문제입니다. 오른쪽 끝이 `right`일 때 만족하는 구간의 왼쪽 끝은 `left`부터 `right`까지 모두 가능하므로 `right − left + 1`개가 늘어납니다.
- 10번은 최빈 글자 수를 줄이지 않는 쪽이 정답 길이만 갱신하는 데 충분합니다. 창이 줄지 않고 밀리기만 해도 정답이 맞는 이유를 직접 확인해 보세요.
- 12번은 입력이 500만 개입니다. `sys.stdin.buffer`로 한 번에 읽고 결과를 `join`으로 한 번에 출력해야 합니다. 그래도 파이썬에서는 빠듯합니다.
- 14번은 다음 단계로 도전할 문제입니다. 접두사 합 `P`에서 `P[j] − P[i] ≥ K`인 `i < j` 중 `j − i`가 최소인 쌍을 덱으로 찾습니다.
