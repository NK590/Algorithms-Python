"""오일러 피 함수 φ(n) — 1 이상 n 이하의 수 중 n 과 서로소인 수의 개수

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 곱셈 공식: φ(n) = n · Π (1 - 1/p)  (p 는 n 의 서로 다른 소인수). 소인수분해를 하면 O(√n) 에 구합니다.
- 성질: φ(p) = p - 1 (소수),  φ(p^k) = p^k - p^(k-1),  gcd(m, n) = 1 이면 φ(mn) = φ(m)φ(n),  Σ_{d | n} φ(d) = n.
- 오일러 정리: gcd(a, n) = 1 이면 a^φ(n) ≡ 1 (mod n).  페르마의 소정리(n 이 소수)의 일반화입니다.
- 직접 실행하면 `N` 을 받아 φ(N) 을 출력합니다.
"""
import sys


def phi(n: int) -> int:
    """φ(n). 소인수를 하나씩 찾아 result 에서 result / p 를 뺀다 (result 에 (1 - 1/p) 를 곱하는 것과 같다). φ(1) = 1."""
    if n < 1:
        raise ValueError("n 은 1 이상이어야 합니다")
    result = n
    remaining = n
    p = 2
    while p * p <= remaining:
        if remaining % p == 0:
            while remaining % p == 0:  # 같은 소인수는 한 번만 처리한다
                remaining //= p
            result -= result // p
        p += 1
    if remaining > 1:  # √n 이하로 다 나눈 뒤 남은 소수
        result -= result // remaining
    return result


def phi_table(limit: int) -> list[int]:
    """φ(0..limit) 을 한꺼번에. 에라토스테네스의 체와 같은 틀로, 소수 p 를 만날 때마다 p 의 배수 x 에서 x / p 를 뺀다. O(n log log n)."""
    table = list(range(limit + 1))
    for i in range(2, limit + 1):
        if table[i] == i:  # 아직 건드려지지 않았다면 소수
            for j in range(i, limit + 1, i):
                table[j] -= table[j] // i
    return table


def pow_mod_large_exponent(a: int, e: int, m: int) -> int:
    """a^e mod m 을 지수를 φ(m) 으로 줄여서 계산한다 (확장 오일러 정리).

    e ≥ φ(m) 이면 gcd(a, m) 이 1 이 아니어도 a^e ≡ a^(e mod φ(m) + φ(m)) (mod m). 지수가 매우 클 때(탑 모양 거듭제곱 등) 지수를 줄이는 데 쓴다."""
    ph = phi(m)
    if e >= ph:
        e = e % ph + ph
    return pow(a, e, m)


def count_proper_reduced_fractions(n: int) -> int:
    """0 < p < q ≤ n 이고 gcd(p, q) = 1 인 분수 p/q 의 개수 = Σ_{q=2..n} φ(q). 분모가 q 인 기약분수는 φ(q) 개이기 때문이다."""
    table = phi_table(n)
    return sum(table[q] for q in range(2, n + 1))


def main() -> None:
    n = int(sys.stdin.readline())
    print(phi(n))


if __name__ == "__main__":
    main()
