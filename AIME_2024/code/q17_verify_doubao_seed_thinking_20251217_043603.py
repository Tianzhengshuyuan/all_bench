inputs = {'volume': 23}

from sympy import symbols, solve, Rational, nsimplify

def solve(volume):
    vol = Rational(volume)
    b = symbols('b')
    equation = b**3 - 27*b + 2*vol == 0
    roots = solve(equation, b)
    real_pos_roots = [root for root in roots if root.is_real and root > 0]
    
    max_D_sq_val = -1
    best_D_sq = None
    for root in real_pos_roots:
        a = vol / (root ** 2)
        D_sq = a**2 + 2 * (root ** 2)
        current_val = D_sq.evalf()
        if current_val > max_D_sq_val:
            max_D_sq_val = current_val
            best_D_sq = D_sq
    
    r_sq = best_D_sq / 4
    r_sq_simplified = nsimplify(r_sq)
    return r_sq_simplified.numerator + r_sq_simplified.denominator

# 调用 solve
result = solve(inputs['volume'])
print(result)