inputs = {'volume': 23}

from sympy import symbols, solve as sym_solve, nsimplify, Rational

def solve(volume):
    V = Rational(volume)
    b = symbols('b')
    equation = b**3 - 27*b + 2*V == 0
    roots = sym_solve(equation, b)
    real_pos_roots = [root for root in roots if root.is_real and root.evalf() > 1e-9]
    max_current = None
    for b_val in real_pos_roots:
        a = V / (b_val ** 2)
        current = a**2 + 2 * (b_val ** 2)
        current_val = current.evalf()
        if max_current is None or current_val > max_current.evalf():
            max_current = current
    r_squared = max_current / 4
    simplified = nsimplify(r_squared, rational=True)
    return simplified.numerator + simplified.denominator

# 调用 solve
result = solve(inputs['volume'])
print(result)