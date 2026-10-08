"""solution.py 검증: 모든 부분 문자열을 뒤집어 비교하는 순진한 방법과 무작위 문자열(작은 알파벳)로 비교"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def random_string(rng, max_len=14, alphabet="ab"):
    return "".join(rng.choice(alphabet) for _ in range(rng.randint(0, max_len)))


def is_pal(t):
    return t == t[::-1]


def test_radii_match_naive_expansion():
    rng = random.Random(0)
    for _ in range(1500):
        s = random_string(rng, 14, rng.choice(["a", "ab", "abc"]))
        odd, even = solution.manacher(s)
        n = len(s)
        expected_odd = [max(k for k in range(1, n + 1) if i - k + 1 >= 0 and i + k <= n and is_pal(s[i - k + 1 : i + k])) for i in range(n)]
        expected_even = [
            max([0] + [k for k in range(1, n + 1) if i - k >= 0 and i + k <= n and is_pal(s[i - k : i + k])]) for i in range(n)
        ]
        assert odd == expected_odd and even == expected_even, s
    assert solution.manacher("") == ([], [])
    assert solution.manacher("aaa") == ([1, 2, 1], [0, 1, 1])


def test_longest_palindromic_substring_matches_brute_force_and_prefers_the_earliest():
    rng = random.Random(1)
    for _ in range(1500):
        s = random_string(rng, 14, rng.choice(["a", "ab", "abc"]))
        best = ""
        for i in range(len(s)):
            for j in range(i + 1, len(s) + 1):
                if is_pal(s[i:j]) and len(s[i:j]) > len(best):
                    best = s[i:j]
        assert solution.longest_palindromic_substring(s) == best, s
    assert solution.longest_palindromic_substring("babad") == "bab"
    assert solution.longest_palindromic_substring("cbbd") == "bb"
    assert solution.longest_palindromic_substring("") == ""


def test_count_palindromic_substrings_matches_brute_force():
    rng = random.Random(2)
    for _ in range(1000):
        s = random_string(rng, 14, rng.choice(["a", "ab"]))
        expected = sum(1 for i in range(len(s)) for j in range(i + 1, len(s) + 1) if is_pal(s[i:j]))
        assert solution.count_palindromic_substrings(s) == expected, s
    assert solution.count_palindromic_substrings("aaa") == 6 and solution.count_palindromic_substrings("abc") == 3


def test_palindrome_checker_matches_every_substring():
    rng = random.Random(3)
    for _ in range(300):
        s = random_string(rng, 12, rng.choice(["a", "ab"]))
        checker = solution.PalindromeChecker(s)
        for i in range(len(s) + 1):
            for j in range(i, len(s) + 1):
                assert checker.is_palindrome(i, j) == is_pal(s[i:j]), (s, i, j)


def test_min_palindrome_cuts_matches_plain_dp():
    rng = random.Random(4)
    for _ in range(500):
        s = random_string(rng, 12, rng.choice(["a", "ab", "abc"]))
        n = len(s)
        pieces = [0] + [None] * n
        for i in range(1, n + 1):
            pieces[i] = min(pieces[j] + 1 for j in range(i) if is_pal(s[j:i]))
        assert solution.min_palindrome_cuts(s) == (pieces[n] - 1 if n else 0), s
    assert solution.min_palindrome_cuts("aab") == 1 and solution.min_palindrome_cuts("abba") == 0


def test_large_inputs_are_linear():
    s = "a" * 200_000
    assert solution.longest_palindromic_substring(s) == s
    t = "ab" * 100_000
    assert len(solution.longest_palindromic_substring(t)) == 199_999
    rng = random.Random(5)
    u = "".join(rng.choice("ab") for _ in range(200_000))
    odd, even = solution.manacher(u)
    assert max(max(odd) * 2 - 1, max(even) * 2) >= 10


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("abacdfgdcaba\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "3"
