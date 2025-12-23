inputs = {'modulus': 7}

def solve(modulus):
    if not isinstance(modulus, int) or modulus <= 0:
        return None
    for N in range(9999, 999, -1):
        a = N // 1000
        b = (N // 100) % 10
        c = (N // 10) % 10
        d = N % 10
        nums = [
            1000 + 100 * b + 10 * c + d,          # replace thousands with 1
            1000 * a + 100 + 10 * c + d,          # replace hundreds with 1
            1000 * a + 100 * b + 10 + d,          # replace tens with 1
            1000 * a + 100 * b + 10 * c + 1       # replace units with 1
        ]
        if all(x % modulus == 0 for x in nums):
            Q = N // 1000
            R = N % 1000
            return Q + R
    return None

result = solve(7)

# 调用 solve
result = solve(inputs['modulus'])
print(result)