inputs = {'white_chips': 25}

from math import comb

def solve(white_chips):
    n = 5
    black_chips = 25
    total = 0
    for r in range(n + 1):
        for c in range(n + 1):
            # Maximality requires: r=0 iff c=0, and r=n iff c=n
            if (r == 0) != (c == 0):
                continue
            if (r == n) != (c == n):
                continue
            white_need = r * c
            black_need = (n - r) * (n - c)
            if white_need > white_chips or black_need > black_chips:
                continue
            total += comb(n, r) * comb(n, c)
    return total

solve(25)

# 调用 solve
result = solve(inputs['white_chips'])
print(result)