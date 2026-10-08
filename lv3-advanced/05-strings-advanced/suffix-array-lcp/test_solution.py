"""solution.py 검증: 접미사를 직접 잘라 정렬하는 순진한 방법, 부분 문자열 집합, 모든 위치 비교와 무작위 문자열(작은 알파벳)로 비교"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def random_string(rng, max_len=14, alphabet="ab"):
    return "".join(rng.choice(alphabet) for _ in range(rng.randint(0, max_len)))


def naive_suffix_array(s):
    return sorted(range(len(s)), key=lambda i: s[i:])


def naive_lcp(a, b):
    k = 0
    while k < len(a) and k < len(b) and a[k] == b[k]:
        k += 1
    return k


def test_suffix_array_matches_sorting_the_suffixes():
    rng = random.Random(0)
    for _ in range(1500):
        s = random_string(rng, 16, rng.choice(["a", "ab", "abc", "abcd"]))
        assert solution.suffix_array(s) == naive_suffix_array(s), s
    assert solution.suffix_array("") == []
    assert solution.suffix_array("a") == [0]
    assert solution.suffix_array("banana") == [5, 3, 1, 0, 4, 2]
    assert solution.suffix_array("aaaa") == [3, 2, 1, 0]


def test_suffix_array_accepts_integer_lists():
    rng = random.Random(1)
    for _ in range(300):
        values = [rng.randint(-3, 3) for _ in range(rng.randint(0, 12))]
        assert solution.suffix_array(values) == sorted(range(len(values)), key=lambda i: values[i:]), values


def test_lcp_array_matches_comparing_neighbouring_suffixes():
    rng = random.Random(2)
    for _ in range(1500):
        s = random_string(rng, 16, rng.choice(["a", "ab", "abc"]))
        sa = solution.suffix_array(s)
        expected = [0 if i == 0 else naive_lcp(s[sa[i - 1] :], s[sa[i] :]) for i in range(len(s))]
        assert solution.lcp_array(s, sa) == expected, s
    assert solution.lcp_array("", []) == []
    sa = solution.suffix_array("banana")
    assert solution.lcp_array("banana", sa) == [0, 1, 3, 0, 0, 2]


def test_count_distinct_substrings_matches_a_set_of_all_substrings():
    rng = random.Random(3)
    for _ in range(1000):
        s = random_string(rng, 14, rng.choice(["a", "ab", "abc"]))
        expected = len({s[i:j] for i in range(len(s)) for j in range(i + 1, len(s) + 1)})
        assert solution.count_distinct_substrings(s) == expected, s
    assert solution.count_distinct_substrings("") == 0
    assert solution.count_distinct_substrings("aaaa") == 4
    assert solution.count_distinct_substrings("banana") == 15


def test_longest_repeated_substring_matches_brute_force_and_prefers_the_smallest():
    rng = random.Random(4)
    for _ in range(1000):
        s = random_string(rng, 14, rng.choice(["a", "ab", "abc"]))
        repeated = {
            s[i:j]
            for i in range(len(s))
            for j in range(i + 1, len(s) + 1)
            if sum(1 for p in range(len(s) - (j - i) + 1) if s[p : p + j - i] == s[i:j]) >= 2  # 겹친 출현도 센다
        }
        expected = min(repeated, key=lambda t: (-len(t), t)) if repeated else ""
        assert solution.longest_repeated_substring(s) == expected, s
    assert solution.longest_repeated_substring("banana") == "ana"
    assert solution.longest_repeated_substring("abcd") == ""
    assert solution.longest_repeated_substring("") == ""
    assert solution.longest_repeated_substring("aaaa") == "aaa"  # 겹쳐도 된다


def test_longest_common_substring_matches_brute_force():
    rng = random.Random(5)
    for _ in range(1500):
        alphabet = rng.choice(["a", "ab", "abc", "\x00a", "\x00\x01"])  # NUL 문자(코드 0)도 들어갈 수 있다
        a = random_string(rng, 10, alphabet)
        b = random_string(rng, 10, alphabet)
        common = {a[i:j] for i in range(len(a)) for j in range(i + 1, len(a) + 1)} & {
            b[i:j] for i in range(len(b)) for j in range(i + 1, len(b) + 1)
        }
        result = solution.longest_common_substring(a, b)
        best = max((len(t) for t in common), default=0)
        expected = min((t for t in common if len(t) == best), default="")  # 가장 긴 것 중 사전순으로 가장 앞
        assert result == expected, (a, b, result)
    assert solution.longest_common_substring("xabcdy", "zabcdw") == "abcd"
    assert solution.longest_common_substring("abc", "") == "" and solution.longest_common_substring("", "abc") == ""
    assert solution.longest_common_substring("abc", "xyz") == ""
    assert solution.longest_common_substring("aaa", "aa") == "aa"


def test_longest_common_substring_handles_the_zero_character():
    # 구분자는 모든 글자보다 작아야 하므로, 글자 코드에 1 을 더해 NUL 문자 와도 구별한다
    assert solution.longest_common_substring("a\x00b", "\x00bc") == "\x00b"
    assert solution.longest_common_substring("\x00", "\x00\x00") == "\x00"


def test_longest_common_substring_does_not_cross_the_separator():
    # 구분자 없이 이어 붙이면 "ab" + "cd" 의 경계를 가로지르는 "bc" 같은 것이 생기지만, 공통 부분 문자열이 될 수 없다
    assert solution.longest_common_substring("ab", "cd") == ""
    assert solution.longest_common_substring("abab", "abab") == "abab"
    assert solution.longest_common_substring("zz", "z") == "z"


def test_find_occurrences_matches_scanning_every_position():
    rng = random.Random(6)
    for _ in range(600):
        s = random_string(rng, 16, rng.choice(["a", "ab", "abc"]))
        sa = solution.suffix_array(s)
        for _ in range(8):
            pattern = random_string(rng, 4, "abc")
            if not pattern:
                assert solution.find_occurrences(s, sa, pattern) == []
                continue
            expected = [i for i in range(len(s) - len(pattern) + 1) if s[i : i + len(pattern)] == pattern]
            assert solution.find_occurrences(s, sa, pattern) == expected, (s, pattern)
    s = "banana"
    sa = solution.suffix_array(s)
    assert solution.find_occurrences(s, sa, "ana") == [1, 3]
    assert solution.find_occurrences(s, sa, "banana") == [0]
    assert solution.find_occurrences(s, sa, "bananas") == []
    assert solution.find_occurrences(s, sa, "n") == [2, 4]
    assert solution.find_occurrences(s, sa, "") == [] and solution.find_occurrences(s, sa, "z") == []


def test_lcp_query_matches_comparing_any_two_suffixes():
    rng = random.Random(7)
    for _ in range(300):
        s = random_string(rng, 14, rng.choice(["a", "ab", "abc"]))
        query = solution.LcpQuery(s)
        for i in range(len(s)):
            for j in range(len(s)):
                assert query.lcp_of_suffixes(i, j) == naive_lcp(s[i:], s[j:]), (s, i, j)


def test_large_strings_run_fast_and_stay_consistent():
    rng = random.Random(8)
    s = "".join(rng.choice("ab") for _ in range(60000))
    sa = solution.suffix_array(s)
    assert sorted(sa) == list(range(len(s)))
    lcp = solution.lcp_array(s, sa)
    for position in rng.sample(range(1, len(s)), 200):  # 일부 이웃 쌍만 직접 확인
        assert min(lcp[position], 80) == naive_lcp(s[sa[position - 1] : sa[position - 1] + 80], s[sa[position] : sa[position] + 80])
    for position in rng.sample(range(1, len(s)), 200):
        assert s[sa[position - 1] : sa[position - 1] + 40] <= s[sa[position] : sa[position] + 40]
    repetitive = "a" * 50000  # 접두사 배가법이 가장 오래 도는 입력
    assert solution.suffix_array(repetitive) == list(range(49999, -1, -1))
    assert solution.count_distinct_substrings(repetitive) == 50000


def test_main_prints_one_based_suffix_array_and_lcp_with_leading_x(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("banana\n"))
    solution.main()
    assert capsys.readouterr().out == "6 4 2 1 5 3\nx 1 3 0 0 2\n"
    monkeypatch.setattr("sys.stdin", io.StringIO("a\n"))
    solution.main()
    assert capsys.readouterr().out == "1\nx\n"
