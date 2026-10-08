# 연습문제 — LIS

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 11053 가장 긴 증가하는 부분 수열](https://www.acmicpc.net/problem/11053) | 기본형 (n ≤ 1,000) | O(n²)과 O(n log n) 둘 다 풀어 본다 |
| 2 | [백준 12015 가장 긴 증가하는 부분 수열 2](https://www.acmicpc.net/problem/12015) | 기본형 (n ≤ 10⁶) | O(n log n) 필수. [solution.py](solution.py)의 `main()`이 같은 형태를 처리한다 |
| 3 | [LeetCode 300 Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) | 기본형 | 엄격한 증가. `lis_length` |
| 4 | [백준 14003 가장 긴 증가하는 부분 수열 5](https://www.acmicpc.net/problem/14003) | 수열 복원 | 길이와 함께 수열 출력. `lis_sequence` |
| 5 | [백준 2565 전깃줄](https://www.acmicpc.net/problem/2565) | 변환 | 한쪽으로 정렬 후 반대쪽의 LIS. 없앨 전깃줄 = 전체 − LIS |
| 6 | [백준 11054 가장 긴 바이토닉 부분 수열](https://www.acmicpc.net/problem/11054) | 바이토닉 | 앞에서 끝나는 LIS + 뒤에서 시작하는 LDS − 1. `longest_bitonic` |
| 7 | [LeetCode 354 Russian Doll Envelopes](https://leetcode.com/problems/russian-doll-envelopes/) | 2차원 | 너비로 정렬(같은 너비는 높이 내림차순) 후 높이의 LIS |
| 8 | [LeetCode 673 Number of Longest Increasing Subsequence](https://leetcode.com/problems/number-of-longest-increasing-subsequence/) | 개수 | LIS의 개수. `O(n²)` DP(`길이`, `개수` 두 배열). n이 크면 세그먼트 트리가 필요 |

## 풀이 메모

- 1번은 O(n²)로 풀리지만 2번과 같은 코드로 풀어 보는 것이 좋습니다. 입력 크기가 어떻게 달라지는지만 확인하세요.
- 4번은 같은 길이의 LIS가 여러 개일 수 있으므로, 문제의 출력 조건("아무거나" 또는 특정 순서)을 확인하세요.
- 5번과 7번은 **정렬 기준**이 핵심입니다. 7번에서는 너비가 같은 봉투끼리는 서로 넣을 수 없으므로, 같은 너비를 높이 내림차순으로 정렬해 같은 너비에서 두 개가 LIS에 들어가지 못하게 합니다.
- 6번은 수열을 뒤집는 트릭이 중요합니다. 뒤에서 시작하는 감소 수열 = 뒤집은 수열의 LIS입니다.
