inputs = {'white_count': 25}

def solve(white_count):
    from math import comb
    n = 5
    black_count = 25  # fixed per problem statement
    total = 0
    for r in range(n + 1):
        for c in range(n + 1):
            # Maximal valid structures:
            if not ((r == 0 and c == 0) or (r == n and c == n) or (1 <= r <= n - 1 and 1 <= c <= n - 1)):
                continue
            w_needed = r * c
            b_needed = (n - r) * (n - c)
            if w_needed <= white_count and b_needed <= black_count:
                total += comb(n, r) * comb(n, c)
    return total

solve(globals().get('white_count', 25))

# 调用 solve
result = solve(inputs['white_count'])
print(result)