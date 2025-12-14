inputs = {'selected_number': 17}

from fractions import Fraction

def solve(selected_number):
    # Define the right-hand sides using the provided selected_number for the second equation
    r1 = Fraction(1, 2)
    r2 = Fraction(1, selected_number)
    r3 = Fraction(1, 4)
    
    # Let a = log2(x), b = log2(y), c = log2(z)
    # From the system:
    # a - b - c = r1
    # b - a - c = r2
    # c - a - b = r3
    # Adding pairs gives:
    a = -(r2 + r3) / 2
    b = -(r1 + r3) / 2
    c = -(r1 + r2) / 2
    
    # Compute |log2(x^4 y^3 z^2)| = |4a + 3b + 2c|
    val = abs(4*a + 3*b + 2*c)
    val = Fraction(val)  # ensure exact fraction
    
    # Return m + n for val = m/n in lowest terms
    return val.numerator + val.denominator

# 调用 solve
result = solve(inputs['selected_number'])
print(result)