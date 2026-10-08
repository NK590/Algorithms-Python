"""모노톤 스택 — 스택의 값이 항상 단조(증가 또는 감소)가 되게 유지하며, 각 원소의 "다음으로 큰/작은 원소" 같은 값을 O(n) 에 구하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 인덱스를 스택에 쌓는다. 새 원소가 들어올 때 스택 맨 위가 "답을 찾았다"는 조건이면 pop 하면서 답을 기록하고, 그 뒤에 새 원소를 push 합니다.
  각 원소는 한 번 push, 한 번 pop 되므로 전체 O(n).
- 여섯 가지: 오큰수(다음으로 큰 수), 다음으로 작은 수, 이전으로 작은 수, 히스토그램의 가장 큰 직사각형, 며칠 뒤에 더 따뜻한가, 빗물 담기.
- 직접 실행하면 `N` 과 수열을 받아 각 원소의 오큰수(오른쪽에서 처음으로 더 큰 수, 없으면 -1)를 출력합니다.
"""
import sys


def next_greater(numbers: list[int]) -> list[int]:
    """각 원소의 오른쪽에서 처음으로 나오는 '더 큰 수' (없으면 -1).

    스택에는 아직 답을 못 찾은 원소의 위치를 쌓는다. 스택 안의 값은 위로 갈수록 작거나 같다(내림차순)."""
    result = [-1] * len(numbers)
    stack: list[int] = []
    for i, x in enumerate(numbers):
        while stack and numbers[stack[-1]] < x:
            result[stack.pop()] = x  # x 가 이들의 오큰수다
        stack.append(i)
    return result


def next_smaller(numbers: list[int]) -> list[int]:
    """각 원소의 오른쪽에서 처음으로 나오는 '더 작은 수' (없으면 -1)."""
    result = [-1] * len(numbers)
    stack: list[int] = []
    for i, x in enumerate(numbers):
        while stack and numbers[stack[-1]] > x:
            result[stack.pop()] = x
        stack.append(i)
    return result


def previous_smaller_index(numbers: list[int]) -> list[int]:
    """각 원소의 왼쪽에서 처음으로 나오는 '더 작은 수'의 위치 (없으면 -1). 스택에는 단조 증가하는 값들의 위치가 남는다."""
    result = [-1] * len(numbers)
    stack: list[int] = []
    for i, x in enumerate(numbers):
        while stack and numbers[stack[-1]] >= x:
            stack.pop()
        result[i] = stack[-1] if stack else -1
        stack.append(i)
    return result


def largest_rectangle_in_histogram(heights: list[int]) -> int:
    """너비 1 인 막대들로 이루어진 히스토그램 안에 들어가는 가장 큰 직사각형의 넓이.

    막대 i 를 높이로 하는 직사각형은 왼쪽·오른쪽으로 i 보다 낮은 막대를 처음 만나기 직전까지 넓어진다.
    스택에서 막대가 pop 될 때(자기보다 낮은 막대를 오른쪽에서 만났을 때) 왼쪽 경계는 새로 맨 위가 된 원소가 알려 준다."""
    best = 0
    stack: list[int] = []
    for i, h in enumerate(list(heights) + [0]):  # 끝에 높이 0 을 붙여 남은 막대를 모두 정리한다
        while stack and heights[stack[-1]] >= h:
            height = heights[stack.pop()]
            left = stack[-1] + 1 if stack else 0
            best = max(best, height * (i - left))
        stack.append(i)
    return best


def days_until_warmer(temperatures: list[int]) -> list[int]:
    """각 날짜에서 더 따뜻해지기까지 며칠을 기다려야 하는지 (오지 않으면 0). 오큰수의 위치 차이."""
    result = [0] * len(temperatures)
    stack: list[int] = []
    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:
            j = stack.pop()
            result[j] = i - j
        stack.append(i)
    return result


def trapped_rain_water(heights: list[int]) -> int:
    """높이 heights 의 막대 사이에 고이는 빗물의 양. 스택으로 '움푹 팬 곳' 을 한 층씩 채운다."""
    water = 0
    stack: list[int] = []
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] < h:
            bottom = heights[stack.pop()]
            if not stack:
                break
            left = stack[-1]
            water += (min(heights[left], h) - bottom) * (i - left - 1)
        stack.append(i)
    return water


def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    numbers = list(map(int, input().split()))[:n]
    print(" ".join(map(str, next_greater(numbers))))


if __name__ == "__main__":
    main()
