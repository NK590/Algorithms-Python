### KMP Algorithm (KMP 알고리즘)

# 주어진 문자열(이하 word)에 어떤 문자열(이하 test)이 있는지 검색하는 대표적인 문자열 탐색 알고리즘
# 먼저 test 문자열의 접두사와 접미사 중에 같은 문자열이 있는지 확인하여 LPS(Longest Prefix & Suffix)
# 리스트를 작성함
# word 문자열의 처음부터 부분 문자열이 test 문자열과 일치하는 지 확인한 뒤, 일치할 경우 문제 조건에 따라
# 적당한 값을 출력하고 일치하지 않을 경우 위 LPS 리스트 값에 따라 word 문자열에서 체크할 값을 '건너뛰어서' 
# 건너뛴 값 이후로 위 탐색을 반복함

# word의 길이를 n, test의 길이를 m이라고 하면 일반적인 이중 반복문 탐색은 시간 복잡도가 O(n*m)이지만,
# KMP 알고리즘을 사용하면 시간 복잡도를 O(n+m)으로 획기적으로 줄일 수 있음

### 예시 코드

# 아래에서 정의하는 LPS 리스트를 실패 함수(Failure Function)라고 부르는 경우도 있음
def computeLPS(word: str):
    # 접두사, 접미사의 일치 여부를 나타내는 LPS 리스트 선언
    # LPS 리스트의 인덱스가 부분 문자열의 길이를 나타내고, 그 원소가 일치하는 길이를 나타냄
    lps = [0 for _ in range(len(word))]
    prefix = 0
    suffix = 1
    while suffix < len(word):
        # 값이 일치할 시 현재까지의 접두사 = 접미사 길이 값을 저장하고, 그 다음 접두사/접미사 값 확인
        if word[suffix] == word[prefix]:
            prefix += 1
            lps[suffix] = prefix
            suffix += 1
        else:
            # 값이 일치하지 않을 시 prefix가 0이 아니면 이전 인덱스에서는 같았으므로 줄여서 다시 검사
            if prefix != 0:
                prefix = lps[prefix-1]
            # prefix가 0일 경우, 일치하는 문자열이 없으므로 lps[suffix]에 0을 넣고 한 칸 늘려서 탐색 반복
            else:
                lps[suffix] = 0
                suffix += 1
    return lps

def KMP(word: str, test: str):
    l_word = len(word)
    l_test = len(test) 
    
    # lps 리스트를 계산
    lps = computeLPS(test)
    ans = []
    
    w_index = 0
    t_index = 0
    
    while w_index < l_word:
        # 주어진 문자열과 테스트 문자열의 문자가 일치할 시 그 다음 글자 확인
        if test[t_index] == word[w_index]:
            w_index += 1
            t_index += 1
        elif test[t_index] != word[w_index]:
            # 일치하지 않을 때, 테스트 문자열 인덱스가 0이 아닐 시 lps만큼 건너뜀
            if t_index != 0:
                t_index = lps[t_index-1]
            # 테스트 문자열 인덱스가 0일 때는 주어진 문자열 인덱스를 하나 늘림
            else:
                w_index += 1
        
        # 테스트 문자열을 마지막까지 확인했을 때, 해당 값을 저장하고 lps만큼 건너뜀
        if t_index == l_test:
            ans.append(w_index - t_index + 1)
            t_index = lps[t_index - 1]
    return ans

### 예제

word = 'ABC ABCDAB ABCDABCDABDE'
test = 'ABCDABD'

print('Count :', len(KMP(word, test)), 'Position :', KMP(word, test))

word = 'ABABABABABABABABABABA'
test = 'ABABA'

print('Count :', len(KMP(word, test)), 'Position :', KMP(word, test))

