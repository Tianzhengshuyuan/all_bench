inputs = {'volume': 23}

from sympy import symbols, solve, Rational

def solve(volume):
    V = Rational(volume)
    b = symbols('b')
    equation = b**3 - 27*b + 2*V == 0
    roots = solve(equation, b)
    real_pos_roots = [root for root in roots if root.is_real and root.evalf() > 1e-9]
    b_min = min(real_pos_roots, key=lambda x: x.evalf())
    a = V / (b_min ** 2)
    r_squared = (a**2 + 2 * b_min**2) / 4
    simplified = r_squared.simplify()
    return simplified.numerator + simplified.denominator

# 调用 solve
result = solve(inputs['volume'])
print(result)