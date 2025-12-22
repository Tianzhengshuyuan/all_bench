inputs = {'volume': 23}

from scipy.optimize import minimize_scalar, brentq
import numpy as np

def solve(volume):
    # Given: surface area = 54, volume = V
    # For a rectangular box with dimensions a, b, c:
    # Surface area: 2(ab + bc + ca) = 54
    # Volume: abc = V
    # The smallest sphere containing the box has radius r = sqrt(a^2 + b^2 + c^2) / 2
    # We want to find the maximum of a^2 + b^2 + c^2 over all valid boxes
    
    S = 54  # surface area
    V = volume
    
    # We have: ab + bc + ca = 27, abc = V
    # Let's parameterize: fix a, then b and c satisfy:
    # b + c = (27 - bc) / a, and bc = V/a
    # So b + c = 27/a - V/(a^2), and bc = V/a
    # b and c are roots of: t^2 - (27/a - V/a^2)t + V/a = 0
    
    # For real positive b, c, we need:
    # 1. Discriminant >= 0
    # 2. b + c > 0
    # 3. bc > 0
    
    # a^2 + b^2 + c^2 = a^2 + (b+c)^2 - 2bc = a^2 + (27/a - V/a^2)^2 - 2V/a
    
    def sum_of_squares(a):
        if a <= 0:
            return None
        s = 27 / a - V / (a**2)  # b + c
        p = V / a  # bc
        if s <= 0 or p <= 0:
            return None
        disc = s**2 - 4*p
        if disc < 0:
            return None
        return a**2 + s**2 - 2*p
    
    # Find the range of valid a values
    # We need discriminant >= 0: (27/a - V/a^2)^2 >= 4V/a
    # Let u = 1/a, then (27u - Vu^2)^2 >= 4Vu
    # Also need 27/a - V/a^2 > 0, i.e., 27 > V/a, i.e., a > V/27
    
    # Find bounds for a
    a_min = V / 27 + 1e-10
    
    # Upper bound: when discriminant = 0 or when b,c become complex
    # Try to find upper bound numerically
    def discriminant(a):
        if a <= 0:
            return -1
        s = 27 / a - V / (a**2)
        p = V / a
        return s**2 - 4*p
    
    # Find where discriminant becomes 0
    # Start from a reasonable upper bound
    a_test = 10
    while discriminant(a_test) > 0 and a_test < 100:
        a_test += 1
    
    if discriminant(a_test) <= 0:
        # Find the root
        a_max = brentq(discriminant, a_min, a_test)
    else:
        a_max = a_test
    
    # Now maximize sum_of_squares over [a_min, a_max]
    # The maximum occurs at the boundary or at a critical point
    
    # Check if maximum is at boundary (when b = c, i.e., discriminant = 0)
    # At discriminant = 0: b = c, so 2b = 27/a - V/a^2, b^2 = V/a
    # So (27/a - V/a^2)^2 = 4V/a
    
    # Let's find a where b = c (discriminant = 0)
    def find_symmetric_a():
        # (27/a - V/a^2)^2 = 4V/a
        # Let x = 1/a
        # (27x - Vx^2)^2 = 4Vx
        # x(27 - Vx)^2 = 4V
        # This is a cubic in x
        from numpy.polynomial import polynomial as P
        # x(27 - Vx)^2 = 4V
        # x(729 - 54Vx + V^2 x^2) = 4V
        # V^2 x^3 - 54V x^2 + 729 x - 4V = 0
        coeffs = [-4*V, 729, -54*V, V**2]
        roots = np.roots([V**2, -54*V, 729, -4*V])
        real_positive = [r.real for r in roots if abs(r.imag) < 1e-10 and r.real > 0]
        return [1/x for x in real_positive if x > 0]
    
    symmetric_as = find_symmetric_a()
    
    max_sum_sq = 0
    for a in symmetric_as:
        if a > a_min:
            val = sum_of_squares(a)
            if val is not None and val > max_sum_sq:
                max_sum_sq = val
    
    # Also check interior maximum
    result = minimize_scalar(lambda a: -sum_of_squares(a) if sum_of_squares(a) is not None else 1e10,
                            bounds=(a_min + 0.001, a_max - 0.001 if a_max > a_min + 0.01 else a_min + 0.01),
                            method='bounded')
    
    interior_val = sum_of_squares(result.x)
    if interior_val is not None and interior_val > max_sum_sq:
        max_sum_sq = interior_val
    
    # r^2 = (a^2 + b^2 + c^2) / 4
    r_squared = max_sum_sq / 4
    
    # Express as p/q
    from fractions import Fraction
    frac = Fraction(r_squared).limit_denominator(10000)
    
    # Verify and refine
    # The answer should be exact. Let's solve symbolically.
    # At b = c: 2bc + ac + ab = 27 => 2b^2 + 2ab = 27
    # abc = V => ab^2 = V
    # From ab^2 = V: a = V/b^2
    # 2b^2 + 2(V/b^2)b = 27
    # 2b^2 + 2V/b = 27
    # 2b^3 + 2V = 27b
    # 2b^3 - 27b + 2V = 0
    
    coeffs_b = [2, 0, -27, 2*V]
    b_roots = np.roots(coeffs_b)
    
    for b in b_roots:
        if abs(b.imag) < 1e-10 and b.real > 0:
            b = b.real
            a = V / (b**2)
            c = b
            # Verify
            surf = 2*(a*b + b*c + c*a)
            vol = a*b*c
            if abs(surf - 54) < 0.01 and abs(vol - V) < 0.01:
                sum_sq = a**2 + b**2 + c**2
                r_sq = sum_sq / 4
                frac = Fraction(r_sq).limit_denominator(10000)
    
    p, q = frac.numerator, frac.denominator
    
    return p + q

result = solve(23)
print(result)

# 调用 solve
result = solve(inputs['volume'])
print(result)