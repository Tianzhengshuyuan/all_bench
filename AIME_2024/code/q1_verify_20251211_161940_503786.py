inputs = {'log_base': 2, 'eq1_rhs_num': 1, 'eq1_rhs_den': 2, 'eq2_rhs_num': 1, 'eq2_rhs_den': 3, 'eq3_rhs_num': 1, 'eq3_rhs_den': 4, 'exp_x_in_target': 4, 'exp_y_in_target': 3, 'exp_z_in_target': 2}

from fractions import Fraction

def solve(eq2_rhs_den):
    """
    Compute m+n for |log2(x^4 y^3 z^2)| given the system:
      log2(x/(yz)) = 1/2
      log2(y/(xz)) = 1/eq2_rhs_den
      log2(z/(xy)) = 1/4

    Parameters
    ----------
    eq2_rhs_den : int
        Denominator of the second equation's RHS (i.e., RHS = 1/eq2_rhs_den).
        Reasonable range: positive integer >= 1.

    Returns
    -------
    int
        The value m+n where |log2(x^4 y^3 z^2)| = m/n in lowest terms.
    """
    # Validate input range
    if not isinstance(eq2_rhs_den, int) or eq2_rhs_den <= 0:
        raise ValueError("eq2_rhs_den must be a positive integer (>= 1).")

    # Right-hand sides as exact rationals
    r1 = Fraction(1, 2)
    r2 = Fraction(1, eq2_rhs_den)
    r3 = Fraction(1, 4)

    # Let a = log2(x), b = log2(y), c = log2(z)
    # System:
    # a - b - c = r1
    # -a + b - c = r2
    # -a - b + c = r3
    # Solve by pairwise addition:
    a = - (r2 + r3) / 2
    b = - (r1 + r3) / 2
    c = - (r1 + r2) / 2

    # Target: |4a + 3b + 2c|
    S = abs(4*a + 3*b + 2*c)  # Fraction in lowest terms
    return S.numerator + S.denominator

# 调用 solve
result = solve(inputs['eq2_rhs_den'])
print(result)