inputs = {'selected_digit': 12}

from fractions import Fraction

def solve(selected_digit: int) -> int:
    """
    Compute m+n where |log2(x^k * y^3 * z^2)| = m/n in lowest terms for the system:
      log2(x/(yz)) = 1/2
      log2(y/(xz)) = 1/3
      log2(z/(xy)) = 1/k
    and k replaces the digit '4' in the original problem.
    
    Input:
      selected_digit (k): positive integer (recommended range: 1-9; must be >=1 to avoid division by zero)
      
    Returns:
      int: m + n where |log2(x^k y^3 z^2)| = m/n in lowest terms
    """
    k = int(selected_digit)
    if k <= 0:
        raise ValueError("selected_digit must be a positive integer.")

    # Let a = log2(x), b = log2(y), c = log2(z)
    # From the system:
    # a - b - c = 1/2
    # -a + b - c = 1/3
    # -a - b + c = 1/k
    # Solve via pairwise sums:
    a = - (Fraction(1, 3) + Fraction(1, k)) * Fraction(1, 2)
    b = - (Fraction(1, 2) + Fraction(1, k)) * Fraction(1, 2)
    c = - (Fraction(1, 2) + Fraction(1, 3)) * Fraction(1, 2)

    # Target: |k*a + 3*b + 2*c|
    value = abs(k * a + 3 * b + 2 * c)
    return value.numerator + value.denominator

# 调用 solve
result = solve(inputs['selected_digit'])
print(result)