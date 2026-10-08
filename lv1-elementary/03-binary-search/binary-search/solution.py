### Binary Search (이진 탐색)

# 정렬되어 있는 리스트에서 특정 원소 값을 찾아내는 알고리즘
# 리스트를 절반씩 나눠가며 해당 값이 어느 쪽에 속해있는지 찾아가는 알고리즘으로,
# 리스트 내 극히 일부 데이터만 확인해도 탐색이 가능하며 시간복잡도가 O(logn)으로 매우 효율적
# 단, 단조증가(감소)하는 데이터에만 사용이 가능하고, 그 외에 경우에는 이분 탐색을 적용할 수 없음

### 예시 코드 1

def Binary_Search(li: list, num: int):
    # 시작점, 끝점을 정의
    low = 0
    high = len(li) - 1
    
    # 시작점이 끝점보다 커질때까지 반복
    while low <= high:
        # 중간점 정의
        mid = (low + high) // 2
        
        # num이 li의 중간 원소보다 작을 경우 끝점을 mid로 끌어내림
        if num < li[mid]:
            high = mid - 1
        # num이 li의 중간 원소보다 클 경우 시작점을 mid로 끌어올림
        elif li[mid] < num:
            low = mid + 1
        # num이 li의 중간 원소와 같을 경우 탐색이 끝났으므로 mid를 리턴
        else:
            return mid
    
    # 반복문을 돌 때까지 못 발견했으면 num은 li 안에 없음
    return -1

### 예시 코드 2
# 재귀적으로도 구현 가능

def Binary_Search_2(li: list, num: int, low: int, high: int):
    if low > high:
        return -1
    
    mid = (low + high) // 2
    
    if num < li[mid]:
        high = mid - 1
    elif li[mid] < num:
        low = mid + 1
    else:
        return mid
    
    return Binary_Search_2(li, num, low, high)

### 예시 코드 3
# 파이썬 내장 bisect 모듈을 사용하면 별다른 구현 없이 사용 가능

from bisect import bisect_left, bisect_right

# bisect 함수는 left, right에 따라 각각 왼쪽, 오른쪽 인덱스를 구함
# 만약 주어진 리스트 안에 찾는 원소가 없을 경우도, 가장 가까운 인덱스를 출력
def Binary_Search_3_left(li, num):
    return bisect_left(li, num)

def Binary_Search_3_right(li, num):
    return bisect_right(li, num)

### 예제

li = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
num1 = 8
num2 = 10

print(Binary_Search(li, num1))
print(Binary_Search(li, num2))

print(Binary_Search_2(li, num1, 0, 10))
print(Binary_Search_2(li, num2, 0, 10))

print(Binary_Search_3_left(li, num1))
print(Binary_Search_3_left(li, num2))

print(Binary_Search_3_right(li, num1))
print(Binary_Search_3_right(li, num2))