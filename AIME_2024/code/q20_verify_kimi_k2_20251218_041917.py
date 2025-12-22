inputs = {'n': 25}

from math import comb

def solve(n):
    total = 0
    for rW in range(n + 1):
        for cW in range(n + 1):
            w_needed = rW * cW
            b_needed = (n - rW) * (n - cW)
            if w_needed <= n and b_needed <= n:
                total += comb(n, rW) * comb(n, cW)
    return total

# 调用 solve
result = solve(inputs['n'])
print(result)