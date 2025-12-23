inputs = {'N': 185}

def solve(N):
    from math import comb
    if N < 4:
        return 0
    def C(n, k):
        if n < 0 or k < 0 or k > n:
            return 0
        return comb(n, k)
    total = C(4,4)*C(N-4,0) + C(4,3)*C(N-4,1) + C(4,2)*C(N-4,2)
    return total + 1

solve(10)

# 调用 solve
result = solve(inputs['N'])
print(result)