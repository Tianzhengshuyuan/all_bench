inputs = {'white_count': 25}

def solve(white_count):
    from math import comb
    n = 5
    avail_w = white_count
    avail_b = white_count
    total = 0
    for a in range(n + 1):       # number of white rows
        for b in range(n + 1):   # number of white columns
            if not ((a == 0 and b == 0) or (a == n and b == n) or (1 <= a <= n - 1 and 1 <= b <= n - 1)):
                continue
            w_needed = a * b
            b_needed = (n - a) * (n - b)
            if w_needed <= avail_w and b_needed <= avail_b:
                total += comb(n, a) * comb(n, b)
    return total

white_count = globals().get('white_count', 25)
solve(white_count)

# 调用 solve
result = solve(inputs['white_count'])
print(result)