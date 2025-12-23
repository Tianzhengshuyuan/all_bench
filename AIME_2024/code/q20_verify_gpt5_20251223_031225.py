inputs = {'white_chips': 25}

from math import comb

def solve(white_chips):
    n = 5
    black_chips = 25
    total = 0
    for r in range(n + 1):
        for c in range(n + 1):
            if (r == 0) != (c == 0):
                continue
            if (r == n) != (c == n):
                continue
            w = r * c
            b = (n - r) * (n - c)
            if w <= white_chips and b <= black_chips:
                total += comb(n, r) * comb(n, c)
    return total

solve(25)

# 调用 solve
result = solve(inputs['white_chips'])
print(result)