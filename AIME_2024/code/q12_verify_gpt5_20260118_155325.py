inputs = {'sum_vertical': 99}

def solve(sum_vertical):
    from math import comb

    rem = sum_vertical - 27
    if rem % 9 != 0:
        return 0
    S = rem // 9
    if S < 0 or S > 27:
        return 0

    def C(n, k):
        if n < 0 or k < 0 or k > n:
            return 0
        return comb(n, k)

    total = 0
    for j in range(4):
        term = C(3, j) * C(S - 10 * j + 2, 2)
        total += term if j % 2 == 0 else -term
    return total

# 调用 solve
result = solve(inputs['sum_vertical'])
print(result)