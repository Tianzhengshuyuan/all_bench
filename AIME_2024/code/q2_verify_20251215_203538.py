inputs = {'b_y_radical_number': 3}

import math

def solve(b_y_radical_number):
    numerator = 1 + 9 * b_y_radical_number
    denominator = 64
    common_divisor = math.gcd(numerator, denominator)
    p = numerator // common_divisor
    q = denominator // common_divisor
    return p + q

# 调用 solve
result = solve(inputs['b_y_radical_number'])
print(result)