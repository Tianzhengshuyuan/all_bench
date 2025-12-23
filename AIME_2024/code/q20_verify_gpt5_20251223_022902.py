inputs = {'white_chips': 25}

def solve(white_chips):
    from math import comb
    n = 5
    black_chips = 25  # fixed by problem statement

    ans = 0
    for rW in range(n + 1):
        for cW in range(n + 1):
            # Maximal configurations:
            # - both rW and cW in 1..n-1 (both colors present and block any addition)
            # - all-black (rW=cW=0) or all-white (rW=cW=n) full grids
            maximal = (
                (1 <= rW <= n - 1 and 1 <= cW <= n - 1) or
                (rW == 0 and cW == 0) or
                (rW == n and cW == n)
            )
            if not maximal:
                continue

            whites_used = rW * cW
            blacks_used = (n - rW) * (n - cW)
            if whites_used <= white_chips and blacks_used <= black_chips:
                ans += comb(n, rW) * comb(n, cW)
    return ans

solve(25)

# 调用 solve
result = solve(inputs['white_chips'])
print(result)