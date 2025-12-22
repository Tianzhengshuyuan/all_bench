inputs = {'volume': 23}

from sympy import symbols, solve as sym_solve, Rational, nsimplify

def solve(volume):
    V = Rational(volume)
    b = symbols('b')
    equation = b**3 - 27*b + 2*V == 0
    roots = sym_solve(equation, b)
    real_pos_roots = []
    for root in roots:
        if root.is_real:
            val = root.evalf()
            if val > 1e-9:
                real_pos_roots.append(root)
    b_min = min(real_pos_roots, key=lambda x: x.evalf())
    a = V / (b_min ** 2)
    r_squared = (a**2 + 2 * b_min**2) / 4
    simplified = nsimplify(r_squared)
    return simplified.numerator + simplified.denominator

# 调用 solve
result = solve(inputs['volume'])
print(result)