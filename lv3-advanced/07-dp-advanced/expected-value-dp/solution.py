"""기댓값 DP(Expected Value DP) — "앞으로 평균 몇 번" 을 점화식으로 쓰고, 분수(Fraction)나 모듈러 역원으로 정확히 구하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- E[상태] = 한 번 움직이는 비용 + Σ (다음 상태로 갈 확률 × E[다음 상태]).  끝나는 상태의 E 는 0.  방향이 정해진(DAG) 상태면 끝에서부터 채우고,
  제자리·되돌아가기가 있으면 연립일차방정식 (I - Q)·E = 1 을 풉니다 (absorbing_chain, solve_linear).
- 기댓값의 선형성: E[X + Y] = E[X] + E[Y] 는 X, Y 가 독립이 아니어도 성립하므로, 복잡한 양을 간단한 지표(0/1) 의 합으로 쪼개 하나씩 기댓값을 구합니다 (expected_inversions, expected_fixed_points).
- 값은 Fraction(정확한 분수) 으로 구하거나, 답을 "p/q mod P" 로 요구하는 문제를 위해 모듈러 역원을 씁니다 (expected_rolls_mod, fraction_mod).
- expected_rolls_to_reach: d 면체 주사위를 합이 목표 이상이 될 때까지 굴리는 횟수의 기댓값.  coupon_collector: n 종류의 쿠폰을 다 모으는 데 필요한 뽑기 횟수의 기댓값.
- sum_distribution: 주사위 n 개 합의 확률 분포.  gamblers_ruin: 도박꾼의 파산 문제 (목표 도달 확률).
- 직접 실행하면 `목표 면의 수` 를 받아 합이 목표 이상이 될 때까지 굴리는 횟수의 기댓값을 기약분수 p/q 와 p·q^(-1) mod 998244353 으로 두 줄에 출력합니다.
"""
import sys
from collections import deque
from fractions import Fraction
from typing import Hashable, Mapping, Sequence

MOD = 998244353


def solve_linear(a: Sequence[Sequence[Fraction]], b: Sequence[Fraction]) -> list[Fraction]:
    """연립일차방정식 A·x = b 를 가우스 소거법으로 (분수로 정확히) 푼다. 특이 행렬이면 ValueError."""
    n = len(a)
    rows = [[Fraction(v) for v in row] + [Fraction(rhs)] for row, rhs in zip(a, b)]
    for column in range(n):
        pivot = next((r for r in range(column, n) if rows[r][column] != 0), None)
        if pivot is None:
            raise ValueError("해가 하나로 정해지지 않는 연립방정식입니다")
        rows[column], rows[pivot] = rows[pivot], rows[column]
        scale = rows[column][column]
        rows[column] = [v / scale for v in rows[column]]
        for r in range(n):
            if r != column and rows[r][column] != 0:
                factor = rows[r][column]
                rows[r] = [x - factor * y for x, y in zip(rows[r], rows[column])]
    return [rows[i][n] for i in range(n)]


def absorbing_chain(
    transitions: Mapping[Hashable, Mapping[Hashable, Fraction]], absorbing: Sequence[Hashable]
) -> tuple[dict, dict]:
    """흡수 마르코프 연쇄. transitions[상태][다음 상태] = 확률 (흡수 상태에서는 나가지 않는다).
    돌려주는 값: (expected_steps[상태], absorption[상태][흡수 상태]) — 각 일반 상태에서 흡수될 때까지 걸리는 평균 횟수와, 어느 흡수 상태에서 끝날 확률."""
    absorbing_set = set(absorbing)
    transient = [s for s in transitions if s not in absorbing_set]
    index = {s: i for i, s in enumerate(transient)}
    size = len(transient)
    # (I - Q)·E = 1  과  (I - Q)·P_a = R_a
    matrix = [[Fraction(1 if i == j else 0) for j in range(size)] for i in range(size)]
    for s in transient:
        for t, probability in transitions[s].items():
            if t in index:
                matrix[index[s]][index[t]] -= Fraction(probability)
    steps = solve_linear(matrix, [Fraction(1)] * size)
    absorption = {s: {} for s in transient}
    for a in absorbing:
        rhs = [Fraction(transitions[s].get(a, 0)) for s in transient]
        solved = solve_linear(matrix, rhs)
        for s in transient:
            absorption[s][a] = solved[index[s]]
    return {s: steps[index[s]] for s in transient}, absorption


def expected_rolls_to_reach(target: int, sides: int = 6) -> Fraction:
    """공정한 sides 면체 주사위를 합이 target 이상이 될 때까지 굴리는 횟수의 기댓값 (정확한 분수).
    E[s] = 1 + (1/sides)·Σ_{k=1..sides} E[s + k],  E[s ≥ target] = 0.  뒤에서부터 구간 합을 밀며 O(target)."""
    if sides < 1:
        raise ValueError("주사위의 면은 1 이상이어야 합니다")
    window = deque([Fraction(0)] * sides)  # window[0] = E[s+1], …, window[-1] = E[s+sides]  (s = target-1 에서 시작)
    window_sum = Fraction(0)
    value = Fraction(0)
    for _ in range(target):
        value = 1 + window_sum / sides
        window_sum += value - window.pop()  # 다음(s-1) 구간: 가장 먼 E[s+sides] 를 빼고 방금 구한 E[s] 를 앞에 넣는다
        window.appendleft(value)
    return value


def fraction_mod(value: Fraction, mod: int = MOD) -> int:
    """분수 p/q 를 p·q^(-1) mod P (P 는 소수) 로. q 가 P 의 배수면 ValueError."""
    if value.denominator % mod == 0:
        raise ValueError("분모가 mod 의 배수입니다")
    return value.numerator % mod * pow(value.denominator, -1, mod) % mod


def expected_rolls_mod(target: int, sides: int = 6, mod: int = MOD) -> int:
    """expected_rolls_to_reach 를 분수 없이 모듈러로 (mod 는 sides 와 서로소인 소수)."""
    if sides < 1 or sides % mod == 0:
        raise ValueError("주사위의 면은 1 이상이고 mod 의 배수가 아니어야 합니다")
    inverse = pow(sides, -1, mod)
    window = deque([0] * sides)
    window_sum = 0
    value = 0
    for _ in range(target):
        value = (1 + window_sum * inverse) % mod
        window_sum = (window_sum + value - window.pop()) % mod
        window.appendleft(value)
    return value


def coupon_collector(n: int) -> Fraction:
    """n 종류가 같은 확률로 나오는 쿠폰을 모두 모으는 데 필요한 뽑기 횟수의 기댓값 (= n·H_n).
    k 종류를 가진 상태에서: E_k = 1 + (k/n)·E_k + ((n-k)/n)·E_{k+1}  →  E_k = n/(n-k) + E_{k+1}."""
    if n < 0:
        raise ValueError("n 은 0 이상이어야 합니다")
    expected = Fraction(0)
    for k in range(n - 1, -1, -1):
        expected += Fraction(n, n - k)
    return expected


def sum_distribution(dice: int, sides: int) -> list[Fraction]:
    """공정한 sides 면체 주사위 dice 개를 굴린 합이 s 일 확률 (인덱스 s = 0..dice·sides)."""
    if dice < 0 or sides < 1:
        raise ValueError("주사위 수는 0 이상, 면은 1 이상이어야 합니다")
    ways = [1]  # ways[s] = 합이 s 인 경우의 수. 주사위를 하나씩 더하며 합성곱
    for _ in range(dice):
        nxt = [0] * (len(ways) + sides)
        for total, count in enumerate(ways):
            for face in range(1, sides + 1):
                nxt[total + face] += count
        ways = nxt
    total_ways = sides**dice
    return [Fraction(count, total_ways) for count in ways]


def probability_sum_at_least(dice: int, sides: int, threshold: int) -> Fraction:
    return sum(sum_distribution(dice, sides)[max(threshold, 0) :], Fraction(0))


def gamblers_ruin(start: int, goal: int, p: Fraction) -> Fraction:
    """시작 돈 start, 한 판에 p 의 확률로 +1, 1-p 로 -1.  0 원이 되기 전에 goal 원에 도달할 확률 (연쇄를 직접 풀어서)."""
    if not 0 <= start <= goal or goal < 1:
        raise ValueError("0 ≤ start ≤ goal, goal ≥ 1 이어야 합니다")
    p = Fraction(p)
    if start in (0, goal):
        return Fraction(1 if start == goal else 0)
    transitions = {0: {}, goal: {}}
    for money in range(1, goal):
        transitions[money] = {money + 1: p, money - 1: 1 - p}
    _, absorption = absorbing_chain(transitions, [0, goal])
    return absorption[start][goal]


def expected_inversions(n: int) -> Fraction:
    """무작위 순열의 역순 쌍(i<j, a_i>a_j) 개수의 기댓값. 쌍마다 확률 1/2 → C(n,2)/2.  (기댓값의 선형성)"""
    return Fraction(n * (n - 1), 4)


def expected_fixed_points(n: int) -> Fraction:
    """무작위 순열에서 a_i = i 인 위치 수의 기댓값. 위치마다 확률 1/n → n·(1/n) = 1.  (선형성; 지표들이 독립이 아니어도 성립)"""
    return Fraction(1) if n >= 1 else Fraction(0)


def main() -> None:
    target, sides = (int(x) for x in sys.stdin.read().split()[:2])
    value = expected_rolls_to_reach(target, sides)
    print(f"{value.numerator}/{value.denominator}")
    print(fraction_mod(value))


if __name__ == "__main__":
    main()
