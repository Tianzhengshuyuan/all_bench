inputs = {'white_chips': 25}

from math import comb

def solve(white_chips):
    n = 5
    total = 0
    for r in range(n + 1):
        for c in range(n + 1):
            if (r == 0 and c > 0) or (c == 0 and r > 0) or (r == n and c < n) or (c == n and r < n):
                continue
            total += comb(n, r) * comb(n, c)
    return total

solve(white_chips)

# 调用 solve
result = solve(inputs['white_chips'])
print(result)