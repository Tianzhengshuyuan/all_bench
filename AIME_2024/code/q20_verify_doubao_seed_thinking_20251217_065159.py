inputs = {'white_chip_count': 25}

import math

def solve(white_chip_count):
    n = int(math.isqrt(white_chip_count))
    return 4 ** n

# 调用 solve
result = solve(inputs['white_chip_count'])
print(result)