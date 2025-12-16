inputs = {'x_coordinate_A': 0.5}

import numpy as np
from scipy.optimize import fsolve

def solve(x_coordinate_A):
    # Point coordinates
    O = np.array([0, 0])
    A = np.array([x_coordinate_A, 0])
    B = np.array([0, np.sqrt(3) * x_coordinate_A])
    
    # Line AB equation: y = mx + b
    # From A to B: slope m = (sqrt(3)*x_coordinate_A - 0)/(0 - x_coordinate_A) = -sqrt(3)
    # Using point A: 0 = -sqrt(3)*x_coordinate_A + b, so b = sqrt(3)*x_coordinate_A
    m_AB = -np.sqrt(3)
    b_AB = np.sqrt(3) * x_coordinate_A
    
    # For a segment PQ with P=(a,0) and Q=(0,b) where a^2 + b^2 = 1
    # The line through PQ has equation: x/a + y/b = 1, or ay + bx = ab
    
    # Find point C on AB such that it only belongs to segment AB
    # This happens when the only solution for a segment through C is a = x_coordinate_A
    
    # For a point (x, y) on AB where y = -sqrt(3)*x + sqrt(3)*x_coordinate_A
    # and a segment with P=(a,0), Q=(0,sqrt(1-a^2)) passing through it:
    # a*y + x*sqrt(1-a^2) = a*sqrt(1-a^2)
    
    # Substituting y = -sqrt(3)*x + sqrt(3)*x_coordinate_A:
    # a*(-sqrt(3)*x + sqrt(3)*x_coordinate_A) + x*sqrt(1-a^2) = a*sqrt(1-a^2)
    # -a*sqrt(3)*x + a*sqrt(3)*x_coordinate_A + x*sqrt(1-a^2) = a*sqrt(1-a^2)
    # a*sqrt(3)*x_coordinate_A = a*sqrt(1-a^2) + a*sqrt(3)*x - x*sqrt(1-a^2)
    # a*sqrt(3)*x_coordinate_A = (a-x)*sqrt(1-a^2) + a*sqrt(3)*x
    
    # After squaring and simplifying, we get a polynomial in a
    # We want x such that a = x_coordinate_A is a double root
    
    def find_critical_x(x):
        # For the polynomial in a after substitution
        # We want the derivative with respect to a at a = x_coordinate_A to be 0
        a = x_coordinate_A
        
        # The condition is that when we substitute back a = x_coordinate_A
        # into the factored polynomial (after removing the factor (a - x_coordinate_A))
        # we get 0
        
        # After factoring out (2a - 1) from the quartic polynomial:
        # -a^3 + (2x - x_coordinate_A)*a^2 + (-4x^2 + 4*x_coordinate_A*x)*a - 2*x_coordinate_A*x^2 = 0
        
        # Substituting a = x_coordinate_A:
        result = (-x_coordinate_A**3 + 
                 (2*x - x_coordinate_A)*x_coordinate_A**2 + 
                 (-4*x**2 + 4*x_coordinate_A*x)*x_coordinate_A - 
                 2*x_coordinate_A*x**2)
        
        return result
    
    # Solve for x
    # When x_coordinate_A = 1/2, we get 16x^2 - 10x + 1 = 0
    # Solutions are x = 1/8 and x = 1/2
    # We need x = 1/8 (the other is point A itself)
    
    # For general x_coordinate_A:
    # The equation becomes: 16*x_coordinate_A^2 * x^2 - 10*x_coordinate_A * x + 1 = 0
    # Using quadratic formula:
    a_coef = 16 * x_coordinate_A**2
    b_coef = -10 * x_coordinate_A
    c_coef = 1
    
    discriminant = b_coef**2 - 4*a_coef*c_coef
    x1 = (-b_coef - np.sqrt(discriminant)) / (2*a_coef)
    x2 = (-b_coef + np.sqrt(discriminant)) / (2*a_coef)
    
    # Choose the smaller x value (not x_coordinate_A itself)
    x_C = x1 if abs(x1 - x_coordinate_A) > 1e-10 else x2
    if abs(x_C - x_coordinate_A) < 1e-10:
        x_C = x1 if x1 != x_C else x2
    
    # Find y coordinate of C
    y_C = m_AB * x_C + b_AB
    
    # Calculate OC^2
    OC_squared = x_C**2 + y_C**2
    
    # Convert to fraction p/q
    from fractions import Fraction
    frac = Fraction(OC_squared).limit_denominator(1000)
    
    return frac.numerator + frac.denominator

# 调用 solve
result = solve(inputs['x_coordinate_A'])
print(result)