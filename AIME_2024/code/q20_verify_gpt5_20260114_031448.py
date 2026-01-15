inputs = {'white_count': 25}

from math import comb

def solve(white_count):
    n = 5
    total = 0
    for r in range(n + 1):
        for c in range(n + 1):
            # Maximal, valid structures:
            if not ((r == 0 and c == 0) or (r == n and c == n) or (1 <= r <= n - 1 and 1 <= c <= n - 1)):
                continue
            # Chip availability constraints (equal white/black supply = white_count)
            if r * c > white_count:
                continue
            if (n - r) * (n - c) > white_count:
                continue
            total += comb(n, r) * comb(n, c)
    return total

solve(globals().get('white_count', 25))

# 调用 solve
result = solve(inputs['white_count'])
print(result)