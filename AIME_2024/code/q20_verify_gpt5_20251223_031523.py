inputs = {'white_chips': 25}

def solve(white_chips):
    from math import comb
    n = 5
    total = 0
    for r in range(1, n):
        for c in range(1, n):
            white_needed = r * c
            black_needed = (n - r) * (n - c)
            if white_needed <= white_chips and black_needed <= white_chips:
                total += comb(n, r) * comb(n, c)
    if n * n <= white_chips:
        total += 2
    return total

solve(white_chips)

# 调用 solve
result = solve(inputs['white_chips'])
print(result)