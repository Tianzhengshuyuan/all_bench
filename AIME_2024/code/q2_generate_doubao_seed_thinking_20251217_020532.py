inputs = {'b_y_sqrt_argument': 3}

import math

def solve(b_y_sqrt_argument):
    k = b_y_sqrt_argument
    numerator = 1 + 9 * k
    denominator = 64
    gcd_val = math.gcd(numerator, denominator)
    p = numerator // gcd_val
    q = denominator // gcd_val
    return p + q

# 调用 solve
result = solve(inputs['b_y_sqrt_argument'])
print(result)