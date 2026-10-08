"""solution.py 검증: 구간을 직접 잘라 세는 순진한 방법과 무작위 수열·질의로 비교"""
import io
import random
import time
from collections import Counter

from tools.loader import load_solution

solution = load_solution(__file__)


def random_queries(rng, n, count, allow_empty=True):
    queries = []
    for _ in range(count):
        left = rng.randint(0, n)
        right = rng.randint(left if allow_empty else min(left + 1, n), n)
        queries.append((left, right))
    return queries


def test_distinct_counts_match_set_of_slice():
    rng = random.Random(0)
    for _ in range(800):
        n = rng.randint(0, 25)
        a = [rng.randint(0, rng.choice([1, 3, 10])) for _ in range(n)]
        queries = random_queries(rng, n, rng.randint(0, 25))
        assert solution.distinct_counts(a, queries) == [len(set(a[l:r])) for l, r in queries], (a, queries)
    assert solution.distinct_counts([], []) == []
    assert solution.distinct_counts([5], [(0, 1), (0, 0), (1, 1)]) == [1, 0, 0]


def test_distinct_counts_accept_any_hashable_values():
    a = ["x", "y", "x", (1, 2), (1, 2), "y"]
    queries = [(0, 6), (1, 4), (3, 5), (2, 3)]
    assert solution.distinct_counts(a, queries) == [3, 3, 1, 1]


def test_equal_pair_counts_match_counting_pairs():
    rng = random.Random(1)
    for _ in range(600):
        n = rng.randint(0, 22)
        a = [rng.randint(0, rng.choice([1, 2, 6])) for _ in range(n)]
        queries = random_queries(rng, n, rng.randint(0, 20))
        expected = [sum(c * (c - 1) // 2 for c in Counter(a[l:r]).values()) for l, r in queries]
        assert solution.equal_pair_counts(a, queries) == expected, (a, queries)
    assert solution.equal_pair_counts([7, 7, 7, 7], [(0, 4), (1, 3), (0, 1)]) == [6, 1, 0]


def test_generic_mo_with_a_sum_and_with_duplicate_queries():
    rng = random.Random(2)
    a = [rng.randint(-5, 5) for _ in range(40)]
    queries = random_queries(rng, 40, 60) + [(3, 17)] * 4  # 같은 질의가 여러 번
    state = [0]

    def add(i):
        state[0] += a[i]

    def remove(i):
        state[0] -= a[i]

    assert solution.mo(40, queries, add, remove, lambda: state[0]) == [sum(a[l:r]) for l, r in queries]


def test_mo_only_adds_absent_elements_and_removes_present_ones():
    # 넓히는 쪽을 먼저 하지 않으면 구간 밖의 원소를 먼저 "빼게" 된다. 합이나 종류 수는 우연히 맞아도 값이 음수가 되는 상태(최빈값 표 등)는 깨진다.
    rng = random.Random(6)
    n = 60
    queries = random_queries(rng, n, 80)
    inside = [False] * n

    def add(i):
        assert not inside[i], "이미 구간 안에 있는 원소를 또 넣었다"
        inside[i] = True

    def remove(i):
        assert inside[i], "구간 안에 없는 원소를 뺐다"
        inside[i] = False

    answers = solution.mo(n, queries, add, remove, lambda: [i for i in range(n) if inside[i]])
    assert answers == [list(range(l, r)) for l, r in queries]


def test_mo_order_is_a_permutation_grouped_by_left_block():
    rng = random.Random(3)
    n = 1000
    queries = random_queries(rng, n, 400)
    order = solution.mo_order(n, queries)
    assert sorted(order) == list(range(400))
    block = max(1, round(n / 400**0.5))
    blocks = [queries[i][0] // block for i in order]
    assert blocks == sorted(blocks)  # 왼쪽 끝의 블록 번호는 줄지 않는다
    for b in set(blocks):
        rights = [queries[i][1] for i in order if queries[i][0] // block == b]
        assert rights == sorted(rights, reverse=b % 2 == 1)  # 같은 블록에서는 홀짝에 따라 오름/내림


def test_sorted_order_moves_the_pointers_far_less_than_a_bad_order():
    rng = random.Random(4)
    n, q = 20000, 20000
    queries = random_queries(rng, n, q, allow_empty=False)
    good = solution.pointer_moves(solution.mo_order(n, queries), queries)
    plain = solution.pointer_moves(range(q), queries)  # 들어온 순서 그대로
    assert good < plain / 8
    assert good <= 6 * n * q**0.5  # 이론상 O(n√q)
    # 손으로 센 작은 예
    assert solution.pointer_moves([0, 1], [(0, 3), (2, 5)]) == 3 + 4


def test_large_input_runs_fast():
    rng = random.Random(5)
    n = q = 100000
    a = [rng.randint(0, 1000) for _ in range(n)]
    queries = random_queries(rng, n, q, allow_empty=False)
    started = time.perf_counter()
    result = solution.distinct_counts(a, queries)
    assert time.perf_counter() - started < 20
    for index in rng.sample(range(q), 20):  # 일부만 직접 확인
        left, right = queries[index]
        assert result[index] == len(set(a[left:right]))


def test_main_reads_one_based_inclusive_queries(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(b"5\n1 1 2 1 3\n3\n1 5\n2 4\n3 3\n")))
    solution.main()
    assert capsys.readouterr().out == "3\n2\n1\n"
