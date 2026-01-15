inputs = {'white_count': 25}

def solve(white_count):
    from math import comb
    n = 5
    total = 0
    avail_w = white_count
    avail_b = white_count
    for r in range(n + 1):
        for c in range(n + 1):
            if not ((r == 0 and c == 0) or (r == n and c == n) or (1 <= r <= n - 1 and 1 <= c <= n - 1)):
                continue
            w_needed = r * c
            b_needed = (n - r) * (n - c)
            if w_needed <= avail_w and b_needed <= avail_b:
                total += comb(n, r) * comb(n, c)
    return total

white_count = globals().get('white_count', 25)
solve(white_count)

# 调用 solve
result = solve(inputs['white_count'])
print(result)