inputs = {'set_size': 10}

def solve(set_size):
    from math import comb, gcd

    def C(n, k):
        return comb(n, k) if 0 <= k <= n else 0

    N = set_size
    # Count of outcomes with at least 2 matches
    denom = sum(C(4, k) * C(N - 4, 4 - k) for k in range(2, 5))
    if denom == 0:
        return None

    m, n = 1, denom  # favorable count for grand prize is 1
    g = gcd(m, n)
    return m // g + n // g

solve(set_size)

# 调用 solve
result = solve(inputs['set_size'])
print(result)