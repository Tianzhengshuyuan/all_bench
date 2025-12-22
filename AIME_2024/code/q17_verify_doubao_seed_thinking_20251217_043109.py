inputs = {'volume': 23}

from sympy import symbols, solve as sym_solve, Rational, nsimplify

def solve(volume):
    volume = Rational(volume)
    b = symbols('b')
    equation = b**3 - 27*b + 2*volume == 0
    roots = sym_solve(equation, b)
    real_pos_roots = [root for root in roots if root.is_real and root > 0]
    b_min = min(real_pos_roots)
    a = volume / (b_min ** 2)
    D_sq = a**2 + 2 * (b_min ** 2)
    r_sq = D_sq / 4
    r_sq_simplified = nsimplify(r_sq)
    p = r_sq_simplified.numerator
    q = r_sq_simplified.denominator
    return p + q

# 调用 solve
result = solve(inputs['volume'])
print(result)