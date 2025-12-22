inputs = {'S_size': 673}

from math import comb, gcd

def solve(S_size):
    if S_size < 4:
        raise ValueError("S_size must be at least 4")
    # Count outcomes where overlap is k between her 4 and the drawn 4
    def count_k(k):
        r = 4 - k  # number drawn from outside her picks
        if r < 0 or S_size - 4 < r:
            return 0
        return comb(4, k) * comb(S_size - 4, r)

    numerator = count_k(4)
    denominator = count_k(2) + count_k(3) + count_k(4)

    g = gcd(numerator, denominator)
    m = numerator // g
    n = denominator // g
    return m + n

# 调用 solve
result = solve(inputs['S_size'])
print(result)