"""solution.py 검증: 정의대로 접두사와 한 글자씩 비교하는 순진한 방법과 무작위 문자열(작은 알파벳)로 비교"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def random_string(rng, max_len=14, alphabet="ab"):
    return "".join(rng.choice(alphabet) for _ in range(rng.randint(0, max_len)))


def naive_z(s):
    n = len(s)
    result = []
    for i in range(n):
        k = 0
        while i + k < n and s[k] == s[i + k]:
            k += 1
        result.append(k)
    return result


def test_z_function_matches_definition():
    rng = random.Random(0)
    for _ in range(1500):
        s = random_string(rng, alphabet=rng.choice(["a", "ab", "abc"]))
        assert solution.z_function(s) == naive_z(s), s
    assert solution.z_function("aabxaabxcaabxaabxay") == [19, 1, 0, 0, 4, 1, 0, 0, 0, 8, 1, 0, 0, 5, 1, 0, 0, 1, 0]
    assert solution.z_function("") == [] and solution.z_function("a") == [1]
    assert solution.z_function("aaaa") == [4, 3, 2, 1]


def test_z_function_works_on_lists_of_numbers():
    assert solution.z_function([1, 2, 1, 2, 1, 3]) == [6, 0, 3, 0, 1, 0]


def test_search_matches_find_loop_including_overlaps():
    rng = random.Random(1)
    for _ in range(1500):
        text = random_string(rng, 20)
        pattern = random_string(rng, 4)
        expected = [i for i in range(len(text) - len(pattern) + 1) if text.startswith(pattern, i)] if pattern else []
        assert solution.z_search(text, pattern) == expected, (text, pattern)
    assert solution.z_search("aaaaa", "aa") == [0, 1, 2, 3]
    assert solution.z_search("abc", "") == []


def test_smallest_period_and_borders_match_definition():
    rng = random.Random(2)
    for _ in range(1500):
        s = random_string(rng, 14, rng.choice(["a", "ab"]))
        n = len(s)
        expected_period = next((p for p in range(1, n) if s[p:] == s[: n - p]), n)
        assert solution.smallest_period(s) == expected_period, s
        expected_borders = [k for k in range(1, n) if s[:k] == s[n - k :]]
        assert solution.all_borders(s) == expected_borders, s
    assert solution.smallest_period("abcabcab") == 3 and solution.smallest_period("abc") == 3
    assert solution.all_borders("ababab") == [2, 4]


def test_prefix_occurrence_counts_match_counting_every_prefix():
    rng = random.Random(3)
    for _ in range(1000):
        s = random_string(rng, 14, rng.choice(["a", "ab"]))
        expected = [0] + [sum(1 for i in range(len(s) - k + 1) if s.startswith(s[:k], i)) for k in range(1, len(s) + 1)]
        assert solution.prefix_occurrence_counts(s) == expected, s
    assert solution.prefix_occurrence_counts("aab") == [0, 2, 1, 1]


def test_large_input_is_linear():
    rng = random.Random(4)
    text = "".join(rng.choice("ab") for _ in range(500_000))
    pattern = text[1234:1254]
    positions = solution.z_search(text, pattern)
    assert 1234 in positions
    assert all(text.startswith(pattern, p) for p in positions)
    assert solution.z_function("a" * 300_000)[1] == 299_999


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("ababababa\naba\n"))
    solution.main()
    assert capsys.readouterr().out.strip().splitlines() == ["4", "1 3 5 7"]
    monkeypatch.setattr("sys.stdin", io.StringIO("abc\nxyz\n"))
    solution.main()
    assert capsys.readouterr().out.strip().splitlines() == ["0"]
