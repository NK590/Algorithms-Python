"""solution.py 검증: itertools 와 순서까지 같은지 비교"""
import io
import itertools
import math
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def test_permutations_match_itertools():
    for n in range(0, 6):
        items = list(range(n))
        for r in range(0, n + 1):
            assert solution.permutations(items, r) == list(itertools.permutations(items, r))
    assert solution.permutations([1, 2, 3]) == list(itertools.permutations([1, 2, 3]))


def test_permutation_count_is_n_factorial():
    assert len(solution.permutations(list(range(6)))) == math.factorial(6)


def test_combinations_match_itertools():
    for n in range(0, 7):
        items = list(range(n))
        for r in range(0, n + 1):
            assert solution.combinations(items, r) == list(itertools.combinations(items, r))
    assert len(solution.combinations(list(range(10)), 3)) == math.comb(10, 3)


def test_unique_permutations_match_set_of_permutations():
    rng = random.Random(0)
    for _ in range(200):
        items = [rng.randint(0, 2) for _ in range(rng.randint(0, 6))]
        expected = sorted(set(itertools.permutations(items)))
        assert solution.unique_permutations(items) == expected, items


def test_next_permutation_walks_through_all_permutations_in_order():
    for items in ([1, 2, 3, 4], [1, 1, 2, 2], [3, 1, 2]):
        arr = sorted(items)
        seen = [tuple(arr)]
        while solution.next_permutation(arr):
            seen.append(tuple(arr))
        assert seen == sorted(set(itertools.permutations(items)))
        assert arr == sorted(items, reverse=True)  # 마지막 순열에서는 바꾸지 않고 False 를 반환한다


def test_next_permutation_examples():
    arr = [1, 2, 3]
    assert solution.next_permutation(arr) and arr == [1, 3, 2]
    arr = [3, 2, 1]
    assert not solution.next_permutation(arr) and arr == [3, 2, 1]
    arr = [1]
    assert not solution.next_permutation(arr)
    arr = []
    assert not solution.next_permutation(arr)


def test_subsets():
    assert sorted(solution.subsets([1, 2, 3])) == sorted(
        c for r in range(4) for c in itertools.combinations([1, 2, 3], r))
    assert len(solution.subsets(list(range(8)))) == 2 ** 8
    assert solution.subsets([]) == [()]


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("3 2\n"))
    solution.main()
    assert capsys.readouterr().out.splitlines() == ["1 2", "1 3", "2 1", "2 3", "3 1", "3 2"]
