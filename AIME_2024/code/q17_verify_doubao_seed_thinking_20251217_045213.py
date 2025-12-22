inputs = {'volume': 23}

from sympy import symbols, Poly, solve, Rational, nsimplify
from sympy.polys.rationaltools import rational_roots

def solve(volume):
    V = Rational(volume)
    b = symbols('b')
    poly = Poly(b**3 - 27*b + 2*V, b)
    
    # Find rational roots using Rational Root Theorem
    possible_roots = rational_roots(poly)
    rational_root = None
    for r in possible_roots:
        if poly.eval(r) == 0:
            rational_root = r
            break
    
    # Factor polynomial and find all roots
    if rational_root is not None:
        quo, _ = poly.div(b - rational_root)
        quad_roots = solve(quo, b)
        all_roots = [rational_root] + quad_roots
    else:
        all_roots = solve(poly, b)
    
    # Filter real positive roots
    real_pos_roots = []
    for root in all_roots:
        if root.is_real:
            val = root.evalf()
            if val > 1e-9:
                real_pos_roots.append(root)
    
    # Find maximum current value (a² + 2b²)
    max_current = None
    for b_root in real_pos_roots:
        a = V / (b_root ** 2)
        current = a**2 + 2 * (b_root ** 2)
        current_val = current.evalf()
        if max_current is None or current_val > max_current.evalf():
            max_current = current
    
    # Calculate r² and simplify
    r_squared = max_current / 4
    simplified = nsimplify(r_squared)
    return simplified.numerator + simplified.denominator

# 调用 solve
result = solve(inputs['volume'])
print(result)