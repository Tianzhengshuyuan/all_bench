inputs = {'surface_area': 54}

import math
from fractions import Fraction

def solve(surface_area):
    # Given: surface_area = 54, volume = 23
    # Let dimensions of box be a, b, c
    # Surface area: 2(ab + bc + ca) = 54  =>  ab + bc + ca = 27
    # Volume: abc = 23
    # We want the smallest sphere that can contain the box.
    # The sphere must have diameter at least the space diagonal of the box: sqrt(a^2 + b^2 + c^2)
    # So the radius r >= sqrt(a^2 + b^2 + c^2)/2
    # We want the minimal such r over all boxes in B.
    # But the sphere must contain the box, so the minimal radius is
    #   r_min = min over (a,b,c) of sqrt(a^2 + b^2 + c^2)/2
    # However, we are told that r is the radius of the smallest sphere that can contain *each* of the boxes.
    # That means: we need one sphere that can contain *every* box in B.
    # So r must be at least the maximum of sqrt(a^2 + b^2 + c^2)/2 over all boxes in B.
    # Hence: r = max_{(a,b,c) in B} sqrt(a^2 + b^2 + c^2)/2
    # So we want to maximize a^2 + b^2 + c^2 subject to:
    #   ab + bc + ca = 27
    #   abc = 23
    # Then r^2 = (a^2 + b^2 + c^2)/4

    # Let S1 = a + b + c
    # Then: a^2 + b^2 + c^2 = (a+b+c)^2 - 2(ab+bc+ca) = S1^2 - 2*27 = S1^2 - 54
    # So we want to maximize S1^2 - 54, i.e., maximize S1 = a+b+c

    # We have:
    #   ab + bc + ca = 27
    #   abc = 23
    # And we want to maximize a+b+c

    # By symmetry and analysis (Lagrange multipliers or known inequalities),
    # the maximum of a+b+c under fixed ab+bc+ca and abc occurs when two variables are equal.
    # So assume b = c.

    # Let b = c
    # Then:
    #   ab + bc + ca = ab + b^2 + ba = 2ab + b^2 = 27  =>  a = (27 - b^2)/(2b)
    #   abc = a * b * b = a b^2 = 23
    # Substitute a:
    #   [(27 - b^2)/(2b)] * b^2 = 23
    #   (27 - b^2) * b / 2 = 23
    #   (27 - b^2) b = 46
    #   27b - b^3 = 46
    #   b^3 - 27b + 46 = 0

    # Solve cubic: b^3 - 27b + 46 = 0
    # Try rational roots: factors of 46: ±1,2,23,46
    b = 2
    if abs(b**3 - 27*b + 46) < 1e-10:
        # b=2 is a root
        # Factor: (b - 2)(b^2 + 2b - 23) = 0
        # Other roots: b = [-2 ± sqrt(4 + 92)]/2 = [-2 ± sqrt(96)]/2 = [-2 ± 4*sqrt(6)]/2 = -1 ± 2*sqrt(6)
        # Take positive roots: b = 2, or b = -1 + 2*sqrt(6) ≈ 3.899
        roots = [2, -1 + 2*math.sqrt(6), -1 - 2*math.sqrt(6)]
        max_sum = 0
        for bval in roots:
            if bval <= 0:
                continue
            a = (27 - bval**2) / (2*bval)
            if a <= 0:
                continue
            c = bval
            # Check abc = 23
            if abs(a * bval * c - 23) > 1e-10:
                continue
            s = a + bval + c
            if s > max_sum:
                max_sum = s
        # Now compute a^2 + b^2 + c^2 = (a+b+c)^2 - 2(ab+bc+ca) = max_sum^2 - 54
        diag_sq = max_sum**2 - 54
        r_squared = diag_sq / 4
        # Return as fraction
        frac = Fraction(r_squared).limit_denominator()
        return frac.numerator + frac.denominator
    else:
        # Fallback: solve numerically
        from scipy.optimize import minimize_scalar
        def obj(b):
            if b <= 0:
                return -1e10
            a = (27 - b*b)/(2*b)
            if a <= 0:
                return -1e10
            if abs(a * b * b - 23) > 1e-6:
                return -1e10
            return -(a + b + b)  # negative because we maximize
        res = minimize_scalar(obj, bounds=(0.1, 10), method='bounded')
        bopt = res.x
        aopt = (27 - bopt**2)/(2*bopt)
        copt = bopt
        max_sum = aopt + bopt + copt
        diag_sq = max_sum**2 - 54
        r_squared = diag_sq / 4
        frac = Fraction(r_squared).limit_denominator()
        return frac.numerator + frac.denominator

# But we know b=2 is exact, so use exact arithmetic
def solve_exact(surface_area):
    # We found b=2 is a root
    b = 2
    a = (27 - b*b) / (2*b)
    c = b
    # Check
    assert abs(a*b*c - 23) < 1e-10
    assert abs(2*(a*b + b*c + c*a) - 54) < 1e-10
    max_sum = a + b + c
    diag_sq = max_sum**2 - 54
    r_squared = diag_sq / 4
    # Express as fraction
    # a = (27 - 4)/4 = 23/4
    a = Fraction(23, 4)
    b = Fraction(2, 1)
    c = Fraction(2, 1)
    max_sum = a + b + c
    diag_sq = max_sum**2 - 54
    r_squared = diag_sq / 4
    p, q = r_squared.numerator, r_squared.denominator
    return p + q

# Test
print(solve_exact(54))

# 调用 solve
result = solve(inputs['surface_area'])
print(result)