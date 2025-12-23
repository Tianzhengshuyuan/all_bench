inputs = {'white_chips': 25}

def solve(white_chips):
    from math import comb
    n = 5
    black_chips = 25  # fixed by problem statement
    ans = 0
    for rW in range(n + 1):
        for cW in range(n + 1):
            valid = (rW == 0 and cW == 0) or (rW == n and cW == n) or (1 <= rW <= n - 1 and 1 <= cW <= n - 1)
            if not valid:
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