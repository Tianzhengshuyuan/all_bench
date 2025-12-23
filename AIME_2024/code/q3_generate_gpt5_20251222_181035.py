inputs = {'k': 7}

from math import comb
from math import gcd

def solve(k):
    N = 10  # size of S = {1, 2, ..., 10}
    if not (0 <= k <= N):
        return None
    denom = 0
    for r in range(2, k + 1):
        # ways to have exactly r matches between two k-subsets of an N-set
        if 0 <= k - r <= N - k:
            denom += comb(k, r) * comb(N - k, k - r)
    if denom == 0:
        return None
    m, n = 1, denom
    g = gcd(m, n)
    m //= g
    n //= g
    return m + n

solve(4)

# 调用 solve
result = solve(inputs['k'])
print(result)