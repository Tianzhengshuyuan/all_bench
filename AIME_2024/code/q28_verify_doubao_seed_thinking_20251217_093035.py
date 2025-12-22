inputs = {'ac_bd_squared_length': 80}

import sympy as sp

def solve(ac_bd_squared_length):
    S = ac_bd_squared_length
    num_numerator = (S**2 - 48**2) * (130 - S)
    num_denominator = 8 * (-S**2 + 260 * S - 2304)
    f = sp.Rational(num_numerator, num_denominator)
    sqrt_f = sp.sqrt(f)
    rational_part = sqrt_f.args[0]
    sqrt_part = sqrt_f.args[1]
    n = sqrt_part.args[0]
    m = rational_part.numerator
    p = rational_part.denominator
    return m + n + p

# 调用 solve
result = solve(inputs['ac_bd_squared_length'])
print(result)