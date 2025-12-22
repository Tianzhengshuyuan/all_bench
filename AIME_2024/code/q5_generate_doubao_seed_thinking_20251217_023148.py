inputs = {'small_circle_count': 2}

import math

def solve(small_circle_count):
    numerator = 34 * (small_circle_count - 8)
    denominator = small_circle_count - 239
    gcd_val = math.gcd(numerator, denominator)
    m = numerator // gcd_val
    n = denominator // gcd_val
    return m + n

# 调用 solve
result = solve(inputs['small_circle_count'])
print(result)