# 연습문제 — 슬라이딩 윈도우

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Playlist](https://cses.fi/problemset/task/1141) | 핵심 연습 | 중복이 없는 창의 왼쪽 경계를 이동한다 |
| 2 | [CSES — Subarray Sums I](https://cses.fi/problemset/task/1660) | 핵심 연습 | 양수의 합에 맞춰 창을 넓히고 줄인다 |
| 3 | [LeetCode 209 Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/) | 가변 길이 (짧은) | 합이 `target` 이상인 가장 짧은 구간. `shortest_subarray_sum_at_least` |
| 4 | [LeetCode 3 Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | 가변 길이 (긴) | `longest_unique_substring`. `last_seen[ch] >= left` 검사 |
| 5 | [LeetCode 904 Fruit Into Baskets](https://leetcode.com/problems/fruit-into-baskets/) | 종류 `K = 2` | 서로 다른 값이 2개 이하인 가장 긴 구간. `longest_with_at_most_k_distinct` |
| 6 | [LeetCode 424 Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) | 창 크기 − 최빈 글자 | `창 길이 − 최빈 글자 수 ≤ k`가 조건. 최빈값을 줄이지 않아도 정답이 맞는 이유를 생각 |
| 7 | [LeetCode 239 Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) | 모노톤 덱 | `window_max(numbers, k)[k-1:]` |
| 8 | [LeetCode 76 Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) | 포함 조건 | `min_window_covering`. 부족한 글자 수 `missing`으로 만족 여부를 `O(1)`에 판단 |
| 9 | [LeetCode 862 Shortest Subarray with Sum at Least K](https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/) | 음수 + 덱 | 원소에 음수가 있어 투 포인터가 안 된다. 접두사 합에 모노톤 덱 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
