inputs = {'log_base': 2, 'eq1_rhs_num': 1, 'eq1_rhs_den': 2, 'eq2_rhs_num': 1, 'eq2_rhs_den': 3, 'eq3_rhs_num': 1, 'eq3_rhs_den': 4, 'exp_x_in_target': 4, 'exp_y_in_target': 3, 'exp_z_in_target': 2}

from fractions import Fraction

def solve(eq1_rhs_num: int) -> int:
    """
    Solve for |log2(x^4 y^3 z^2)| given the system:
        log2(x/(yz)) = eq1_rhs_num/2
        log2(y/(xz)) = eq1_rhs_num/3
        log2(z/(xy)) = eq1_rhs_num/4
    and return m + n where |log2(x^4 y^3 z^2)| = m/n in lowest terms.

    Input:
        eq1_rhs_num: int
        - Reasonable range: any integer (commonly positive).
          The system remains solvable for any integer; eq1_rhs_num = 1 for this problem.

    Returns:
        int: m + n
    """
    r = Fraction(eq1_rhs_num, 1)
    # RHS values as Fractions
    rhs1 = r / 2  # = eq1_rhs_num/2
    rhs2 = r / 3  # = eq1_rhs_num/3
    rhs3 = r / 4  # = eq1_rhs_num/4

    # Let a = log2(x), b = log2(y), c = log2(z)
    # System:
    # a - b - c = rhs1
    # -a + b - c = rhs2
    # -a - b + c = rhs3
    # Sum pairs to eliminate variables:
    c = - (rhs1 + rhs2) / 2
    a = - (rhs2 + rhs3) / 2
    b = - (rhs1 + rhs3) / 2

    value = abs(4*a + 3*b + 2*c)  # |log2(x^4 y^3 z^2)|
    return value.numerator + value.denominator

# 调用 solve
result = solve(inputs['eq1_rhs_num'])
print(result)