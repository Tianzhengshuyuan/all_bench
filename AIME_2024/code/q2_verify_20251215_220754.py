inputs = {'unit_length': 1}

def solve(unit_length):
    """
    Solve the problem of finding OC^2 where C is the unique point on AB
    that doesn't belong to any other unit segment from family F.
    
    The family F consists of segments PQ of given length lying in the first quadrant
    with P on the x-axis and Q on the y-axis.
    
    For the original problem, unit_length = 1, and AB is a segment from A(1/2, 0) to B(0, sqrt(3)/2).
    """
    import math
    from fractions import Fraction
    
    # The segment AB has length unit_length
    # A is at (a_x, 0) and B is at (0, b_y) where a_x^2 + b_y^2 = unit_length^2
    # For the specific problem: A = (1/2, 0), B = (0, sqrt(3)/2)
    # We can verify: (1/2)^2 + (sqrt(3)/2)^2 = 1/4 + 3/4 = 1 = unit_length^2
    
    # The key insight is that for a segment PQ of length L with P=(a,0) and Q=(0,b),
    # we have a^2 + b^2 = L^2
    
    # For the original problem with unit_length = 1:
    # A = (1/2, 0), B = (0, sqrt(3)/2)
    # The angle theta for AB satisfies: cos(theta) = 1/2, sin(theta) = sqrt(3)/2, so theta = pi/3
    
    # For a general segment PQ with P=(cos(theta), 0) and Q=(0, sin(theta)) (when L=1),
    # the line equation is: x/cos(theta) + y/sin(theta) = 1
    # or: x*sin(theta) + y*cos(theta) = sin(theta)*cos(theta)
    
    # The line AB has equation: y = -sqrt(3)*x + sqrt(3)/2
    # In parametric form with angle theta: y = -tan(theta)*x + sin(theta)
    
    # For AB, theta = pi/3, so tan(theta) = sqrt(3), sin(theta) = sqrt(3)/2
    
    # The intersection of a general line (angle phi) with line AB:
    # y = -tan(phi)*x + sin(phi) and y = -sqrt(3)*x + sqrt(3)/2
    # Solving: x = (sin(phi) - sqrt(3)/2) / (tan(phi) - sqrt(3))
    
    # Using L'Hopital's rule as phi -> pi/3:
    # x = lim (cos(phi)) / (sec^2(phi)) = lim cos^3(phi) = (1/2)^3 = 1/8
    
    # This is for unit_length = 1. For general unit_length L:
    # A = (L/2, 0), B = (0, L*sqrt(3)/2)
    # The x-coordinate of C scales linearly with L: x_C = L/8
    # The y-coordinate: y = -sqrt(3)*x + L*sqrt(3)/2 = -sqrt(3)*(L/8) + L*sqrt(3)/2
    #                     = L*sqrt(3)*(-1/8 + 1/2) = L*sqrt(3)*(3/8) = 3*L*sqrt(3)/8
    
    # So C = (L/8, 3*L*sqrt(3)/8)
    # OC^2 = (L/8)^2 + (3*L*sqrt(3)/8)^2 = L^2/64 + 27*L^2/64 = 28*L^2/64 = 7*L^2/16
    
    # For unit_length = 1: OC^2 = 7/16, so p = 7, q = 16, p + q = 23
    
    L = unit_length
    
    # Calculate OC^2
    x_C = L / 8
    y_C = 3 * L * math.sqrt(3) / 8
    
    OC_squared = x_C**2 + y_C**2
    
    # OC^2 = L^2/64 + 27*L^2/64 = 28*L^2/64 = 7*L^2/16
    # For L = 1: OC^2 = 7/16
    
    # Convert to fraction
    # OC^2 = 7*L^2/16
    # For L = 1, this is 7/16
    
    # Use Fraction for exact arithmetic
    OC_squared_frac = Fraction(7, 16) * Fraction(L**2).limit_denominator(10000)
    
    # For the original problem with L=1:
    if L == 1:
        p = 7
        q = 16
    else:
        # General case
        OC_squared_frac = Fraction(7 * L * L, 16).limit_denominator(100000)
        p = OC_squared_frac.numerator
        q = OC_squared_frac.denominator
    
    return p + q


if __name__ == "__main__":
    result = solve(1)
    print(f"Answer: {result}")

# 调用 solve
result = solve(inputs['unit_length'])
print(result)