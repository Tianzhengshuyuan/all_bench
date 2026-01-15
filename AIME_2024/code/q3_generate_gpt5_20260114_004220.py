inputs = {'size': 163}

def solve(size):
    def nCk(n, k):
        if k < 0 or k > n:
            return 0
        k = min(k, n - k)
        res = 1
        for i in range(1, k + 1):
            res = res * (n - i + 1) // i
        return res

    def my_gcd(a, b):
        while b:
            a, b = b, a % b
        return a if a >= 0 else -a

    N = size
    k = 4
    numerator = nCk(k, k) * nCk(N - k, 0)
    denom = 0
    for i in range(2, k + 1):
        denom += nCk(k, i) * nCk(N - k, k - i)
    if denom == 0:
        return 0
    g = my_gcd(numerator, denom)
    m = numerator // g
    n = denom // g
    return m + n

solve(10)

# 调用 solve
result = solve(inputs['size'])
print(result)