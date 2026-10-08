"""확장 유클리드 호제법 — gcd(a, b) 와 함께 a·x + b·y = gcd(a, b) 를 만족하는 정수 x, y(베주 계수)를 구하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 유클리드 호제법의 각 나머지가 "원래 a, b 의 정수 결합" 이라는 사실을 끝까지 추적합니다. O(log min(a, b)).
- 응용: ① 모듈러 역원(소수가 아니어도 됨)  ② 일차 부정 방정식 a·x + b·y = c  ③ 일차 합동식 a·x ≡ b (mod m).
- 해는 하나가 아니라 x = x0 + (b/g)·t, y = y0 − (a/g)·t (t 는 임의의 정수) 꼴로 무한히 많습니다.
- 직접 실행하면 `A B C` 를 받아 A·x + B·y = C 인 정수 x, y 를 출력합니다(x 가 0 이상으로 가장 작은 해). 해가 없으면 -1.
"""
import math
import sys


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """(g, x, y): g = gcd(a, b) ≥ 0, a·x + b·y = g.

    나머지가 0 이 될 때까지 (r0, r1) → (r1, r0 mod r1) 를 반복하면서, 각 나머지를 a, b 의 결합 s·a + t·b 로 함께 갱신한다."""
    old_r, r = a, b
    old_s, s = 1, 0  # old_r = old_s·a + old_t·b
    old_t, t = 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    if old_r < 0:  # 음수 입력이면 gcd 의 부호를 맞춘다
        old_r, old_s, old_t = -old_r, -old_s, -old_t
    return old_r, old_s, old_t


def extended_gcd_recursive(a: int, b: int) -> tuple[int, int, int]:
    """재귀 버전 (a, b ≥ 0). b·y' + (a mod b)·x' = g 이고 a mod b = a − (a // b)·b 이므로 x = y', y = x' − (a // b)·y'."""
    if b == 0:
        return a, 1, 0
    g, x, y = extended_gcd_recursive(b, a % b)
    return g, y, x - (a // b) * y


def mod_inverse(a: int, m: int) -> int:
    """a·x ≡ 1 (mod m) 인 0 ≤ x < m. m 이 소수가 아니어도 되고, gcd(a, m) ≠ 1 이면 ValueError."""
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("역원이 없습니다")
    return x % m


def solve_diophantine(a: int, b: int, c: int):
    """a·x + b·y = c 의 해 하나 (x, y). 해가 없으면 None. 해가 있을 조건은 gcd(a, b) | c."""
    g, x, y = extended_gcd(a, b)
    if g == 0:
        return (0, 0) if c == 0 else None
    if c % g:
        return None
    k = c // g
    return x * k, y * k


def diophantine_family(a: int, b: int, c: int):
    """모든 해를 (x0, y0, dx, dy) 로: x = x0 + dx·t, y = y0 + dy·t (t 는 정수). 해가 없으면 None. a = b = 0 이면 (c = 0 일 때) 모든 쌍이 해라서 표현하지 못한다."""
    solution = solve_diophantine(a, b, c)
    if solution is None:
        return None
    g = math.gcd(a, b)
    if g == 0:
        raise ValueError("a = b = 0 이면 해가 모든 (x, y) 입니다")
    return solution[0], solution[1], b // g, -(a // g)


def smallest_nonnegative_x_solution(a: int, b: int, c: int):
    """a·x + b·y = c 의 해 중 x 가 0 이상이면서 가장 작은 것 (x, y). b ≠ 0 이어야 한다. 해가 없으면 None."""
    family = diophantine_family(a, b, c)
    if family is None:
        return None
    x0, y0, dx, dy = family
    x = x0 % abs(dx)  # 0 ≤ x < |dx|: x0 에서 dx 의 배수만큼 움직인 가장 작은 비음수
    t = (x - x0) // dx  # 정확히 나누어떨어진다
    return x, y0 + dy * t


def count_nonnegative_solutions(a: int, b: int, c: int) -> int:
    """a·x + b·y = c 를 만족하는 x ≥ 0, y ≥ 0 인 정수 쌍의 수 (a, b > 0, c ≥ 0)."""
    first = smallest_nonnegative_x_solution(a, b, c)
    if first is None:
        return 0
    y = first[1]  # x 가 가장 작은 해라서 y 는 가장 크다. 이때 y > -a/g 이므로 y 가 음수이면 아래 식이 0 이 되어 해가 없다는 뜻과 맞는다
    y_step = a // math.gcd(a, b)
    return y // y_step + 1  # x 를 b/g 씩 늘릴 때 y 는 a/g 씩 줄어든다: 0 이상을 유지하는 횟수


def solve_linear_congruence(a: int, b: int, m: int):
    """a·x ≡ b (mod m) 의 해. 해가 있으면 (x0, m') 로, 모든 해가 x ≡ x0 (mod m') (m' = m / gcd(a, m)). 없으면 None."""
    g = math.gcd(a, m)
    if b % g:
        return None
    a, b, m = a // g, b // g, m // g
    return b * mod_inverse(a % m, m) % m, m


def main() -> None:
    a, b, c = map(int, sys.stdin.readline().split())
    answer = smallest_nonnegative_x_solution(a, b, c) if b else solve_diophantine(a, b, c)
    print(-1 if answer is None else f"{answer[0]} {answer[1]}")


if __name__ == "__main__":
    main()
