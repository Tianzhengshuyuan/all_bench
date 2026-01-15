inputs = {'white_count': 25}

from math import comb

def solve(white_count):
    n = 5
    total = 0

    # Extremes: all white or all black if we can fill the whole grid with one color
    if white_count >= n * n:
        total += 2

    # Mixed cases: both white and black rows/cols present (no empty row/col), hence 1..n-1
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