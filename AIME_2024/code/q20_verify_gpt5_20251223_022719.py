inputs = {'white_chips': 25}

def solve(white_chips):
    from math import comb
    n = 5
    black_chips = 25  # fixed by problem statement

    ans = 0
    # Require both colors to appear (exclude all-white and all-black grids)
    for rW in range(1, n):  # 1..4
        for cW in range(1, n):  # 1..4
            whites_used = rW * cW
            blacks_used = (n - rW) * (n - cW)
            if whites_used <= white_chips and blacks_used <= black_chips:
                ans += comb(n, rW) * comb(n, cW)
    return ans

solve(25)

# 调用 solve
result = solve(inputs['white_chips'])
print(result)