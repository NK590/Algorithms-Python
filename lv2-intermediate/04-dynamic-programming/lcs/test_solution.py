"""solution.py 검증: 부분 수열 열거, 지수 시간 재귀, 모든 부분 문자열 비교와 대조"""
import io
import itertools
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def is_subsequence(small, big):
    it = iter(big)
    return all(ch in it for ch in small)


def lcs_by_enumeration(a, b):
    best = 0
    for r in range(len(a) + 1):
        for combo in itertools.combinations(a, r):
            if is_subsequence(combo, b):
                best = max(best, r)
    return best


def edit_by_recursion(a, b):
    """정의를 그대로 옮긴 지수 시간 재귀 (메모 없음)"""
    if not a:
        return len(b)
    if not b:
        return len(a)
    if a[-1] == b[-1]:
        return edit_by_recursion(a[:-1], b[:-1])
    return 1 + min(edit_by_recursion(a[:-1], b[:-1]), edit_by_recursion(a[:-1], b), edit_by_recursion(a, b[:-1]))


def random_strings(rng, max_len=8, alphabet="abc"):
    return ["".join(rng.choice(alphabet) for _ in range(rng.randint(0, max_len))) for _ in range(2)]


def test_lcs_matches_enumeration_in_all_forms():
    rng = random.Random(0)
    for _ in range(400):
        a, b = random_strings(rng, max_len=9)
        expected = lcs_by_enumeration(a, b)
        assert solution.lcs_length(a, b) == expected, (a, b)
        assert solution.lcs_table(a, b)[len(a)][len(b)] == expected
        s = solution.lcs_string(a, b)
        assert len(s) == expected and is_subsequence(s, a) and is_subsequence(s, b), (a, b, s)


def test_readme_example():
    assert solution.lcs_length("ACAYKP", "CAPCAK") == 4
    assert solution.lcs_string("ACAYKP", "CAPCAK") == "ACAK"
    assert solution.lcs_table("ACAYKP", "CAPCAK")[-1] == [0, 1, 2, 3, 3, 3, 4]
    table = solution.lcs_table("ABCBDAB", "BDCABA")
    assert table[-1][-1] == 4
    assert solution.lcs_length("", "abc") == 0 and solution.lcs_string("abc", "") == ""


def test_edit_distance_matches_recursion():
    rng = random.Random(1)
    for _ in range(400):
        a, b = random_strings(rng, max_len=6)
        assert solution.edit_distance(a, b) == edit_by_recursion(a, b), (a, b)
    assert solution.edit_distance("kitten", "sitting") == 3
    assert solution.edit_distance("", "abc") == 3 and solution.edit_distance("abc", "abc") == 0


def test_edit_distance_is_a_metric():
    rng = random.Random(2)
    for _ in range(200):
        a, b = random_strings(rng)
        c = random_strings(rng)[0]
        assert solution.edit_distance(a, b) == solution.edit_distance(b, a)
        assert solution.edit_distance(a, c) <= solution.edit_distance(a, b) + solution.edit_distance(b, c)
        # 길이 차이 이상, 긴 쪽 길이 이하
        assert abs(len(a) - len(b)) <= solution.edit_distance(a, b) <= max(len(a), len(b))


def test_longest_common_substring_matches_all_substrings():
    rng = random.Random(3)
    for _ in range(500):
        a, b = random_strings(rng, max_len=9)
        length, text = solution.longest_common_substring(a, b)
        best = max((j - i for i in range(len(a)) for j in range(i, len(a) + 1) if a[i:j] in b), default=0)
        assert length == best == len(text), (a, b)
        assert text in a and text in b
    assert solution.longest_common_substring("abcdxyz", "xyzabcd") == (4, "abcd")


def test_substring_is_not_subsequence():
    # "ace" 는 "abcde" 와 "xaxcxe" 의 공통 부분 수열이지만 연속한 공통 부분 문자열은 아니다
    assert solution.lcs_length("abcde", "xaxcxe") == 3
    assert solution.longest_common_substring("abcde", "xaxcxe")[0] == 1


def test_shortest_common_supersequence():
    rng = random.Random(4)
    for _ in range(400):
        a, b = random_strings(rng, max_len=8)
        s = solution.shortest_common_supersequence(a, b)
        assert is_subsequence(a, s) and is_subsequence(b, s)
        assert len(s) == len(a) + len(b) - solution.lcs_length(a, b), (a, b, s)
    assert solution.shortest_common_supersequence("abac", "cab") == "cabac"  # 길이 4 + 3 - LCS("ab") = 5


def test_large_inputs_run_fast():
    a = "ab" * 750
    b = "ba" * 750
    assert solution.lcs_length(a, b) == 1499
    assert solution.edit_distance(a[:800], b[:800]) == 2


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("ACAYKP\nCAPCAK\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "4"
