"""자릿수 DP(Digit DP) — 1 이상 N 이하의 수 중 "자릿수들이 만드는 조건" 을 만족하는 수를 N 이 10^18 이어도 자릿수 길이만큼의 DP 로 세기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 수를 높은 자리부터 한 자리씩 만들어 가며 (지금까지의 상태) 만 기억합니다. N 과 같은 접두사를 유지 중인지(tight) 와 이미 N 보다 작아졌는지(free) 를 구분하고,
  free 가 되면 남은 자리는 0..base-1 어떤 숫자든 올 수 있어서 같은 상태끼리 묶어 (개수, 이득의 합) 으로 압축합니다.
- 앞쪽 0 (leading zero) 은 자릿수가 아니므로 step 에 들어가지 않습니다. 길이가 N 보다 짧은 수는 두 번째 자리부터 새로 시작하는 것으로 셉니다.
- digit_dp(upper, init, step): 1..upper 를 훑어 {최종 상태: (수의 개수, 이득의 합)} 을 돌려줍니다.
  step(상태, 숫자) 는 (새 상태, 이 숫자가 주는 이득) 또는 None(이 숫자는 금지 — 그 수는 세지 않음) 을 돌려줍니다.
- 그 위에 쓴 함수들: 숫자가 나온 횟수, 자릿수 합의 총합, 금지 숫자가 없는 수, 자릿수 합이 정해진 수, m 의 배수, 이웃한 숫자가 같지 않은 수.
- 직접 실행하면 N 을 받아 1..N 의 모든 자연수에서 0, 1, …, 9 가 각각 몇 번 나오는지 출력합니다 (자릿수 출현 집계 예제 형식).
"""
import sys
from typing import Callable, Hashable, Optional

State = Hashable
Step = Callable[[State, int], Optional[tuple[State, int]]]


def digits_of(n: int, base: int = 10) -> list[int]:
    """n 의 base 진법 숫자들 (높은 자리부터). n ≥ 1."""
    digits = []
    while n:
        n, r = divmod(n, base)
        digits.append(r)
    return digits[::-1]


def digit_dp(upper: int, init: State, step: Step, base: int = 10) -> dict[State, tuple[int, int]]:
    """1 이상 upper 이하의 수들 중 step 이 금지하지 않은 수에 대해 {최종 상태: (수의 개수, 이득의 총합)}."""
    if base < 2:
        raise ValueError("진법은 2 이상이어야 합니다")
    if upper < 1:
        return {}
    digits = digits_of(upper, base)
    free: dict[State, list[int]] = {}  # 이미 upper 보다 작아진 접두사들: 상태 -> [개수, 이득의 합]
    tight: Optional[tuple[State, int]] = None  # upper 의 접두사와 같은 접두사 하나: (상태, 이득)

    def add_free(table, state, count, gain):
        entry = table.setdefault(state, [0, 0])
        entry[0] += count
        entry[1] += gain

    # 첫 자리: 1..first-1 은 곧바로 free, first 는 tight 로 이어진다
    first = digits[0]
    for d in range(1, first):
        result = step(init, d)
        if result is not None:
            add_free(free, result[0], 1, result[1])
    result = step(init, first)
    tight = (result[0], result[1]) if result is not None else None

    for position in range(1, len(digits)):
        next_free: dict[State, list[int]] = {}
        for state, (count, gain) in free.items():  # free 는 남은 자리에 무엇이든 올 수 있다
            for d in range(base):
                result = step(state, d)
                if result is not None:
                    add_free(next_free, result[0], count, gain + count * result[1])
        if tight is not None:
            state, gain = tight
            for d in range(digits[position]):  # upper 의 이번 숫자보다 작은 숫자를 고르면 free 가 된다
                result = step(state, d)
                if result is not None:
                    add_free(next_free, result[0], 1, gain + result[1])
            result = step(state, digits[position])  # 같은 숫자를 고르면 tight 유지
            tight = (result[0], gain + result[1]) if result is not None else None
        for d in range(1, base):  # 길이가 upper 보다 짧은 수: 이 자리에서 시작
            result = step(init, d)
            if result is not None:
                add_free(next_free, result[0], 1, result[1])
        free = next_free

    final = {state: (count, gain) for state, (count, gain) in free.items()}
    if tight is not None:
        state, gain = tight
        count0, gain0 = final.get(state, (0, 0))
        final[state] = (count0 + 1, gain0 + gain)
    return final


def count_digit_occurrences(n: int, digit: int, base: int = 10) -> int:
    """1..n 의 모든 수를 쓸 때 숫자 digit 이 나오는 횟수 (앞쪽 0 은 쓰지 않는다)."""
    if not 0 <= digit < base:
        raise ValueError("digit 은 0 이상 base 미만이어야 합니다")
    result = digit_dp(n, 0, lambda s, d: (0, 1 if d == digit else 0), base)
    return sum(gain for _, gain in result.values())


def digit_counts(n: int) -> list[int]:
    """1..n 에서 0, 1, …, 9 가 나오는 횟수 (자릿수 출현 집계 예제)."""
    return [count_digit_occurrences(n, d) for d in range(10)]


def digit_sum_total(n: int, base: int = 10) -> int:
    """1..n 의 각 수의 자릿수 합을 모두 더한 값."""
    result = digit_dp(n, 0, lambda s, d: (0, d), base)
    return sum(gain for _, gain in result.values())


def count_without_digit(n: int, banned: int, base: int = 10) -> int:
    """1..n 중 숫자 banned 가 한 번도 나오지 않는 수의 개수."""
    result = digit_dp(n, 0, lambda s, d: None if d == banned else (0, 0), base)
    return sum(count for count, _ in result.values())


def count_with_digit_sum(n: int, target: int, base: int = 10) -> int:
    """1..n 중 자릿수 합이 정확히 target 인 수의 개수."""

    def step(total, d):
        total += d
        return (total, 0) if total <= target else None  # 합이 넘으면 더 볼 필요가 없다

    result = digit_dp(n, 0, step, base)
    return result.get(target, (0, 0))[0]


def count_digit_sum_divisible(n: int, k: int, base: int = 10) -> int:
    """1..n 중 자릿수 합이 k 의 배수인 수의 개수."""
    if k < 1:
        raise ValueError("k 는 1 이상이어야 합니다")
    result = digit_dp(n, 0, lambda r, d: ((r + d) % k, 0), base)
    return result.get(0, (0, 0))[0]


def count_multiples(n: int, m: int, base: int = 10) -> int:
    """1..n 중 m 의 배수의 개수. 상태는 지금까지 만든 수를 m 으로 나눈 나머지 (다른 조건과 합칠 때의 기본형)."""
    if m < 1:
        raise ValueError("m 은 1 이상이어야 합니다")
    result = digit_dp(n, 0, lambda r, d: ((r * base + d) % m, 0), base)
    return result.get(0, (0, 0))[0]


def count_no_adjacent_equal(n: int, base: int = 10) -> int:
    """1..n 중 이웃한 두 숫자가 같은 곳이 없는 수의 개수. 상태는 직전 숫자."""
    result = digit_dp(n, -1, lambda last, d: None if d == last else (d, 0), base)
    return sum(count for count, _ in result.values())


def count_binary_without_adjacent_ones(n: int) -> int:
    """1..n 중 이진수로 쓸 때 1 이 이웃한 곳이 없는 수의 개수. 상태는 직전 숫자 (이진법의 digit_dp)."""
    result = digit_dp(n, 0, lambda last, d: None if last == 1 and d == 1 else (d, 0), base=2)
    return sum(count for count, _ in result.values())


def count_in_range(count_up_to: Callable[[int], int], lo: int, hi: int) -> int:
    """lo..hi (lo ≥ 1) 의 개수 = count_up_to(hi) - count_up_to(lo - 1)."""
    return count_up_to(hi) - count_up_to(lo - 1)


def main() -> None:
    n = int(sys.stdin.readline())
    print(" ".join(map(str, digit_counts(n))))


if __name__ == "__main__":
    main()
