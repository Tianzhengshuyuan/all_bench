inputs = {'sum_of_squares': 236}

from math import isqrt
from collections import Counter

def solve(sum_of_squares):
    S2 = sum_of_squares

    def check_and_return(non9, k):
        L = sorted(non9 + [9]*k)
        n = len(L)
        if n % 2 == 1:
            return None
        a, b = L[n//2 - 1], L[n//2]
        if (a + b) % 2 != 0:
            return None
        med = (a + b) // 2
        if med in set(L):
            return None
        cnt = Counter(L)
        if cnt.get(9, 0) != k:
            return None
        max_other = max((c for v, c in cnt.items() if v != 9), default=0)
        if max_other >= k:
            return None
        return sum(L)

    max_k = S2 // 81
    for k in range(2, max_k + 1):
        rem = S2 - 81 * k
        if rem < 0:
            continue
        ans = None

        def dfs(rem, start, counts, non9):
            nonlocal ans
            if ans is not None:
                return
            if rem == 0:
                res = check_and_return(non9, k)
                if res is not None:
                    ans = res
                return
            max_v = isqrt(rem)
            for v in range(start, max_v + 1):
                if v == 9:
                    continue
                c = counts.get(v, 0)
                if c >= k - 1:
                    continue
                counts[v] = c + 1
                non9.append(v)
                dfs(rem - v * v, v, counts, non9)
                non9.pop()
                if c == 0:
                    counts.pop(v, None)
                else:
                    counts[v] = c
                if ans is not None:
                    return

        dfs(rem, 1, {}, [])
        if ans is not None:
            return ans
    return None

sum_of_squares = 236
solve(sum_of_squares)

# 调用 solve
result = solve(inputs['sum_of_squares'])
print(result)