"""solution.py 검증: heapq / sorted 와 무작위 연산 비교 + 힙 성질"""
import heapq
import io
import random

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def is_min_heap(a):
    return all(a[(i - 1) // 2] <= a[i] for i in range(1, len(a)))


def test_operations_match_heapq():
    rng = random.Random(0)
    for _ in range(300):
        heap, model = solution.MinHeap(), []
        for _ in range(80):
            if model and rng.random() < 0.4:
                assert heap.peek() == model[0]
                assert heap.pop() == heapq.heappop(model)
            else:
                value = rng.randint(-20, 20)
                heap.push(value)
                heapq.heappush(model, value)
            assert len(heap) == len(model) and is_min_heap(heap._a)


def test_build_from_iterable_creates_a_heap():
    rng = random.Random(1)
    for _ in range(300):
        values = [rng.randint(0, 30) for _ in range(rng.randint(0, 20))]
        heap = solution.MinHeap(values)
        assert is_min_heap(heap._a) and sorted(heap._a) == sorted(values)


def test_empty_heap_raises():
    for operation in ("pop", "peek"):
        with pytest.raises(IndexError):
            getattr(solution.MinHeap(), operation)()


def test_heap_sorted_matches_sorted():
    rng = random.Random(2)
    for _ in range(300):
        values = [rng.randint(-9, 9) for _ in range(rng.randint(0, 25))]
        assert solution.heap_sorted(values) == sorted(values)


def test_kth_largest():
    rng = random.Random(3)
    for _ in range(300):
        values = [rng.randint(0, 20) for _ in range(rng.randint(1, 20))]
        k = rng.randint(1, len(values))
        assert solution.kth_largest(values, k) == sorted(values, reverse=True)[k - 1]


def test_merge_sorted_lists():
    rng = random.Random(4)
    for _ in range(300):
        lists = [sorted(rng.randint(0, 15) for _ in range(rng.randint(0, 5))) for _ in range(rng.randint(0, 5))]
        assert solution.merge_sorted_lists(lists) == sorted(x for lst in lists for x in lst)


def test_running_median_matches_sorting_every_time():
    rng = random.Random(5)
    for _ in range(300):
        median, seen = solution.RunningMedian(), []
        for _ in range(rng.randint(1, 25)):
            x = rng.randint(-10, 10)
            median.add(x)
            seen.append(x)
            assert median.median() == sorted(seen)[(len(seen) - 1) // 2]  # 짝수 개이면 작은 쪽 가운데


def test_running_median_empty():
    with pytest.raises(IndexError):
        solution.RunningMedian().median()


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("6\n5\n3\n0\n0\n0\n8\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["3", "5", "0"]
