inputs = {'m': 115}

from math import gcd

def solve(m):
    total_colorings = 2**8  # each of 8 vertices independently red/blue
    n = total_colorings // gcd(m, total_colorings)  # reduced denominator
    return m + n

solve(115)

# 调用 solve
result = solve(inputs['m'])
print(result)