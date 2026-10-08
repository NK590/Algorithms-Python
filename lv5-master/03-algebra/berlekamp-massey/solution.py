"""벌레캠프-매시(Berlekamp–Massey) — 수열의 앞부분만 보고 그것을 만드는 가장 짧은 선형 점화식을 찾기, O(n²)

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 길이 L 의 선형 점화식: L ≤ i 인 모든 i 에서 s[i] = c[1]·s[i-1] + … + c[L]·s[i-L]  (mod p, p 는 소수).
  berlekamp_massey(seq, mod) 는 seq 전체를 만족하는 점화식 중 L 이 가장 작은 것의 c = [c1, …, cL] 을 돌려준다 (이때 L = len(c); 선형 복잡도).
- 현재의 점화식 C(x) = 1 - c1 x - … - cL x^L 으로 i 번째 항을 예측했을 때의 오차 d 가 0 이면 그대로 두고, 아니면 "마지막으로 틀렸던 점화식" B 를 d/b 배, m 칸 밀어서 빼 오차를 지운다 (b 는 그때의 오차).
  2L ≤ i 였다면 길이도 늘려야 하므로 L = i + 1 - L 로 바꾸고 B, b, m 을 갱신한다. 항 하나에 O(L) 이라 전체 O(n²).
- 원래 점화식의 길이가 L 이면 2L 개의 항이면 충분하다: 앞의 2L 항만 주면 같은 점화식(최소 다항식) 이 나온다. 그보다 적게 주면 다른 (더 짧은 우연의) 점화식이 나올 수 있다.
- nth_term(c, init, k, mod): k 번째 항을 O(L² log k) (특성 다항식으로 x^k 를 나누는 키타마사 방식). 점화식을 구한 뒤 아주 먼 항을 얻는 데 쓴다.
- extend(seq, count, mod): 앞부분에서 찾은 점화식으로 count 개의 항을 더 이어 쓴다.
- 직접 실행하면 Library Checker "Find Linear Recurrence" 형식 — `N`, 이어서 a_0 … a_{N-1} (mod 998244353) — 를 받아 길이 L 과 c_1 … c_L 을 출력합니다.
"""
import sys
from typing import Sequence

MOD = 998244353


def berlekamp_massey(seq: Sequence[int], mod: int = MOD) -> list[int]:
    """seq 전체를 만족하는 가장 짧은 선형 점화식의 계수 [c1, …, cL] (mod 는 소수)."""
    n = len(seq)
    connection = [1] + [0] * n  # C(x): s[i] + C[1] s[i-1] + … = 0 꼴로 보관 (부호를 반대로)
    previous = [1] + [0] * n  # 길이가 마지막으로 늘어났을 때의 C
    length = 0
    gap = 1  # 마지막 갱신 이후 지난 칸 수 (m)
    last_error = 1  # 그때의 오차 (b)
    for i in range(n):
        error = seq[i] % mod
        for j in range(1, length + 1):
            error = (error + connection[j] * seq[i - j]) % mod
        if error == 0:
            gap += 1
            continue
        saved = connection[:]
        coefficient = error * pow(last_error, mod - 2, mod) % mod
        for j in range(gap, n + 1):
            connection[j] = (connection[j] - coefficient * previous[j - gap]) % mod
        if 2 * length <= i:
            length = i + 1 - length
            previous, last_error, gap = saved, error, 1
        else:
            gap += 1
    return [(-connection[j]) % mod for j in range(1, length + 1)]


def check_recurrence(seq: Sequence[int], coefficients: Sequence[int], mod: int = MOD) -> bool:
    """seq 가 점화식을 (길이 L 이후의 모든 항에서) 만족하는가."""
    length = len(coefficients)
    return all(
        (seq[i] - sum(coefficients[j] * seq[i - 1 - j] for j in range(length))) % mod == 0
        for i in range(length, len(seq))
    )


def _poly_mul_mod(a: list[int], b: list[int], char_poly: list[int], mod: int) -> list[int]:
    """a(x)·b(x) 를 특성 다항식 x^L - c1 x^{L-1} - … - cL 로 나눈 나머지 (계수는 낮은 차수부터 길이 L)."""
    length = len(char_poly)
    product = [0] * (2 * length - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                product[i + j] = (product[i + j] + x * y) % mod
    for degree in range(2 * length - 2, length - 1, -1):
        top = product[degree]
        if top:
            for j in range(length):  # x^L = c1 x^{L-1} + … + cL
                product[degree - 1 - j] = (product[degree - 1 - j] + top * char_poly[j]) % mod
    return product[:length]


def nth_term(coefficients: Sequence[int], initial: Sequence[int], k: int, mod: int = MOD) -> int:
    """점화식 s[i] = Σ c[j]·s[i-j] 와 처음 L 개의 항 initial 에서 k 번째 항 (0부터), O(L² log k)."""
    length = len(coefficients)
    if length == 0:
        return 0  # 길이 0 점화식은 모든 항이 0
    if k < length:
        return initial[k] % mod
    base = [0] * length
    result = [0] * length
    result[0] = 1
    if length == 1:
        base[0] = coefficients[0] % mod  # x mod (x - c1) = c1
    else:
        base[1] = 1
    char_poly = [c % mod for c in coefficients]
    power = k
    while power:
        if power & 1:
            result = _poly_mul_mod(result, base, char_poly, mod)
        base = _poly_mul_mod(base, base, char_poly, mod)
        power >>= 1
    return sum(r * initial[i] for i, r in enumerate(result)) % mod


def extend(seq: Sequence[int], count: int, mod: int = MOD) -> list[int]:
    """seq 의 점화식을 찾아 뒤에 count 개의 항을 더 이은 새 리스트."""
    coefficients = berlekamp_massey(seq, mod)
    result = list(seq)
    length = len(coefficients)
    for _ in range(count):
        i = len(result)
        result.append(sum(coefficients[j] * result[i - 1 - j] for j in range(length)) % mod)
    return result


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    seq = [int(x) for x in data[1:1 + n]]
    coefficients = berlekamp_massey(seq, MOD)
    print(len(coefficients))
    print(" ".join(map(str, coefficients)))


if __name__ == "__main__":
    main()
