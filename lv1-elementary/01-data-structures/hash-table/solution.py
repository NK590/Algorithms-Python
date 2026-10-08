"""해시 테이블 — 키를 해시 함수로 칸 번호로 바꿔 평균 O(1) 에 저장하고 찾는 자료구조

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- HashMap 은 체이닝(같은 칸에 들어온 항목을 리스트로 이어 두는 방식)으로 충돌을 처리하고, 가득 차 가면 칸 수를 두 배로 늘립니다.
- 파이썬의 dict 와 set 이 이 원리로 동작합니다. 실전에서는 내장 dict 를 쓰세요.
- 직접 실행하면 `N`, N 개의 카드, `M`, M 개의 질문을 받아, 질문한 수를 가지고 있으면 1 아니면 0 을 한 줄에 출력합니다.
"""
import sys


class HashMap:
    LOAD_FACTOR_LIMIT = 0.75  # 평균적으로 한 칸에 0.75 개를 넘으면 칸을 늘린다

    def __init__(self, capacity: int = 8):
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0

    @property
    def capacity(self) -> int:
        return len(self._buckets)

    def _bucket(self, key) -> list:
        return self._buckets[hash(key) % len(self._buckets)]  # 해시 값을 칸 수로 나눈 나머지가 칸 번호

    def put(self, key, value) -> None:
        """key 에 value 를 저장한다. 이미 있으면 값을 바꾼다. 평균 O(1)"""
        bucket = self._bucket(key)
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1
        if self._size > self.LOAD_FACTOR_LIMIT * len(self._buckets):
            self._resize(2 * len(self._buckets))

    def get(self, key, default=None):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return default

    def remove(self, key) -> bool:
        bucket = self._bucket(key)
        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self._size -= 1
                return True
        return False

    def __contains__(self, key) -> bool:
        return any(k == key for k, _ in self._bucket(key))

    def __len__(self) -> int:
        return self._size

    def items(self) -> list:
        return [(k, v) for bucket in self._buckets for k, v in bucket]

    def _resize(self, new_capacity: int) -> None:
        """칸 수가 바뀌면 칸 번호(해시 % 칸 수)도 바뀌므로 모든 항목을 다시 넣어야 한다."""
        old_items = self.items()
        self._buckets = [[] for _ in range(new_capacity)]
        self._size = 0
        for key, value in old_items:
            self.put(key, value)


def two_sum(numbers: list, target: int):
    """합이 target 인 서로 다른 두 위치 (i, j) (i < j). 없으면 None. 딕셔너리로 "이미 본 값"을 기억해 O(n)."""
    seen = HashMap()
    for j, x in enumerate(numbers):
        i = seen.get(target - x)
        if i is not None:
            return i, j
        seen.put(x, j)
    return None


def group_anagrams(words: list) -> list:
    """글자 구성이 같은 단어끼리 묶는다. 글자를 정렬한 문자열을 키로 쓴다. 각 묶음은 입력 순서를 유지하고, 묶음은 처음 나온 순서."""
    groups = HashMap()
    order = []
    for word in words:
        key = "".join(sorted(word))
        if key not in groups:
            groups.put(key, [])
            order.append(key)
        groups.get(key).append(word)
    return [groups.get(key) for key in order]


def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    cards = HashMap()
    for x in map(int, input().split()):
        cards.put(x, True)
    m = int(input())
    print(*(1 if x in cards else 0 for x in map(int, input().split())))


if __name__ == "__main__":
    main()
