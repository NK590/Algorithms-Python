"""solution.py 검증: 모든 쌍/모든 구간을 확인하는 O(n²) 방법과 비교"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def random_numbers(rng, max_n=15, high=9):
    return [rng.randint(0, high) for _ in range(rng.randint(0, max_n))]


def test_next_greater_and_smaller_match_scan():
    rng = random.Random(0)
    for _ in range(800):
        numbers = random_numbers(rng)
        greater = [next((y for y in numbers[i + 1 :] if y > x), -1) for i, x in enumerate(numbers)]
        smaller = [next((y for y in numbers[i + 1 :] if y < x), -1) for i, x in enumerate(numbers)]
        assert solution.next_greater(numbers) == greater, numbers
        assert solution.next_smaller(numbers) == smaller, numbers
    assert solution.next_greater([3, 5, 2, 7]) == [5, 7, 7, -1]
    assert solution.next_greater([9, 5, 4, 3]) == [-1, -1, -1, -1]
    assert solution.next_greater([]) == [] and solution.next_greater([4, 4, 4]) == [-1, -1, -1]  # 같은 값은 '큰' 것이 아니다


def test_previous_smaller_index_matches_scan():
    rng = random.Random(1)
    for _ in range(800):
        numbers = random_numbers(rng)
        expected = [next((j for j in range(i - 1, -1, -1) if numbers[j] < x), -1) for i, x in enumerate(numbers)]
        assert solution.previous_smaller_index(numbers) == expected, numbers


def histogram_by_scan(heights):
    best = 0
    for i in range(len(heights)):
        low = heights[i]
        for j in range(i, len(heights)):
            low = min(low, heights[j])
            best = max(best, low * (j - i + 1))
    return best


def test_largest_rectangle_matches_all_intervals():
    rng = random.Random(2)
    for _ in range(800):
        heights = random_numbers(rng, max_n=12, high=8)
        assert solution.largest_rectangle_in_histogram(heights) == histogram_by_scan(heights), heights
    assert solution.largest_rectangle_in_histogram([2, 1, 5, 6, 2, 3]) == 10
    assert solution.largest_rectangle_in_histogram([]) == 0 and solution.largest_rectangle_in_histogram([4]) == 4
    assert solution.largest_rectangle_in_histogram([1000000000] * 3) == 3_000_000_000


def test_days_until_warmer():
    rng = random.Random(3)
    for _ in range(500):
        temps = random_numbers(rng, max_n=15, high=9)
        expected = [next((j - i for j in range(i + 1, len(temps)) if temps[j] > temps[i]), 0) for i in range(len(temps))]
        assert solution.days_until_warmer(temps) == expected, temps
    assert solution.days_until_warmer([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]


def rain_by_scan(heights):
    return sum(max(0, min(max(heights[: i + 1]), max(heights[i:])) - h) for i, h in enumerate(heights))


def test_trapped_rain_water_matches_two_sided_maximum():
    rng = random.Random(4)
    for _ in range(800):
        heights = random_numbers(rng, max_n=15, high=6)
        assert solution.trapped_rain_water(heights) == (rain_by_scan(heights) if heights else 0), heights
    assert solution.trapped_rain_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert solution.trapped_rain_water([4, 2, 0, 3, 2, 5]) == 9


def test_large_input_is_linear():
    n = 300_000
    rng = random.Random(5)
    numbers = [rng.randint(0, 10**9) for _ in range(n)]
    assert len(solution.next_greater(numbers)) == n
    assert solution.largest_rectangle_in_histogram(list(range(n))) == max(h * (n - h) for h in (n // 2, n // 2 + 1))


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("4\n3 5 2 7\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "5 7 7 -1"
