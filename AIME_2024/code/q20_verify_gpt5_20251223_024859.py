inputs = {'white_chips': 25}

def solve(white_chips):
    from math import comb
    S = white_chips
    n = 5
    total = 0
    # All white
    if S >= n * n:
        total += 1
    # All black
    if S >= n * n:
        total += 1
    # Mixed colors with both colors present in rows and columns
    for r in range(1, n):
        for c in range(1, n):
            w = r * c
            b = (n - r) * (n - c)
            if w <= S and b <= S:
                total += comb(n, r) * comb(n, c)
    return total

solve(white_chips)

# 调用 solve
result = solve(inputs['white_chips'])
print(result)