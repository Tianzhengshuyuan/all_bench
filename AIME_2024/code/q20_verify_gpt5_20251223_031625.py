inputs = {'white_chips': 25}

from math import comb

def solve(white_chips):
    n = 5
    black_chips = 25  # fixed by problem statement

    total = 0

    # All-black full grid
    if black_chips >= n * n:
        total += 1

    # Mixed configurations with both colors present
    for r in range(1, n):
        for c in range(1, n):
            white_need = r * c
            black_need = (n - r) * (n - c)
            if white_need <= white_chips and black_need <= black_chips:
                total += comb(n, r) * comb(n, c)

    # All-white full grid
    if white_chips >= n * n:
        total += 1

    return total

solve(25)

# 调用 solve
result = solve(inputs['white_chips'])
print(result)