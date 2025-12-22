inputs = {'volume': 23}

from sympy import symbols, Poly, solve as sym_solve, Rational, nsimplify

def solve(volume):
    volume = Rational(volume)
    b = symbols('b')
    poly = Poly(b**3 - 27*b + 2*volume, b)
    # Find rational roots using Rational Root Theorem
    rational_roots = poly.rational_roots()
    # Select positive rational root (exists for given volume=23)
    positive_rational_roots = [r for r in rational_roots if r > 0]
    b_min = min(positive_rational_roots) if positive_rational_roots else None
    
    if not b_min:
        # Fallback to find real positive roots if no rational root found
        roots = sym_solve(poly, b)
        real_pos_roots = [root for root in roots if root.is_real and root.evalf() > 1e-9]
        b_min = min(real_pos_roots, key=lambda x: x.evalf())
    
    a = volume / (b_min ** 2)
    D_sq = a**2 + 2 * (b_min ** 2)
    r_sq = D_sq / 4
    r_sq_simplified = nsimplify(r_sq)
    return r_sq_simplified.numerator + r_sq_simplified.denominator

# 调用 solve
result = solve(inputs['volume'])
print(result)