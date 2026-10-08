"""solution.py 검증: 손으로 확인한 예제 + 정의를 그대로 옮긴 더 단순한 기준 구현과의 랜덤 비교"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def test_has_pair_with_sum():
    assert solution.has_pair_with_sum([1, 4, 5], 9)
    assert not solution.has_pair_with_sum([1, 4, 5], 8)  # 같은 원소를 두 번 쓰면 안 된다 (4 + 4)
    assert not solution.has_pair_with_sum([5], 10)
    assert solution.has_pair_with_sum([5, 5], 10)


def test_has_pair_matches_set_based_check():
    rng = random.Random(0)
    for _ in range(500):
        arr = [rng.randint(-5, 5) for _ in range(rng.randint(0, 8))]
        target = rng.randint(-10, 10)
        expected = any(arr[i] + arr[j] == target for i in range(len(arr)) for j in range(len(arr)) if i != j)
        assert solution.has_pair_with_sum(arr, target) == expected


def test_max_subarray_sum_matches_cubic_definition():
    rng = random.Random(1)
    for _ in range(500):
        arr = [rng.randint(-6, 6) for _ in range(rng.randint(1, 9))]
        expected = max(sum(arr[i:j]) for i in range(len(arr)) for j in range(i + 1, len(arr) + 1))
        assert solution.max_subarray_sum(arr) == expected, arr


def test_max_subarray_sum_all_negative_needs_one_element():
    assert solution.max_subarray_sum([-3, -1, -2]) == -1


def test_closest_triple_sum():
    assert solution.closest_triple_sum([5, 6, 7, 8, 9], 21) == 21
    rng = random.Random(2)
    for _ in range(300):
        cards = [rng.randint(1, 30) for _ in range(rng.randint(3, 8))]
        limit = rng.randint(3, 80)
        sums = [cards[i] + cards[j] + cards[k]
                for i in range(len(cards)) for j in range(i + 1, len(cards)) for k in range(j + 1, len(cards))]
        fitting = [x for x in sums if x <= limit]
        assert solution.closest_triple_sum(cards, limit) == (max(fitting) if fitting else -1)
    assert solution.closest_triple_sum([1, 2, 3], 5) == -1  # 합이 5 이하인 3장이 없다


def test_smallest_generator():
    assert solution.smallest_generator(216) == 198
    assert solution.smallest_generator(1) == 0
    assert solution.smallest_generator(2) == 1  # 1 + 1 = 2
    assert solution.smallest_generator(256) == 245
    generators = [n for n in range(1, 300) if solution.smallest_generator(n) == 0]
    assert 1 in generators and 3 in generators  # 생성자가 없는 수는 존재한다


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("5 21\n5 6 7 8 9\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "21"
