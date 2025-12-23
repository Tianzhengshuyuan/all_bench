inputs = {'set_size': 546}

def solve(set_size):
    from math import comb

    def C(n, k):
        return comb(n, k) if 0 <= k <= n else 0

    N = set_size
    denom = sum(C(4, k) * C(N - 4, 4 - k) for k in range(2, 5))
    if denom == 0:
        return None
    return 1 + denom

solve(10)

# 调用 solve
result = solve(inputs['set_size'])
print(result)