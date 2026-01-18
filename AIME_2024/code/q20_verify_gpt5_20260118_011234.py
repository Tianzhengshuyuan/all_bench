inputs = {'white_count': 25}

from math import isqrt

def solve(white_count):
    n = isqrt(white_count)
    return (2**n - 2)**2 + 2

white_count = 25
solve(white_count)

# 调用 solve
result = solve(inputs['white_count'])
print(result)