inputs = {'vertical_sum': 117}

def solve(vertical_sum):
    from math import comb

    V = vertical_sum
    if (V - 27) % 9 != 0:
        return 0
    S = (V - 27) // 9
    if S < 0 or S > 27:
        return 0

    def nCk(n, k):
        if n < 0 or k < 0 or k > n:
            return 0
        return comb(n, k)

    total = 0
    for j in range(4):
        total += ((-1) ** j) * nCk(3, j) * nCk(S - 10 * j + 2, 2)
    return total

solve(99)

# 调用 solve
result = solve(inputs['vertical_sum'])
print(result)