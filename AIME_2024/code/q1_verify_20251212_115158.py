inputs = {'denominator': 3}

from fractions import Fraction

def solve(denominator):
    # Define the right-hand sides
    r1 = Fraction(1, 2)
    r2 = Fraction(1, denominator)
    r3 = Fraction(1, 4)
    
    # Let a = log2(x), b = log2(y), c = log2(z)
    # From adding pairs of equations:
    # (1)+(3): -2b = r1 + r3  => b = -(r1 + r3)/2
    # (2)+(3): -2a = r2 + r3  => a = -(r2 + r3)/2
    # (1)+(2): -2c = r1 + r2  => c = -(r1 + r2)/2
    a = - (r2 + r3) / 2
    b = - (r1 + r3) / 2
    c = - (r1 + r2) / 2
    
    # Compute |log2(x^4 y^3 z^2)| = |4a + 3b + 2c|
    val = abs(4*a + 3*b + 2*c)
    
    # Return m + n where val = m/n in lowest terms
    return val.numerator + val.denominator

# 调用 solve
result = solve(inputs['denominator'])
print(result)