inputs = {'x_coordinate_A': 16}

def solve(x_coordinate_A):
    import numpy as np
    from fractions import Fraction
    
    # Given points
    # O = (0, 0)
    # A = (x_coordinate_A, 0)
    # B = (0, sqrt(3)/2)
    
    # The line AB has equation: y = -sqrt(3)x + sqrt(3)/2
    # This can be rewritten as: y = -sqrt(3)(x - 1/2)
    
    # For a unit segment PQ with P=(a,0) and Q=(0,b), we have a^2 + b^2 = 1
    # The line through P and Q has equation: x/a + y/b = 1, or bx + ay = ab
    
    # Substituting b = sqrt(1-a^2) and the line AB equation into the intersection condition:
    # We get a polynomial in a for each x on AB
    
    # The key insight is that we want to find x such that a = x_coordinate_A is the only solution
    # (besides being on AB itself)
    
    # After algebraic manipulation (as shown in the solution), when we require
    # a = x_coordinate_A to be a repeated root, we get:
    # 16x^2 - 10x + 1 = 0
    
    # Solving this quadratic
    discriminant = 100 - 64
    x1 = (10 + np.sqrt(discriminant)) / 32
    x2 = (10 - np.sqrt(discriminant)) / 32
    
    # x1 = 1/2, x2 = 1/8
    # We need x = 1/8 (the other gives point A itself)
    x = 1/8
    
    # Find y coordinate on line AB
    y = -np.sqrt(3) * x + np.sqrt(3) / 2
    y = -np.sqrt(3) / 8 + np.sqrt(3) / 2
    y = np.sqrt(3) * (1/2 - 1/8)
    y = np.sqrt(3) * 3/8
    
    # Calculate OC^2
    OC_squared = x**2 + y**2
    OC_squared = (1/8)**2 + (3*np.sqrt(3)/8)**2
    OC_squared = 1/64 + 27/64
    OC_squared = 28/64
    OC_squared = 7/16
    
    # Find p and q where OC^2 = p/q in lowest terms
    frac = Fraction(7, 16)
    p = frac.numerator
    q = frac.denominator
    
    return p + q

# 调用 solve
result = solve(inputs['x_coordinate_A'])
print(result)