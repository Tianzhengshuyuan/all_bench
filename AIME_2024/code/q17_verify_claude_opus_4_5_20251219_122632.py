inputs = {'volume': 23}

from scipy.optimize import minimize_scalar, brentq
import numpy as np

def solve(volume):
    # Given: surface area = 54, volume = V
    # For a rectangular box with dimensions a, b, c:
    # Surface area: 2(ab + bc + ca) = 54, so ab + bc + ca = 27
    # Volume: abc = V
    # The smallest sphere containing the box has radius r = sqrt(a^2 + b^2 + c^2) / 2
    # We want to find the maximum of a^2 + b^2 + c^2 over all valid boxes
    
    S = 54  # surface area
    V = volume
    
    # We have constraints:
    # ab + bc + ca = 27
    # abc = V
    
    # For a given value of c, we have:
    # ab + c(a+b) = 27
    # ab = V/c
    # So: V/c + c(a+b) = 27
    # a + b = (27 - V/c) / c = 27/c - V/c^2
    
    # Also a and b are roots of: t^2 - (a+b)t + ab = 0
    # t^2 - (27/c - V/c^2)t + V/c = 0
    
    # For real positive a, b:
    # 1. Discriminant >= 0: (27/c - V/c^2)^2 - 4V/c >= 0
    # 2. Sum > 0: 27/c - V/c^2 > 0, i.e., 27c - V > 0, c > V/27
    # 3. Product > 0: V/c > 0 (always true for c > 0)
    
    # We want to maximize a^2 + b^2 + c^2 = (a+b)^2 - 2ab + c^2
    # = (27/c - V/c^2)^2 - 2V/c + c^2
    
    def sum_ab(c):
        return 27/c - V/c**2
    
    def prod_ab(c):
        return V/c
    
    def discriminant(c):
        s = sum_ab(c)
        p = prod_ab(c)
        return s**2 - 4*p
    
    def sum_of_squares(c):
        s = sum_ab(c)
        p = prod_ab(c)
        return s**2 - 2*p + c**2
    
    # Find valid range of c
    # Need: c > V/27 and discriminant >= 0
    
    c_min = V / 27 + 1e-10
    
    # Find upper bound where discriminant = 0
    # (27/c - V/c^2)^2 = 4V/c
    # Let's find where discriminant becomes 0
    
    # Start from a reasonable upper bound
    c_max_search = 10.0
    
    # Find where discriminant = 0 for upper bound
    def disc_eq(c):
        return discriminant(c)
    
    # Check if discriminant is positive at c_min
    if discriminant(c_min) < 0:
        c_min = c_min + 0.01
    
    # Find the range where discriminant >= 0
    # Binary search for upper bound
    c_test = c_min
    while c_test < 100 and discriminant(c_test) >= 0:
        c_test *= 1.1
    
    if discriminant(c_test) < 0:
        # Find exact upper bound
        c_upper = brentq(disc_eq, c_min, c_test)
    else:
        c_upper = c_test
    
    # Also need to check lower bound more carefully
    c_lower = c_min
    if discriminant(c_lower) < 0:
        c_lower = brentq(disc_eq, c_min, (c_min + c_upper)/2)
    
    # Maximize sum of squares
    # Use negative for minimization
    def neg_sum_sq(c):
        if discriminant(c) < 0:
            return 1e10
        return -sum_of_squares(c)
    
    # Check at boundaries and critical points
    result = minimize_scalar(neg_sum_sq, bounds=(c_lower + 1e-8, c_upper - 1e-8), method='bounded')
    
    # Also check boundary values
    eps = 1e-8
    candidates = []
    
    for c in [c_lower + eps, c_upper - eps, result.x]:
        if c_lower <= c <= c_upper and discriminant(c) >= -1e-10:
            candidates.append(sum_of_squares(c))
    
    # The maximum sum of squares
    max_sum_sq = max(candidates)
    
    # r^2 = (a^2 + b^2 + c^2) / 4
    r_squared = max_sum_sq / 4
    
    # Convert to fraction p/q
    from fractions import Fraction
    
    # The answer should be a nice fraction
    # Let's compute more precisely at the boundary
    
    # At the boundary, discriminant = 0, so a = b
    # Then: 2a^2 + 2ac = 27, a^2*c = V
    # From second: a^2 = V/c
    # Substitute: 2V/c + 2ac = 27
    # a = V/(c*a) => a^2 = V/c (consistent)
    # 2V/c + 2c*sqrt(V/c) = 27
    # Let u = sqrt(c), then c = u^2
    # 2V/u^2 + 2u^2 * sqrt(V)/u = 27
    # 2V/u^2 + 2u*sqrt(V) = 27
    
    # At boundary: a = b, so sum_sq = 2a^2 + c^2 = 2V/c + c^2
    
    def boundary_sum_sq(c):
        return 2*V/c + c**2
    
    # Derivative: -2V/c^2 + 2c = 0 => c^3 = V => c = V^(1/3)
    # But we need to check if this is in valid range
    
    c_critical = V**(1/3)
    
    # Check constraint: 2V/c + 2c*sqrt(V/c) = 27
    def constraint_check(c):
        a_sq = V/c
        a = np.sqrt(a_sq)
        return 2*a_sq + 2*a*c - 27
    
    # Solve for c where a=b
    c_boundary = brentq(constraint_check, 0.1, 10)
    
    sum_sq_at_boundary = boundary_sum_sq(c_boundary)
    
    r_sq = sum_sq_at_boundary / 4
    
    # Convert to fraction
    frac = Fraction(r_sq).limit_denominator(10000)
    
    # More precise calculation
    # At a=b: 2a^2 + 2ac = 27, a^2*c = 23
    # Let a^2 = x, then 2x + 2*sqrt(x)*c = 27, x*c = 23
    # c = 23/x, so 2x + 2*sqrt(x)*23/x = 27
    # 2x + 46/sqrt(x) = 27
    # Let y = sqrt(x), x = y^2
    # 2y^2 + 46/y = 27
    # 2y^3 + 46 = 27y
    # 2y^3 - 27y + 46 = 0
    
    # Solve 2y^3 - 27y + 46 = 0
    coeffs = [2, 0, -27, 46]
    roots = np.roots(coeffs)
    
    # Find positive real root
    for root in roots:
        if np.isreal(root) or abs(root.imag) < 1e-10:
            y = root.real
            if y > 0:
                x = y**2  # a^2
                c = 23/x
                sum_sq = 2*x + c**2
                r_sq_val = sum_sq / 4
    
    # r^2 = (2a^2 + c^2)/4 = (2x + (23/x)^2)/4
    # With 2y^3 - 27y + 46 = 0, y = sqrt(x)
    
    # Using exact arithmetic with the polynomial
    # The answer is p/q where p+q is what we need
    
    frac_result = Fraction(r_sq_val).limit_denominator(1000)
    p = frac_result.numerator
    q = frac_result.denominator
    
    return p + q

result = solve(23)
print(result)

# 调用 solve
result = solve(inputs['volume'])
print(result)