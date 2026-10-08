# 연습문제 — 이진 탐색 트리

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [LeetCode 700 Search in a Binary Search Tree](https://leetcode.com/problems/search-in-a-binary-search-tree/) | 검색 | 비교 한 번마다 한쪽을 버리며 내려간다 |
| 2 | [LeetCode 701 Insert into a Binary Search Tree](https://leetcode.com/problems/insert-into-a-binary-search-tree/) | 삽입 | 빈 자리에 새 잎으로 붙인다 |
| 3 | [LeetCode 98 Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) | 검증 | 부모-자식 비교만으로는 부족하다. 범위(하한·상한)를 들고 내려가거나 중위 순회가 오름차순인지 확인 |
| 4 | [LeetCode 230 Kth Smallest Element in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) | 순서 질의 | 중위 순회의 k번째. 서브트리 크기를 저장하면 O(높이) (`kth_smallest`) |
| 5 | [백준 5639 이진 검색 트리](https://www.acmicpc.net/problem/5639) | 전위 → 후위 | 전위 순회에서 후위 순회 복원. 깊이가 최대 약 10⁴라 재귀 한도에 주의. `postorder_from_preorder`. [solution.py](solution.py)의 `main()`이 같은 형태를 처리한다 |
| 6 | [LeetCode 108 Convert Sorted Array to Binary Search Tree](https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/) | 균형 만들기 | 가운데를 루트로 (`build_balanced`) |
| 7 | [LeetCode 450 Delete Node in a BST](https://leetcode.com/problems/delete-node-in-a-bst/) | 삭제 | 세 경우(잎, 자식 하나, 자식 둘) |
| 8 | [LeetCode 235 Lowest Common Ancestor of a Binary Search Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) | 응용 | 두 키 사이의 첫 노드가 LCA. BST 성질로 O(높이) |
| 9 | [백준 7662 이중 우선순위 큐](https://www.acmicpc.net/problem/7662) | 응용 | 최솟값과 최댓값을 모두 삭제. BST(multiset)나 힙 두 개 + 지연 삭제로 푼다 |

## 풀이 메모

- 3번은 "왼쪽 자식 < 부모"만 확인하는 풀이가 흔히 틀립니다. 서브트리 안의 **모든** 키가 범위 안에 있어야 합니다.
- 5번은 테스트 데이터가 사슬 모양일 수 있어 재귀 구현이 `RecursionError`로 실패하는 경우가 있습니다. 이 폴더의 스택 방식(O(n))은 키가 정렬되어 있어도 문제없습니다. ([테스트](test_solution.py)의 `test_postorder_from_preorder_long_chain`)
- 9번은 표준 라이브러리에 균형 BST가 없으므로 파이썬에서는 힙 두 개와 "이미 삭제된 항목" 표시를 쓰는 방법이 일반적입니다.
