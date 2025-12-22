inputs = {'n': 10}

from math import comb

def solve(n):
    # Case 1: sides parallel to some edges of the dodecagon
    a = n // 2 - 1
    b = n // 4
    case1_per_dir = 2 * comb(a, 2) * comb(b, 2) - comb(b, 2) ** 2
    case1 = case1_per_dir * 3
    
    # Case 2: sides not parallel
    c = n // 3
    d = n // 2
    case2_per_dir = comb(c, 2) ** 2 + 2 * (comb(d, 2) - comb(c, 2))
    case2 = case2_per_dir * 3
    
    return case1 + case2

# 调用 solve
result = solve(inputs['n'])
print(result)