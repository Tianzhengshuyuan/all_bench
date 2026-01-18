inputs = {'N': 10}

def solve(N):
    from math import comb
    if N < 4:
        raise ValueError("N must be >= 4")
    def nCk(n, k):
        if k < 0 or k > n:
            return 0
        return comb(n, k)
    total_wins = nCk(4, 2) * nCk(N - 4, 2) + nCk(4, 3) * nCk(N - 4, 1) + nCk(4, 4) * nCk(N - 4, 0)
    return total_wins + 1

# 调用 solve
result = solve(inputs['N'])
print(result)