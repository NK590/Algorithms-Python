"""정렬 알고리즘 테스트 공용 도우미 (lv1-elementary/02-sorting 의 test_solution.py 들이 함께 쓴다)

정렬 함수는 두 종류다.
- 제자리(in_place=True): 입력 리스트를 직접 정렬하고 반환값은 쓰지 않는다.
- 새 리스트(in_place=False): 입력은 그대로 두고 정렬된 새 리스트를 반환한다.
"""
from __future__ import annotations

import random
from typing import Callable, Iterator


def random_arrays(seed: int = 0, count: int = 300, max_len: int = 12,
                  low: int = -10, high: int = 10) -> Iterator[list[int]]:
    """빈 배열, 원소 1개, 그리고 중복·음수가 섞인 짧은 배열을 만들어 낸다"""
    rng = random.Random(seed)  # 시드를 고정해 실패를 재현할 수 있게 한다
    yield []
    yield [0]
    for _ in range(count):
        yield [rng.randint(low, high) for _ in range(rng.randint(0, max_len))]


class Keyed:
    """key 로만 크기를 비교하고 id 로 원래 순서를 기억하는 값 (안정성 검사용)"""
    __slots__ = ("key", "id")

    def __init__(self, key: int, id: int):
        self.key = key
        self.id = id

    def __lt__(self, other: Keyed) -> bool:
        return self.key < other.key

    def __le__(self, other: Keyed) -> bool:
        return self.key <= other.key

    def __gt__(self, other: Keyed) -> bool:
        return self.key > other.key

    def __ge__(self, other: Keyed) -> bool:
        return self.key >= other.key

    def __repr__(self) -> str:
        return f"{self.key}#{self.id}"


def apply_sort(sort_fn: Callable, arr: list, in_place: bool) -> list:
    """in_place 면 복사본을 정렬해 돌려주고, 아니면 함수의 반환값을 돌려준다"""
    if in_place:
        copy = list(arr)
        sort_fn(copy)
        return copy
    return sort_fn(arr)


def check_sorts_correctly(sort_fn: Callable, *, in_place: bool) -> None:
    """내장 sorted() 와 결과를 비교한다. 새 리스트를 반환하는 함수는 입력이 그대로인지도 확인한다."""
    for arr in random_arrays():
        before = list(arr)
        assert apply_sort(sort_fn, arr, in_place) == sorted(arr), arr
        assert arr == before, f"입력이 바뀌었습니다: {before} -> {arr}"


def check_is_stable(sort_fn: Callable, *, in_place: bool) -> None:
    """key 가 같은 원소들의 원래 순서가 유지되는지 확인한다"""
    rng = random.Random(1)
    for _ in range(300):
        items = [Keyed(rng.randint(0, 4), i) for i in range(rng.randint(0, 12))]
        result = apply_sort(sort_fn, items, in_place)
        assert sorted(x.key for x in items) == [x.key for x in result]
        for a, b in zip(result, result[1:]):
            assert a.key < b.key or a.id < b.id, f"안정적이지 않습니다: {items} -> {result}"
