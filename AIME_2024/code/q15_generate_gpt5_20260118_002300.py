inputs = {'turns': 5}

def solve(turns):
    from math import comb
    def compositions(n, k):
        if k < 1 or k > n:
            return 0
        return comb(n - 1, k - 1)
    S = turns + 1
    r_segments = (S + 1) // 2
    u_segments = S // 2
    return 2 * compositions(8, r_segments) * compositions(8, u_segments)

solve(4)

# 调用 solve
result = solve(inputs['turns'])
print(result)