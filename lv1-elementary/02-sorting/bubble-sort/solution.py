"""버블 정렬 — 이웃한 두 원소를 비교해 큰 값을 뒤로 밀어 보내는 정렬

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 입력 리스트를 제자리에서 오름차순으로 정렬합니다. (안정 정렬)
- 반환값은 교환 횟수이며, 이는 뒤집힌 쌍(역전)의 수와 같습니다.
- 직접 실행하면 첫 줄에 N, 둘째 줄부터 N개의 정수(한 줄에 하나)를 받아 오름차순으로 한 줄에 하나씩 출력합니다.
"""
import sys


def bubble_sort(arr: list) -> int:
    """arr 을 제자리에서 오름차순으로 정렬하고, 교환한 횟수를 반환한다."""
    swaps = 0
    # 한 바퀴를 돌 때마다 남은 구간에서 가장 큰 값이 맨 뒤(end)에 자리 잡는다.
    for end in range(len(arr) - 1, 0, -1):
        swapped = False
        for j in range(end):
            if arr[j] > arr[j + 1]:  # 같을 때는 바꾸지 않아야 안정 정렬이 된다
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True
        if not swapped:  # 한 바퀴 동안 한 번도 안 바꿨다면 이미 정렬된 상태이므로 끝낸다
            break
    return swaps


def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    arr = [int(input()) for _ in range(n)]
    bubble_sort(arr)
    print("\n".join(map(str, arr)))


if __name__ == "__main__":
    main()
