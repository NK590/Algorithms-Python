"""solution.py 검증: 느린 정의 그대로의 풀이(이중 반복, 정렬 후 훑기)와 무작위 비교"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def random_values(rng, high=8):
    return [rng.randint(0, high) for _ in range(rng.randint(0, 12))]


def test_count_distinct_and_set_operations_match_list_definitions():
    rng = random.Random(0)
    for _ in range(500):
        a, b = random_values(rng), random_values(rng)
        distinct = []
        for x in a:
            if x not in distinct:
                distinct.append(x)
        assert solution.count_distinct(a) == len(distinct)
        assert solution.common_elements(a, b) == sorted({x for x in a if x in b})
        only_a = {x for x in a if x not in b}
        only_b = {x for x in b if x not in a}
        assert solution.symmetric_difference_size(a, b) == len(only_a) + len(only_b)


def test_first_duplicate_matches_double_loop():
    rng = random.Random(1)
    for _ in range(500):
        values = random_values(rng, 20)
        expected = None
        for j in range(len(values)):
            if values[j] in values[:j]:
                expected = values[j]
                break
        assert solution.first_duplicate(values) == expected


def test_group_by_length():
    assert solution.group_by_length(["a", "bb", "c", "dd", "eee"]) == {1: ["a", "c"], 2: ["bb", "dd"], 3: ["eee"]}
    assert solution.group_by_length([]) == {}


def test_top_k_frequent_breaks_ties_by_smaller_value():
    assert solution.top_k_frequent([1, 1, 1, 2, 2, 3], 2) == [1, 2]
    assert solution.top_k_frequent([5, 3, 5, 3, 9], 2) == [3, 5]  # 횟수가 같으면 작은 값(3)이 먼저
    rng = random.Random(2)
    for _ in range(300):
        values = random_values(rng)
        k = rng.randint(1, 4)
        counts = {v: values.count(v) for v in set(values)}
        expected = sorted(counts, key=lambda v: (-counts[v], v))[:k]
        assert solution.top_k_frequent(values, k) == expected


def test_longest_consecutive_matches_sorted_scan():
    rng = random.Random(3)
    for _ in range(500):
        values = [rng.randint(0, 15) for _ in range(rng.randint(0, 12))]
        distinct = sorted(set(values))
        best, run = 0, 0
        for i, x in enumerate(distinct):
            run = run + 1 if i > 0 and x == distinct[i - 1] + 1 else 1
            best = max(best, run)
        assert solution.longest_consecutive(values) == best, values
    assert solution.longest_consecutive([100, 4, 200, 1, 3, 2]) == 4


def test_large_inputs_are_fast_because_membership_is_o1():
    n = 200_000
    values = list(range(n)) + [n // 2]
    assert solution.first_duplicate(values) == n // 2
    assert solution.longest_consecutive(values) == n
    assert solution.count_distinct(values) == n


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("3 5\n1 2 4\n3 4 5 6 7\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "6"
