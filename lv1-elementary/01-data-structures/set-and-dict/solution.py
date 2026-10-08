"""집합(set)과 딕셔너리(dict) 활용 — "이미 봤는가?", "몇 번 나왔는가?"를 평균 O(1) 에 답하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 둘 다 해시 테이블이라 값의 존재 확인, 추가, 삭제가 평균 O(1) 입니다. (리스트의 `in` 은 O(n))
- 직접 실행하면 `A B` 와 두 집합의 원소를 받아, 한쪽에만 있는 원소의 총 개수(대칭 차집합의 크기)를 출력합니다.
"""
import sys
from collections import Counter, defaultdict


def count_distinct(values) -> int:
    """서로 다른 값의 개수."""
    return len(set(values))


def common_elements(a, b) -> list:
    """두 입력에 모두 있는 값 (오름차순, 중복 없음). 집합의 교집합."""
    return sorted(set(a) & set(b))


def symmetric_difference_size(a, b) -> int:
    """한쪽에만 있는 값의 개수 = |A − B| + |B − A|."""
    return len(set(a) ^ set(b))


def first_duplicate(values):
    """처음으로 "앞에서 이미 나온 값"이 다시 나오는 값. 없으면 None. 본 값을 집합에 기록하며 한 번만 훑는다."""
    seen = set()
    for x in values:
        if x in seen:
            return x
        seen.add(x)
    return None


def group_by_length(words) -> dict:
    """길이별로 단어를 묶는다. defaultdict 는 없는 키에 자동으로 빈 리스트를 만들어 준다."""
    groups = defaultdict(list)
    for word in words:
        groups[len(word)].append(word)
    return dict(groups)


def top_k_frequent(values, k: int) -> list:
    """가장 자주 나온 값 k 개. 횟수가 같으면 작은 값 먼저."""
    counts = Counter(values)
    return sorted(counts, key=lambda v: (-counts[v], v))[:k]


def longest_consecutive(values) -> int:
    """연속된 정수로 이루어진 가장 긴 부분의 길이 (순서 무관, 예: {100, 4, 200, 1, 3, 2} → 4). 정렬 없이 O(n).

    각 수가 "연속 구간의 시작"일 때(x - 1 이 집합에 없을 때)만 앞으로 세어 나가면 모든 수를 한 번씩만 본다.
    """
    present = set(values)
    best = 0
    for x in present:
        if x - 1 not in present:
            length = 1
            while x + length in present:
                length += 1
            best = max(best, length)
    return best


def main() -> None:
    input = sys.stdin.readline
    input()
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    print(symmetric_difference_size(a, b))


if __name__ == "__main__":
    main()
