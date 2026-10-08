"""solution.py 검증: 모든 창/모든 구간을 직접 확인하는 O(nk) / O(n²) 방법과 비교"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def random_numbers(rng, max_n=15, low=0, high=9):
    return [rng.randint(low, high) for _ in range(rng.randint(0, max_n))]


def test_window_max_and_min_match_brute_force():
    rng = random.Random(0)
    for _ in range(800):
        numbers = random_numbers(rng, low=-5)
        k = rng.randint(1, 8)
        trailing = [numbers[max(0, i - k + 1) : i + 1] for i in range(len(numbers))]
        assert solution.window_max(numbers, k) == [max(w) for w in trailing], (numbers, k)
        assert solution.window_min(numbers, k) == [min(w) for w in trailing], (numbers, k)
    # 완전한 창만 보려면 앞의 k-1 개를 버린다
    assert solution.window_max([1, 3, -1, -3, 5, 3, 6, 7], 3)[2:] == [3, 3, 5, 5, 6, 7]
    assert solution.window_min([1, 3, -1, -3, 5, 3, 6, 7], 3)[2:] == [-1, -3, -3, -3, 3, 3]


def test_window_extremes_special_cases():
    assert solution.window_max([], 3) == [] and solution.window_min([5], 1) == [5]
    assert solution.window_max([4, 3, 2, 1], 1) == [4, 3, 2, 1]  # k = 1 이면 자기 자신
    assert solution.window_max([1, 2, 3, 4], 10) == [1, 2, 3, 4]  # k 가 n 보다 크면 앞에서부터의 최댓값
    assert solution.window_min([2, 2, 2], 2) == [2, 2, 2]


def test_max_sum_of_k_consecutive():
    rng = random.Random(1)
    for _ in range(500):
        numbers = random_numbers(rng, low=-5)
        k = rng.randint(0, 8)
        if 0 < k <= len(numbers):
            expected = max(sum(numbers[i : i + k]) for i in range(len(numbers) - k + 1))
        else:
            expected = 0
        assert solution.max_sum_of_k_consecutive(numbers, k) == expected, (numbers, k)
    assert solution.max_sum_of_k_consecutive([3, -2, 5, -1, 6, -3, 2, 7, -5, 2], 5) == 11


def test_longest_unique_substring():
    rng = random.Random(2)
    for _ in range(800):
        s = "".join(rng.choice("abcd") for _ in range(rng.randint(0, 14)))
        expected = max((j - i for i in range(len(s)) for j in range(i, len(s) + 1) if len(set(s[i:j])) == j - i), default=0)
        assert solution.longest_unique_substring(s) == expected, s
    assert solution.longest_unique_substring("abcabcbb") == 3 and solution.longest_unique_substring("bbbbb") == 1
    assert solution.longest_unique_substring("pwwkew") == 3 and solution.longest_unique_substring("abba") == 2


def test_longest_with_at_most_k_distinct():
    rng = random.Random(3)
    for _ in range(800):
        items = random_numbers(rng, max_n=14, high=4)
        k = rng.randint(0, 4)
        expected = max((j - i for i in range(len(items)) for j in range(i, len(items) + 1) if len(set(items[i:j])) <= k), default=0) if k > 0 else 0
        assert solution.longest_with_at_most_k_distinct(items, k) == expected, (items, k)
    assert solution.longest_with_at_most_k_distinct("eceba", 2) == 3
    assert solution.longest_with_at_most_k_distinct([1, 2, 1, 2, 3], 2) == 4


def test_shortest_subarray_sum_at_least_for_positive_numbers():
    rng = random.Random(4)
    for _ in range(800):
        numbers = random_numbers(rng, max_n=14, low=1, high=9)
        target = rng.randint(1, 40)
        lengths = [j - i for i in range(len(numbers)) for j in range(i + 1, len(numbers) + 1) if sum(numbers[i:j]) >= target]
        assert solution.shortest_subarray_sum_at_least(numbers, target) == (min(lengths) if lengths else 0), (numbers, target)
    assert solution.shortest_subarray_sum_at_least([2, 3, 1, 2, 4, 3], 7) == 2


def test_min_window_covering():
    rng = random.Random(5)
    for _ in range(800):
        s = "".join(rng.choice("abc") for _ in range(rng.randint(0, 12)))
        t = "".join(rng.choice("abc") for _ in range(rng.randint(0, 4)))
        best = None
        for i in range(len(s)):
            for j in range(i + 1, len(s) + 1):
                window = s[i:j]
                if all(window.count(ch) >= t.count(ch) for ch in set(t)):
                    if best is None or len(window) < len(best):
                        best = window
        expected = "" if not t else (best or "")
        assert solution.min_window_covering(s, t) == expected, (s, t)
    assert solution.min_window_covering("ADOBECODEBANC", "ABC") == "BANC"
    assert solution.min_window_covering("a", "aa") == ""


def test_large_input_runs_in_linear_time():
    rng = random.Random(6)
    numbers = [rng.randint(0, 10**9) for _ in range(300_000)]
    result = solution.window_max(numbers, 1000)
    assert len(result) == len(numbers) and result[-1] == max(numbers[-1000:])
    assert solution.longest_unique_substring("".join(chr(97 + i % 26) for i in range(200_000))) == 26


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("12 3\n1 5 2 3 6 2 3 7 3 5 2 6\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "1 1 1 2 2 2 2 2 3 3 2 2"
