inputs = {'exp_y': 3}

from fractions import Fraction

def solve(exp_y):
    """
    Solve for m+n where |log2(x^4 * y^exp_y * z^2)| = m/n given:
      log2(x/(yz)) = 1/2
      log2(y/(xz)) = 1/3
      log2(z/(xy)) = 1/4

    Parameters:
      exp_y (int): exponent of y in the target expression. 
                   Reasonable range: any integer (typically non-negative small integers, e.g., 0 <= exp_y <= 10**6).

    Returns:
      int: m + n for the reduced fraction m/n.
    """
    # Convert the right-hand sides to exact fractions
    r1 = Fraction(1, 2)
    r2 = Fraction(1, 3)
    r3 = Fraction(1, 4)

    # Let a = log2(x), b = log2(y), c = log2(z)
    # The system:
    # a - b - c = r1
    # -a + b - c = r2
    # -a - b + c = r3
    #
    # Adding equation pairs:
    # (1)+(2): -2c = r1 + r2  -> c = -(r1 + r2)/2
    # (1)+(3): -2b = r1 + r3  -> b = -(r1 + r3)/2
    # (2)+(3): -2a = r2 + r3  -> a = -(r2 + r3)/2
    a = -(r2 + r3) / 2
    b = -(r1 + r3) / 2
    c = -(r1 + r2) / 2

    # Compute |4a + exp_y*b + 2c|
    val = abs(4 * a + Fraction(exp_y, 1) * b + 2 * c)

    # val is a reduced Fraction; return m + n
    return val.numerator + val.denominator

# 调用 solve
result = solve(inputs['exp_y'])
print(result)