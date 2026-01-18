inputs = {'size': 10}

def solve(size):
    from math import gcd
    def comb(n, k):
        if k < 0 or k > n:
            return 0
        k = min(k, n - k)
        res = 1
        for i in range(1, k + 1):
            res = res * (n - k + i) // i
        return res
    n2 = comb(4, 2) * comb(size - 4, 2)
    n3 = comb(4, 3) * comb(size - 4, 1)
    n4 = comb(4, 4) * comb(size - 4, 0)
    den = n2 + n3 + n4
    if den == 0:
        return 0
    g = gcd(n4, den)
    m = n4 // g
    n = den // g
    return m + n

solve(10)

# 调用 solve
result = solve(inputs['size'])
print(result)