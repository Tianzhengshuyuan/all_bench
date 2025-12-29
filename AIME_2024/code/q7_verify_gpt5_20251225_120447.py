inputs = {'N': 115}

from math import gcd

def solve(N):
    total_colorings = 2 ** 8
    g = gcd(N, total_colorings)
    m = N // g
    n = total_colorings // g
    return f"{m}/{n}"

solve(115)

# 调用 solve
result = solve(inputs['N'])
print(result)