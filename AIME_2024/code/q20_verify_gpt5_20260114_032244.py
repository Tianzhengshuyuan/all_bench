inputs = {'white_count': 25}

def solve(white_count):
    from math import comb
    n = 5
    black_count = white_count
    total = 0

    # Extremes: all white or all black (requires n*n chips of that color)
    if white_count >= n * n and black_count >= n * n:
        total += 2

    # Mixed cases: both row colors and both column colors appear (counts 1..n-1)
    for rw in range(1, n):
        for cw in range(1, n):
            white_needed = rw * cw
            black_needed = (n - rw) * (n - cw)
            if white_count >= white_needed and black_count >= black_needed:
                total += comb(n, rw) * comb(n, cw)

    return total

ans = solve(white_count)

# 调用 solve
result = solve(inputs['white_count'])
print(result)