"""solution.py 검증: 모든 부분 문자열을 직접 나열·세는 순진한 방법과 무작위 문자열(작은 알파벳)로 비교하고, 자동자의 구조적 불변식을 확인"""
import io
import random

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def random_string(rng, max_len=14, alphabet="ab"):
    return "".join(rng.choice(alphabet) for _ in range(rng.randint(0, max_len)))


def substrings(s):
    return {s[i:j] for i in range(len(s)) for j in range(i + 1, len(s) + 1)}


def overlapping_count(s, t):
    return sum(1 for i in range(len(s) - len(t) + 1) if s[i : i + len(t)] == t)


def test_distinct_substring_count_and_membership():
    rng = random.Random(0)
    for _ in range(600):
        s = random_string(rng, 14, rng.choice(["a", "ab", "abc"]))
        sam = solution.SuffixAutomaton(s)
        subs = substrings(s)
        assert sam.distinct == len(subs) == solution.count_distinct_substrings(s), s
        for t in subs:
            assert sam.contains(t)
        for _ in range(10):
            t = random_string(rng, 5, "abcd")
            assert sam.contains(t) == (t == "" or t in subs), (s, t)


def test_incremental_extend_equals_building_at_once():
    rng = random.Random(1)
    for _ in range(100):
        s = random_string(rng, 12, "ab")
        sam = solution.SuffixAutomaton()
        for i, ch in enumerate(s):
            sam.extend(ch)
            assert sam.distinct == len(substrings(s[: i + 1]))
        assert sam.length == solution.SuffixAutomaton(s).length and sam.link == solution.SuffixAutomaton(s).link
    # 질의 사이에 글자를 더 붙여도 캐시된 출현 횟수가 낡지 않는다
    sam = solution.SuffixAutomaton("aba")
    assert sam.count_occurrences("a") == 2
    sam.extend("a")
    assert sam.count_occurrences("a") == 3 and sam.count_occurrences("aba") == 1


def test_size_bounds_and_state_structure():
    rng = random.Random(2)
    for _ in range(200):
        s = random_string(rng, 16, rng.choice(["ab", "abc"]))
        sam = solution.SuffixAutomaton(s)
        n = len(s)
        if n >= 2:
            assert sam.state_count <= 2 * n - 1
        if n >= 3:
            assert sam.transition_count() <= 3 * n - 4
        # 한 상태의 문자열들은 같은 끝 위치 집합을 가지고, 길이는 len[link]+1 .. len 이 전부다
        groups = {}
        for t in substrings(s):
            groups.setdefault(sam._walk(t), []).append(t)
        assert len(groups) == sam.state_count - 1  # 루트(빈 문자열)를 뺀 모든 상태가 쓰인다
        for v, members in groups.items():
            ends = {frozenset(i + len(t) - 1 for i in range(n - len(t) + 1) if s[i : i + len(t)] == t) for t in members}
            assert len(ends) == 1
            assert sorted(len(t) for t in members) == list(range(sam.length[sam.link[v]] + 1, sam.length[v] + 1))


def test_occurrence_counts_first_occurrence_and_positions():
    rng = random.Random(3)
    for _ in range(400):
        s = random_string(rng, 14, rng.choice(["a", "ab", "abc"]))
        sam = solution.SuffixAutomaton(s)
        for _ in range(8):
            t = random_string(rng, 4, "abc")
            expected = [i for i in range(len(s) - len(t) + 1) if s[i : i + len(t)] == t]
            if t:
                assert sam.count_occurrences(t) == overlapping_count(s, t) == len(expected), (s, t)
                assert sam.first_occurrence(t) == (expected[0] if expected else -1), (s, t)
                assert sam.occurrence_positions(t) == expected, (s, t)
        assert sam.count_occurrences("") == len(s) + 1 and sam.first_occurrence("") == 0
        assert sam.occurrence_positions("") == list(range(len(s) + 1))


def test_longest_repeated_substring_length():
    rng = random.Random(4)
    for _ in range(500):
        s = random_string(rng, 14, rng.choice(["a", "ab", "abc"]))
        expected = max((len(t) for t in substrings(s) if overlapping_count(s, t) >= 2), default=0)
        assert solution.SuffixAutomaton(s).longest_repeated_substring_length() == expected, s
    assert solution.SuffixAutomaton("aaaa").longest_repeated_substring_length() == 3  # 겹쳐도 된다


def test_kth_distinct_substring_matches_sorting():
    rng = random.Random(5)
    for _ in range(300):
        s = random_string(rng, 10, rng.choice(["ab", "abc"]))
        sam = solution.SuffixAutomaton(s)
        ordered = sorted(substrings(s))
        for k in range(1, len(ordered) + 1):
            assert sam.kth_distinct_substring(k) == ordered[k - 1], (s, k)
    with pytest.raises(ValueError):
        solution.SuffixAutomaton("ab").kth_distinct_substring(0)
    with pytest.raises(ValueError):
        solution.SuffixAutomaton("ab").kth_distinct_substring(4)  # a, ab, b 세 개뿐


def test_longest_common_substring_of_two():
    rng = random.Random(6)
    for _ in range(600):
        alphabet = rng.choice(["a", "ab", "abc"])
        a, b = random_string(rng, 10, alphabet), random_string(rng, 10, alphabet)
        common = substrings(a) & substrings(b)
        best = max((len(t) for t in common), default=0)
        result = solution.SuffixAutomaton(a).longest_common_substring_with(b)
        assert len(result) == best and (best == 0 or result in common), (a, b, result)
    assert solution.SuffixAutomaton("xabcdy").longest_common_substring_with("zabcdw") == "abcd"
    assert solution.SuffixAutomaton("abc").longest_common_substring_with("xyz") == ""


def test_longest_common_substring_of_many():
    rng = random.Random(7)
    for _ in range(500):
        alphabet = rng.choice(["a", "ab", "abc"])
        strings = [random_string(rng, 9, alphabet) for _ in range(rng.randint(1, 4))]
        common = substrings(strings[0])
        for other in strings[1:]:
            common &= substrings(other)
        best = max((len(t) for t in common), default=0)
        result = solution.longest_common_substring_of_many(strings)
        assert len(result) == best and (best == 0 or result in common), (strings, result)
        if best:  # 같은 길이면 첫 문자열에서 가장 먼저 나오는 것
            assert result == min((t for t in common if len(t) == best), key=strings[0].find), (strings, result)
    assert solution.longest_common_substring_of_many([]) == ""
    assert solution.longest_common_substring_of_many(["abcde", "xbcdy", "ubcdv"]) == "bcd"
    assert solution.longest_common_substring_of_many(["abc"]) == "abc"
    assert solution.longest_common_substring_of_many(["ab", "cd", "ab"]) == ""


def test_shortest_absent_string():
    rng = random.Random(8)
    for _ in range(400):
        alphabet = rng.choice(["a", "ab", "abc"])
        s = random_string(rng, 12, alphabet)
        result = solution.SuffixAutomaton(s).shortest_absent_string(alphabet)
        subs = substrings(s) | {""}
        # 길이를 늘려 가며 사전순으로 처음 나오는, 부분 문자열이 아닌 문자열
        expected = None
        length = 1
        while expected is None:
            candidates = [""]
            for _ in range(length):
                candidates = [c + ch for c in candidates for ch in sorted(alphabet)]
            expected = next((c for c in candidates if c not in subs), None)
            length += 1
        assert result == expected, (s, alphabet, result, expected)
    assert solution.SuffixAutomaton("").shortest_absent_string("ab") == "a"


def test_non_string_symbols_and_large_input():
    sam = solution.SuffixAutomaton([1, 2, 1, 2, 3])
    assert sam.distinct == 12 and sam.count_occurrences([1, 2]) == 2
    rng = random.Random(9)
    s = "".join(rng.choice("abcd") for _ in range(100000))
    sam = solution.SuffixAutomaton(s)
    assert sam.state_count <= 2 * len(s) and sam.distinct <= len(s) * (len(s) + 1) // 2
    assert sam.contains(s[500:700]) and sam.count_occurrences(s[:50]) >= 1
    a = "ab" * 50000
    assert solution.SuffixAutomaton(a).distinct == 2 * len(a) - 1  # "ab" 의 반복: 길이 L 마다 서로 다른 것이 2개 (마지막 길이 제외)


def test_main_counts_distinct_substrings(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("abcbc\n"))
    solution.main()
    assert capsys.readouterr().out == "12\n"
