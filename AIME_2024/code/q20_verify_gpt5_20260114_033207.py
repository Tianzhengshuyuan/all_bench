inputs = {'white_count': 25}

def solve(white_count):
    from math import comb
    n = 5
    total = 0

    # Extremes: all white or all black (requires n*n chips of that color)
    if white_count >= n * n:
        total += 2

    # Mixed cases: choose 1..n-1 white rows and 1..n-1 white columns
    # Fill white on their intersections and black on the complement block
    for r in range(1, n):
        for c in range(1, n):
            w_needed = r * c
            b_needed = (n - r) * (n - c)
            if w_needed <= white_count and b_needed <= white_count:
                total += comb(n, r) * comb(n, c)

    return total

solve(white_count)

# 调用 solve
result = solve(inputs['white_count'])
print(result)