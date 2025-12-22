inputs = {'white_chip_count': 25}

import math

def solve(white_chip_count):
    n = math.isqrt(white_chip_count)
    return ( (2 ** n - 2) ** 2 ) + 2

# 调用 solve
result = solve(inputs['white_chip_count'])
print(result)