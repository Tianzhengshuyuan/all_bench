inputs = {'white_chips': 25}

from math import comb

def solve(white_chips):
    n = 5
    black_chips = 25  # fixed by problem statement

    total = 0
    for r in range(n + 1):
        for c in range(n + 1):
            # Maximal configurations:
            # - r,c in 1..n-1 (both colors present), or
            # - r=c=0 (all black full), or
            # - r=c=n (all white full)
            if (r == 0) != (c == 0):
                continue
            if (r == n) != (c == n):
                continue
            white_need = r * c
            black_need = (n - r) * (n - c)
            if white_need <= white_chips and black_need <= black_chips:
                total += comb(n, r) * comb(n, c)
    return total

solve(25)

# 调用 solve
result = solve(inputs['white_chips'])
print(result)