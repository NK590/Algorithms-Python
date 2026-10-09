# 연습문제 — 이진 탐색 트리

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [AOJ — Binary Search Tree I](https://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ALDS1_8_A) | 핵심 연습 | 삽입과 중위 순회로 BST의 순서 성질을 확인한다 |
| 2 | [LeetCode 700 Search in a Binary Search Tree](https://leetcode.com/problems/search-in-a-binary-search-tree/) | 검색 | 비교 한 번마다 한쪽을 버리며 내려간다 |
| 3 | [LeetCode 701 Insert into a Binary Search Tree](https://leetcode.com/problems/insert-into-a-binary-search-tree/) | 삽입 | 빈 자리에 새 잎으로 붙인다 |
| 4 | [LeetCode 98 Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) | 검증 | 부모-자식 비교만으로는 부족하다. 범위(하한·상한)를 들고 내려가거나 중위 순회가 오름차순인지 확인 |
| 5 | [LeetCode 230 Kth Smallest Element in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) | 순서 질의 | 중위 순회의 k번째. 서브트리 크기를 저장하면 O(높이) (`kth_smallest`) |
| 6 | [LeetCode 108 Convert Sorted Array to Binary Search Tree](https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/) | 균형 만들기 | 가운데를 루트로 (`build_balanced`) |
| 7 | [LeetCode 450 Delete Node in a BST](https://leetcode.com/problems/delete-node-in-a-bst/) | 삭제 | 세 경우(잎, 자식 하나, 자식 둘) |
| 8 | [LeetCode 235 Lowest Common Ancestor of a Binary Search Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) | 응용 | 두 키 사이의 첫 노드가 LCA. BST 성질로 O(높이) |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
