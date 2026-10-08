"""solution.py 검증: 모든 위치를 직접 비교하는 O(nm) 방법과 비교, 실패 함수는 정의대로 계산한 값과 비교"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def failure_by_definition(pattern):
    """각 접두사에 대해 접두사이자 접미사인 가장 긴 진부분 문자열의 길이"""
    result = []
    for i in range(1, len(pattern) + 1):
        prefix = pattern[:i]
        best = 0
        for length in range(1, i):
            if prefix[:length] == prefix[-length:]:
                best = length
        result.append(best)
    return result


def search_by_definition(text, pattern):
    if not pattern:
        return []
    return [i for i in range(len(text) - len(pattern) + 1) if text[i : i + len(pattern)] == pattern]


def random_text(rng, alphabet, max_len):
    return "".join(rng.choice(alphabet) for _ in range(rng.randint(0, max_len)))


def test_failure_function_matches_definition():
    rng = random.Random(0)
    for _ in range(1000):
        pattern = random_text(rng, "ab", 14)
        assert solution.failure_function(pattern) == failure_by_definition(pattern), pattern
    assert solution.failure_function("ABCDABD") == [0, 0, 0, 0, 1, 2, 0]
    assert solution.failure_function("AAAA") == [0, 1, 2, 3]
    assert solution.failure_function("") == []


def test_search_matches_naive_search_including_overlaps():
    rng = random.Random(1)
    for _ in range(2000):
        alphabet = rng.choice(["ab", "abc", "a"])
        text = random_text(rng, alphabet, 30)
        pattern = random_text(rng, alphabet, 6)
        assert solution.kmp_search(text, pattern) == search_by_definition(text, pattern), (text, pattern)
    assert solution.kmp_search("AAAAA", "AA") == [0, 1, 2, 3]  # 겹치는 등장도 모두
    assert solution.kmp_search("ABC ABCDAB ABCDABCDABDE", "ABCDABD") == [15]
    assert solution.kmp_search("abc", "") == [] and solution.kmp_search("", "a") == []


def test_count_occurrences():
    assert solution.count_occurrences("ABABABABABABABABABABA", "ABABA") == 9
    assert solution.count_occurrences("hello", "z") == 0


def test_worst_case_for_naive_search_is_linear():
    # 순진한 방법이 O(nm) 이 되는 입력: "aaaa…a" 에서 "aaa…ab" 를 찾기
    text = "a" * 200_000
    pattern = "a" * 1000 + "b"
    assert solution.kmp_search(text, pattern) == []
    assert solution.kmp_search(text, "a" * 1000)[:3] == [0, 1, 2]


def smallest_period_by_definition(s):
    n = len(s)
    for unit in range(1, n + 1):
        if n % unit == 0 and s == s[:unit] * (n // unit):
            return unit
    return 0


def test_smallest_period_matches_definition():
    rng = random.Random(2)
    for _ in range(1000):
        base = random_text(rng, "ab", 5) or "a"
        s = base * rng.randint(1, 4) if rng.random() < 0.6 else random_text(rng, "ab", 12)
        assert solution.smallest_period(s) == smallest_period_by_definition(s), s
    assert solution.smallest_period("abcabcabc") == 3 and solution.smallest_period("abcabca") == 7
    assert solution.smallest_period("") == 0 and solution.smallest_period("aaaa") == 1


def test_shortest_prefix_covering():
    # 접두사를 겹쳐 이어 붙여도 되는 경우: "abcabca" 는 "abc" 를 반복해 만들 수 있다
    assert solution.shortest_prefix_covering("abcabca") == 3
    assert solution.shortest_prefix_covering("abcabcabc") == 3
    assert solution.shortest_prefix_covering("abcd") == 4
    assert solution.shortest_prefix_covering("") == 0


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("ABC ABCDAB ABCDABCDABDE\nABCDABD\n"))
    solution.main()
    assert capsys.readouterr().out.splitlines() == ["1", "16"]
    monkeypatch.setattr("sys.stdin", io.StringIO("aaaa\naa\n"))
    solution.main()
    assert capsys.readouterr().out.splitlines() == ["3", "1 2 3"]
    monkeypatch.setattr("sys.stdin", io.StringIO("abc\nz\n"))
    solution.main()
    assert capsys.readouterr().out.splitlines() == ["0", ""]
