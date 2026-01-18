inputs = {'white_count': 25}

def solve(white_count):
    from math import comb
    n = 5
    m = int(white_count)
    total = 0

    # Extreme cases: all white or all black
    if n * n <= m:
        total += 2  # one all-white + one all-black

    # Mixed cases: choose nonempty proper subsets of rows and columns for white
    # Ensure both color blocks fit within available chips
    for r in range(1, n):
        cr = comb(n, r)
        for c in range(1, n):
            if r * c <= m and (n - r) * (n - c) <= m:
                total += cr * comb(n, c)

    return total

# 调用 solve
result = solve(inputs['white_count'])
print(result)