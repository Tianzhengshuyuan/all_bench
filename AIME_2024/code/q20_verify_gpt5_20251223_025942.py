inputs = {'white_chips': 25}

def solve(white_chips):
    from math import comb
    n = 5
    black_chips = 25  # fixed by problem statement

    total = 0
    for r in range(n + 1):
        for c in range(n + 1):
            white_need = r * c
            black_need = (n - r) * (n - c)

            # Case A: mixed colors (both r and c are between 1 and n-1)
            if 1 <= r <= n - 1 and 1 <= c <= n - 1:
                if white_need <= white_chips and black_need <= black_chips:
                    total += comb(n, r) * comb(n, c)
            # Case B: all-black full grid
            elif r == 0 and c == 0:
                if black_need <= black_chips:
                    total += 1
            # Case C: all-white full grid
            elif r == n and c == n:
                if white_need <= white_chips:
                    total += 1
            # Other (r,c) pairs are impossible in maximal configurations
    return total

solve(white_chips)

# 调用 solve
result = solve(inputs['white_chips'])
print(result)