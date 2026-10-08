### Merge Sort (병합 정렬)

# 분할 정복을 이용한 재귀 정렬 알고리즘으로 O(nlogn)의 시간 복잡도를 가짐
# 주어진 리스트를 먼저 길이가 1이 될 때까지 절반으로 쪼갠 뒤 합치는 과정에서 순서에 맞게 정렬
# 쪼갠 데이터를 보관할 메모리가 필요하므로, 메모리 측면에선 비효율적

### 예시 코드

def Merge_Sort(li: list):
    # li의 크기가 1이 될 때까지 반으로 나눠가며 재귀 선언
    if len(li) < 2:
        return li
    
    mid = len(li) // 2
    low_li = Merge_Sort(li[:mid])
    high_li = Merge_Sort(li[mid:])
    
    merged_li = []
    low = 0
    high = 0
    
    # 리스트를 low_li, high_li 두 리스트로 쪼개서 각 리스트 인덱스를 0부터 훑어가면서
    # 작은 순서대로 merged_li에 넣기
    while low < len(low_li) and high < len(high_li):
        if low_li[low] < high_li[high]:
            merged_li.append(low_li[low])
            low += 1
        else:
            merged_li.append(high_li[high])
            high += 1
    # 위 반복문을 다 돌고도 low_li, high_li에 남아있는 원소가 있을 수 있으므로 마지막에 전부 더하기
    merged_li += low_li[low:]
    merged_li += high_li[high:]
    
    return merged_li

### 예제

li = [1, 9, 2, 3, 7, 4, 5, 0, 6, 8]
print("before :", li)
ans = Merge_Sort(li)
print("after :", ans)