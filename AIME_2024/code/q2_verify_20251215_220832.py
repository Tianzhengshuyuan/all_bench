inputs = {'unit_length': 1}

def solve(unit_length):
    """
    Solve the problem of finding OC^2 where C is the unique point on AB
    that doesn't belong to any other unit segment from family F.
    
    The family F consists of segments PQ of given length lying in the first quadrant
    with P on the x-axis and Q on the y-axis.
    
    For the original problem, unit_length = 1, and AB is a segment from A(1/2, 0) to B(0, sqrt(3)/2).
    """
    from fractions import Fraction
    import math
    
    # The segment AB has length unit_length = 1
    # A = (1/2, 0), B = (0, sqrt(3)/2)
    # Line AB: y = -sqrt(3)*x + sqrt(3)/2
    
    # For a segment PQ with P=(a,0) and Q=(0,b) where a^2 + b^2 = unit_length^2
    # Line PQ: x/a + y/b = 1, or bx + ay = ab
    
    # Using the parametric approach with angle theta:
    # P = (L*cos(theta), 0), Q = (0, L*sin(theta)) where L = unit_length
    # For AB: cos(theta) = 1/2, sin(theta) = sqrt(3)/2, so theta = pi/3
    
    # Line equation for general segment: y = -tan(theta)*x + L*sin(theta)
    # Line AB: y = -sqrt(3)*x + L*sqrt(3)/2
    
    # Intersection of general line with AB:
    # -tan(phi)*x + L*sin(phi) = -sqrt(3)*x + L*sqrt(3)/2
    # x*(sqrt(3) - tan(phi)) = L*(sqrt(3)/2 - sin(phi))
    # x = L*(sqrt(3)/2 - sin(phi)) / (sqrt(3) - tan(phi))
    
    # As phi -> pi/3, both numerator and denominator -> 0
    # Using L'Hopital's rule:
    # d/dphi (sqrt(3)/2 - sin(phi)) = -cos(phi)
    # d/dphi (sqrt(3) - tan(phi)) = -sec^2(phi)
    # x = L * (-cos(phi)) / (-sec^2(phi)) = L * cos^3(phi)
    # At phi = pi/3: x = L * (1/2)^3 = L/8
    
    L = unit_length
    
    # x_C = L/8
    # y_C = -sqrt(3)*(L/8) + L*sqrt(3)/2 = L*sqrt(3)*(-1/8 + 1/2) = L*sqrt(3)*(3/8) = 3*L*sqrt(3)/8
    
    # OC^2 = (L/8)^2 + (3*L*sqrt(3)/8)^2
    #      = L^2/64 + 9*3*L^2/64
    #      = L^2/64 + 27*L^2/64
    #      = 28*L^2/64
    #      = 7*L^2/16
    
    # For L = 1: OC^2 = 7/16
    
    # Use exact symbolic computation
    # x_C^2 = L^2/64
    x_C_squared = Fraction(L * L, 64)
    # y_C^2 = (3*L*sqrt(3)/8)^2 = 9*L^2*3/64 = 27*L^2/64
    y_C_squared = Fraction(27 * L * L, 64)
    
    OC_squared = x_C_squared + y_C_squared
    # = L^2/64 + 27*L^2/64 = 28*L^2/64 = 7*L^2/16
    
    # Simplify the fraction
    p = OC_squared.numerator
    q = OC_squared.denominator
    
    # Make sure p and q are coprime
    gcd = math.gcd(p, q)
    p = p // gcd
    q = q // gcd
    
    return p + q


if __name__ == "__main__":
    result = solve(1)
    print(f"Answer: {result}")

# 调用 solve
result = solve(inputs['unit_length'])
print(result)