inputs = {'set_size': 10}

from math import comb

def solve(set_size):
    def C(n, k):
        if n < 0 or k < 0 or k > n:
            return 0
        return comb(n, k)
    n = set_size
    denom = C(4, 2) * C(n - 4, 2) + C(4, 3) * C(n - 4, 1) + C(4, 4) * C(n - 4, 0)
    return 1 + denom

solve(set_size)

# 调用 solve
result = solve(inputs['set_size'])
print(result)