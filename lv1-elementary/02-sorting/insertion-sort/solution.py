"""삽입 정렬 — 앞쪽의 정렬된 구간에 새 원소를 알맞은 자리에 끼워 넣는 정렬

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 입력 리스트를 제자리에서 오름차순으로 정렬합니다. (안정 정렬)
- 직접 실행하면 첫 줄에 N, 둘째 줄부터 N개의 정수를 받아 오름차순으로 한 줄에 하나씩 출력합니다.
"""
import sys


def insertion_sort(arr: list) -> None:
    """arr 을 제자리에서 오름차순으로 정렬한다."""
    for i in range(1, len(arr)):
        # arr[:i] 는 이미 정렬되어 있다. arr[i] 를 꺼내 들고 들어갈 자리를 찾는다.
        value = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > value:  # 엄격하게 큰 값만 밀어야 같은 값의 순서가 유지된다
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = value


def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    arr = [int(input()) for _ in range(n)]
    insertion_sort(arr)
    print("\n".join(map(str, arr)))


if __name__ == "__main__":
    main()
