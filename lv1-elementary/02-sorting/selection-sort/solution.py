"""선택 정렬 — 남은 구간에서 가장 작은 값을 골라 맨 앞으로 보내는 정렬

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 입력 리스트를 제자리에서 오름차순으로 정렬합니다. (안정 정렬이 아님)
- 직접 실행하면 첫 줄에 N, 둘째 줄부터 N개의 정수를 받아 오름차순으로 한 줄에 하나씩 출력합니다.
"""
import sys


def selection_sort(arr: list) -> None:
    """arr 을 제자리에서 오름차순으로 정렬한다."""
    n = len(arr)
    for i in range(n - 1):
        # arr[i:] 중 가장 작은 값의 위치를 찾는다.
        smallest = i
        for j in range(i + 1, n):
            if arr[j] < arr[smallest]:
                smallest = j
        # 맨 앞과 맞바꾼다. 멀리 떨어진 원소끼리 바뀌므로 같은 값의 순서가 뒤집힐 수 있다.
        if smallest != i:
            arr[i], arr[smallest] = arr[smallest], arr[i]


def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    arr = [int(input()) for _ in range(n)]
    selection_sort(arr)
    print("\n".join(map(str, arr)))


if __name__ == "__main__":
    main()
