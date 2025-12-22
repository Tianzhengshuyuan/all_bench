inputs = {'unit_length': 1}

import sympy as sp
from sympy import sqrt, Rational, symbols, solve as sp_solve, simplify

def solve(unit_length):
    """
    Find OC^2 where C is the unique point on AB that doesn't belong to any other
    unit segment from family F (except AB itself).
    
    The family F consists of segments PQ of given length with P on x-axis and Q on y-axis.
    """
    L = unit_length  # Length of segments in family F
    
    # Points O(0,0), A, B are defined such that AB has length L
    # A is at (L/2, 0) and B is at (0, sqrt(3)*L/2)
    # This makes |AB| = sqrt((L/2)^2 + (3*L^2/4)) = sqrt(L^2) = L
    
    A_x = Rational(1, 2) * L
    A_y = 0
    B_x = 0
    B_y = sqrt(3) * L / 2
    
    # Line AB: passes through A(L/2, 0) and B(0, sqrt(3)*L/2)
    # Slope = (sqrt(3)*L/2 - 0) / (0 - L/2) = -sqrt(3)
    # Equation: y = -sqrt(3)*x + sqrt(3)*L/2
    
    # For a general segment PQ in family F:
    # P = (a, 0) on x-axis, Q = (0, b) on y-axis
    # Constraint: a^2 + b^2 = L^2
    # Line PQ: x/a + y/b = 1, or bx + ay = ab
    
    # We need to find point C on AB such that the only segment from F passing through C is AB itself.
    
    x, a = symbols('x a', real=True, positive=True)
    
    # From constraint a^2 + b^2 = L^2, we get b = sqrt(L^2 - a^2)
    b = sqrt(L**2 - a**2)
    
    # Point on line AB: (x, -sqrt(3)*x + sqrt(3)*L/2)
    y_on_AB = -sqrt(3) * x + sqrt(3) * L / 2
    
    # This point must satisfy line PQ equation: bx + ay = ab
    # sqrt(L^2 - a^2) * x + a * (-sqrt(3)*x + sqrt(3)*L/2) = a * sqrt(L^2 - a^2)
    
    eq = b * x + a * y_on_AB - a * b
    eq = simplify(eq)
    
    # Rearrange: a*(-sqrt(3)*x + sqrt(3)*L/2) = (a - x) * sqrt(L^2 - a^2)
    # Square both sides to eliminate square root
    lhs = a * (-sqrt(3) * x + sqrt(3) * L / 2)
    rhs = (a - x) * sqrt(L**2 - a**2)
    
    # lhs^2 = rhs^2
    eq_squared = sp.expand(lhs**2 - rhs**2)
    eq_squared = simplify(eq_squared)
    
    # This gives a polynomial in a. We know a = L/2 is always a solution (corresponding to AB itself)
    # We need to factor out (a - L/2) and find x such that a = L/2 is the only solution
    
    # Convert to polynomial in a
    poly = sp.Poly(eq_squared, a)
    coeffs = poly.all_coeffs()
    
    # Divide by (a - L/2) to remove the trivial solution
    quotient, remainder = sp.div(sp.Poly(eq_squared, a), sp.Poly(a - L/2, a))
    
    # The quotient is a polynomial in a. For C to be unique, setting a = L/2 in the quotient
    # should give us the x-coordinate of C
    quotient_expr = quotient.as_expr()
    
    # Substitute a = L/2 into the quotient and solve for x
    eq_for_x = quotient_expr.subs(a, L/2)
    eq_for_x = simplify(eq_for_x)
    
    x_solutions = sp_solve(eq_for_x, x)
    
    # Filter out x = L/2 (which corresponds to point A)
    valid_x = None
    for sol in x_solutions:
        sol_simplified = simplify(sol)
        if sol_simplified != L/2 and sol_simplified > 0:
            valid_x = sol_simplified
            break
    
    if valid_x is None:
        # Try another approach - find x values
        for sol in x_solutions:
            sol_val = float(sol.subs(L, 1))
            if abs(sol_val - 0.5) > 0.01 and sol_val > 0:
                valid_x = sol
                break
    
    # Calculate y coordinate of C
    y_C = -sqrt(3) * valid_x + sqrt(3) * L / 2
    
    # Calculate OC^2
    OC_squared = valid_x**2 + y_C**2
    OC_squared = simplify(OC_squared)
    
    # For L = 1, get the numerical answer
    OC_squared_val = OC_squared.subs(L, 1)
    OC_squared_val = simplify(OC_squared_val)
    
    # Convert to fraction p/q
    OC_squared_rational = sp.nsimplify(OC_squared_val)
    
    p = OC_squared_rational.p
    q = OC_squared_rational.q
    
    return p + q

result = solve(1)

# 调用 solve
result = solve(inputs['unit_length'])
print(result)