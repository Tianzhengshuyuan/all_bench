inputs = {'unit_length': 1}

def solve(unit_length):
    """
    Solve the problem of finding OC^2 where C is the unique point on AB
    that doesn't belong to any other unit segment from family F.
    
    The family F consists of segments PQ of given length lying in the first quadrant
    with P on the x-axis and Q on the y-axis.
    """
    import sympy as sp
    from sympy import sqrt, Rational, gcd
    
    # Given points
    # O(0,0), A(1/2, 0), B(0, sqrt(3)/2)
    # Note: A and B are endpoints of a segment of length 1 (unit_length)
    # We need to scale based on unit_length
    
    # For the original problem with unit_length = 1:
    # A = (1/2, 0), B = (0, sqrt(3)/2)
    # |AB| = sqrt((1/2)^2 + (sqrt(3)/2)^2) = sqrt(1/4 + 3/4) = 1
    
    # For general unit_length L:
    # A = (L/2, 0), B = (0, L*sqrt(3)/2)
    
    L = unit_length
    
    # Line AB: passes through A(L/2, 0) and B(0, L*sqrt(3)/2)
    # Slope = (L*sqrt(3)/2 - 0) / (0 - L/2) = -sqrt(3)
    # Equation: y = -sqrt(3)*x + L*sqrt(3)/2
    
    # Family F: segments PQ of length L with P=(a,0) on x-axis, Q=(0,b) on y-axis
    # Constraint: a^2 + b^2 = L^2
    
    # Line PQ: x/a + y/b = 1, or bx + ay = ab
    
    # For segment AB: a = L/2, b = L*sqrt(3)/2
    # We parameterize: a = L*cos(theta), b = L*sin(theta) where theta in (0, pi/2)
    # For AB: theta = pi/3 (since cos(pi/3) = 1/2, sin(pi/3) = sqrt(3)/2)
    
    # Using the approach from Solution 2 with L'Hôpital's rule:
    # The intersection of line PQ (parameterized by theta) with line AB gives x-coordinate
    # 
    # Line PQ: y = -(tan(theta))*x + L*sin(theta)
    # Line AB: y = -sqrt(3)*x + L*sqrt(3)/2
    # 
    # Setting equal: -(tan(theta))*x + L*sin(theta) = -sqrt(3)*x + L*sqrt(3)/2
    # x*(sqrt(3) - tan(theta)) = L*sqrt(3)/2 - L*sin(theta)
    # x = L*(sqrt(3)/2 - sin(theta)) / (sqrt(3) - tan(theta))
    # x = L*(sqrt(3) - 2*sin(theta)) / (2*sqrt(3) - 2*tan(theta))
    
    # As theta -> pi/3, both numerator and denominator -> 0
    # Using L'Hôpital's rule:
    # d/dtheta [sqrt(3) - 2*sin(theta)] = -2*cos(theta)
    # d/dtheta [2*sqrt(3) - 2*tan(theta)] = -2*sec^2(theta)
    # 
    # Limit = L * (-2*cos(theta)) / (-2*sec^2(theta)) = L * cos^3(theta)
    # At theta = pi/3: cos(pi/3) = 1/2, so cos^3(pi/3) = 1/8
    # x = L/8
    
    x_C = sp.Rational(L, 8) if isinstance(L, int) else L / 8
    
    # For symbolic computation with L=1:
    x_C = sp.Rational(1, 8) * L
    
    # y_C from line AB: y = -sqrt(3)*x + L*sqrt(3)/2
    y_C = -sp.sqrt(3) * x_C + L * sp.sqrt(3) / 2
    y_C = sp.sqrt(3) * (-x_C + L/2)
    y_C = sp.sqrt(3) * (-sp.Rational(1,8)*L + sp.Rational(1,2)*L)
    y_C = sp.sqrt(3) * sp.Rational(3,8) * L
    
    # OC^2 = x_C^2 + y_C^2
    OC_squared = x_C**2 + y_C**2
    OC_squared = (sp.Rational(1,8)*L)**2 + (sp.sqrt(3)*sp.Rational(3,8)*L)**2
    OC_squared = sp.Rational(1,64)*L**2 + sp.Rational(27,64)*L**2
    OC_squared = sp.Rational(28,64)*L**2
    OC_squared = sp.Rational(7,16)*L**2
    
    # For L = unit_length = 1:
    if L == 1:
        OC_squared = sp.Rational(7, 16)
        p = 7
        q = 16
        return p + q
    else:
        # General case
        OC_squared = sp.Rational(7, 16) * L**2
        # Simplify and extract p, q
        OC_squared_simplified = sp.simplify(OC_squared)
        if OC_squared_simplified.is_Rational:
            p = OC_squared_simplified.p
            q = OC_squared_simplified.q
            return p + q
        else:
            # For non-unit length, return the expression
            return OC_squared_simplified

# Test with unit_length = 1
print(solve(1))

# 调用 solve
result = solve(inputs['unit_length'])
print(result)