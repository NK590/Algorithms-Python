"""solution.py 검증: O(n²) DP 와 모든 부분 수열 열거와 비교"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def lis_n2(numbers, strict=True):
    if not numbers:
        return 0
    dp = [1] * len(numbers)
    for i in range(len(numbers)):
        for j in range(i):
            if (numbers[j] < numbers[i]) if strict else (numbers[j] <= numbers[i]):
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


def best_by_enumeration(numbers, keep):
    best = 0
    for mask in range(1 << len(numbers)):
        picked = [numbers[i] for i in range(len(numbers)) if mask >> i & 1]
        if keep(picked):
            best = max(best, len(picked))
    return best


def is_subsequence(small, big):
    it = iter(big)
    return all(x in it for x in small)


def random_numbers(rng, max_n=40, high=15):
    return [rng.randint(0, high) for _ in range(rng.randint(0, max_n))]


def test_length_matches_quadratic_dp():
    rng = random.Random(0)
    for _ in range(800):
        numbers = random_numbers(rng)
        assert solution.lis_length(numbers) == lis_n2(numbers), numbers
        assert solution.longest_non_decreasing(numbers) == lis_n2(numbers, strict=False), numbers


def test_matches_full_enumeration_on_short_sequences():
    rng = random.Random(1)
    for _ in range(300):
        numbers = random_numbers(rng, max_n=10, high=6)
        strict = lambda p: all(a < b for a, b in zip(p, p[1:]))
        assert solution.lis_length(numbers) == best_by_enumeration(numbers, strict), numbers


def test_sequence_is_a_valid_longest_subsequence():
    rng = random.Random(2)
    for _ in range(800):
        numbers = random_numbers(rng)
        sequence = solution.lis_sequence(numbers)
        assert len(sequence) == solution.lis_length(numbers)
        assert all(a < b for a, b in zip(sequence, sequence[1:]))
        assert is_subsequence(sequence, numbers)


def test_readme_example():
    numbers = [10, 20, 10, 30, 20, 50]
    assert solution.lis_length(numbers) == 4
    assert solution.lis_sequence(numbers) == [10, 20, 30, 50]
    assert solution.lis_lengths_ending_at(numbers) == [1, 2, 1, 3, 2, 4]
    assert solution.longest_non_decreasing([1, 2, 2, 3]) == 4 and solution.lis_length([1, 2, 2, 3]) == 3
    # tails 는 LIS 자체가 아니다: [4, 5, 1] 을 다 읽은 뒤 tails 는 [1, 5] 이지만 LIS 는 [4, 5]
    assert solution.lis_sequence([4, 5, 1]) == [4, 5]


def test_special_cases():
    assert solution.lis_length([]) == 0 and solution.lis_sequence([]) == []
    assert solution.lis_length([7]) == 1 and solution.lis_sequence([7]) == [7]
    assert solution.lis_length([5, 5, 5]) == 1 and solution.longest_non_decreasing([5, 5, 5]) == 3
    assert solution.lis_length([5, 4, 3, 2, 1]) == 1
    assert solution.lis_length(list(range(1000))) == 1000


def test_lengths_ending_at_match_quadratic_dp():
    rng = random.Random(3)
    for _ in range(500):
        numbers = random_numbers(rng, max_n=25)
        expected = []
        for i in range(len(numbers)):
            expected.append(1 + lis_n2([x for x in numbers[:i] if x < numbers[i]]))  # i 앞에서 i 보다 작은 값들의 LIS + 1
        assert solution.lis_lengths_ending_at(numbers) == expected, numbers


def test_bitonic_matches_enumeration():
    rng = random.Random(4)

    def bitonic(p):
        if not p:
            return True
        peak = p.index(max(p))
        return all(a < b for a, b in zip(p[: peak + 1], p[1 : peak + 1])) and all(a > b for a, b in zip(p[peak:], p[peak + 1 :]))

    for _ in range(300):
        numbers = random_numbers(rng, max_n=10, high=7)
        assert solution.longest_bitonic(numbers) == best_by_enumeration(numbers, bitonic), numbers
    assert solution.longest_bitonic([1, 5, 2, 4, 3, 2, 1]) == 6  # 1 2 4 3 2 1
    assert solution.longest_bitonic([]) == 0


def test_min_removals():
    assert solution.min_removals_to_sort([3, 1, 2, 5, 4]) == 2
    assert solution.min_removals_to_sort([]) == 0
    assert solution.min_removals_to_sort([2, 2, 2]) == 2  # 엄격한 오름차순이어야 하므로 같은 값도 지워야 한다


def test_large_input_is_fast():
    rng = random.Random(5)
    numbers = [rng.randint(0, 10**9) for _ in range(200_000)]
    assert 1 <= solution.lis_length(numbers) <= 200_000
    assert len(solution.lis_sequence(numbers)) == solution.lis_length(numbers)


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("6\n10 20 10 30 20 50\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "4"
