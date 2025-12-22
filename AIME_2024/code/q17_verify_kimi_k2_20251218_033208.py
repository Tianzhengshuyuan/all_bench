inputs = {'surface_area': 54}

import math
from fractions import Fraction

def solve(surface_area):
    # Given surface_area = 54 and volume = 23
    # Let the dimensions of the box be a, b, c
    # Surface area: 2(ab + bc + ca) = 54  =>  ab + bc + ca = 27
    # Volume: abc = 23
    # The smallest sphere that can contain the box has diameter equal to the space diagonal of the box
    # Space diagonal d = sqrt(a^2 + b^2 + c^2)
    # So r = d / 2, and r^2 = d^2 / 4 = (a^2 + b^2 + c^2) / 4
    
    # We need to minimize r, which is equivalent to minimizing a^2 + b^2 + c^2
    # But actually, we want the smallest sphere that can contain *any* such box,
    # so we want the maximum possible space diagonal among all boxes with given surface area and volume.
    # However, the problem asks for the smallest sphere that can contain *each* box in B.
    # That means we need the supremum of the space diagonals over all such boxes.
    # But since the set is closed and bounded, the maximum is attained.
    
    # We want to maximize a^2 + b^2 + c^2 subject to:
    #   ab + bc + ca = 27
    #   abc = 23
    #   a,b,c > 0
    
    # Note: a^2 + b^2 + c^2 = (a+b+c)^2 - 2(ab+bc+ca) = (a+b+c)^2 - 54
    # So maximizing a^2 + b^2 + c^2 is equivalent to maximizing a+b+c
    
    # Let s = a+b+c, p = ab+bc+ca = 27, q = abc = 23
    # a,b,c are roots of x^3 - s x^2 + p x - q = 0
    # For real positive roots, discriminant conditions must hold, but we can use calculus.
    
    # Alternatively, use symmetry: the maximum of a+b+c (and hence of a^2+b^2+c^2)
    # under fixed ab+bc+ca and abc often occurs when two variables are equal.
    
    # Assume b = c. Then:
    #   ab + bc + ca = a b + b^2 + b a = 2ab + b^2 = 27
    #   abc = a b^2 = 23
    # From second: a = 23 / b^2
    # Plug into first: 2*(23/b^2)*b + b^2 = 46/b + b^2 = 27
    # => b^3 - 27 b + 46 = 0
    # We solve this cubic.
    
    # Try rational roots: factors of 46: ±1,2,23,46
    # b=2: 8 - 54 + 46 = 0 -> yes!
    # So (b-2) is a factor.
    # Divide: b^3 - 27b + 46 = (b-2)(b^2 + 2b - 23) = 0
    # So b = 2 or b = [-2 ± sqrt(4 + 92)]/2 = [-2 ± sqrt(96)]/2 = [-2 ± 4√6]/2 = -1 ± 2√6
    # Positive root: b = -1 + 2√6 ≈ -1 + 4.9 = 3.9 > 0
    # So two positive solutions: b = 2 and b = -1 + 2√6
    
    # Case 1: b = 2
    #   a = 23 / b^2 = 23 / 4
    #   c = b = 2
    #   Check: ab+bc+ca = (23/4)*2 + 2*2 + 2*(23/4) = 23/2 + 4 + 23/2 = 23 + 4 = 27 -> good
    #   a^2+b^2+c^2 = (23/4)^2 + 4 + 4 = 529/16 + 8 = 529/16 + 128/16 = 657/16
    
    # Case 2: b = -1 + 2√6
    #   b^2 = (-1 + 2√6)^2 = 1 - 4√6 + 24 = 25 - 4√6
    #   a = 23 / b^2 = 23 / (25 - 4√6)
    #   Rationalize: multiply numerator and denominator by 25 + 4√6
    #   denominator = 25^2 - (4√6)^2 = 625 - 16*6 = 625 - 96 = 529
    #   so a = 23*(25 + 4√6)/529 = (23/529)*(25 + 4√6) = (1/23)*(25 + 4√6)
    #   Now compute a^2 + b^2 + c^2 = a^2 + 2b^2
    #   We already have 2b^2 = 2*(25 - 4√6) = 50 - 8√6
    #   a^2 = (1/23^2)*(25 + 4√6)^2 = (1/529)*(625 + 200√6 + 16*6) = (1/529)*(625 + 96 + 200√6) = (721 + 200√6)/529
    #   So total: a^2+b^2+c^2 = (721 + 200√6)/529 + 50 - 8√6
    #             = (721 + 200√6)/529 + (50*529 - 8√6*529)/529
    #             = [721 + 200√6 + 26450 - 4232√6] / 529
    #             = (27171 - 4032√6) / 529
    #   Now √6 ≈ 2.45, so 4032*2.45 ≈ 9878, so this is about (27171 - 9878)/529 ≈ 17293/529 ≈ 32.7
    #   Compare to case 1: 657/16 = 41.0625
    #   So case 1 gives larger a^2+b^2+c^2
    
    # But is this the maximum? We want the maximum possible space diagonal.
    # Case 1 gives larger sum of squares.
    
    # Check if other cases (all distinct) could give larger? Probably not, since symmetry often gives extrema.
    # So we take the maximum of a^2+b^2+c^2 as 657/16
    
    max_diag_sq = Fraction(657, 16)
    r_squared = max_diag_sq / 4   # because r = sqrt(diag_sq)/2  =>  r^2 = diag_sq / 4
    r_squared = r_squared / 4     # wait: r^2 = (a^2+b^2+c^2)/4  -> yes, already have diag_sq = a^2+b^2+c^2
    r_squared = Fraction(657, 16) / 4   # no: r^2 = (a^2+b^2+c^2)/4 = (657/16) / 4 ? 
    # No: r^2 = (a^2+b^2+c^2) / 4 = (657/16) * 1/4 = 657 / 64
    r_squared = Fraction(657, 64)
    
    # Reduce: 657 and 64
    # 657 ÷ 3 = 219, 219 ÷ 3 = 73 -> 657 = 9*73
    # 64 = 2^6
    # no common factors
    p, q = 657, 64
    return p + q

print(solve(54))

# 调用 solve
result = solve(inputs['surface_area'])
print(result)