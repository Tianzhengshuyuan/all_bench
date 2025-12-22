inputs = {'exponent_x': 4}

from fractions import Fraction

def solve(exponent_x):
    # Given system of equations:
    # log_2(x/yz) = 1/2
    # log_2(y/xz) = 1/3
    # log_2(z/xy) = 1/4
    
    # Let a = log_2(x), b = log_2(y), c = log_2(z)
    # Then:
    # a - b - c = 1/2
    # -a + b - c = 1/3
    # -a - b + c = 1/4
    
    # Solve the system of linear equations
    # Equation 1: a - b - c = 1/2
    # Equation 2: -a + b - c = 1/3
    # Equation 3: -a - b + c = 1/4
    
    # Add equations 1 and 2: -2c = 1/2 + 1/3 = 5/6, so c = -5/12
    # Add equations 2 and 3: -2a = 1/3 + 1/4 = 7/12, so a = -7/24
    # Add equations 1 and 3: -2b = 1/2 + 1/4 = 3/4, so b = -3/8
    
    a = Fraction(-7, 24)  # log_2(x)
    b = Fraction(-3, 8)   # log_2(y)
    c = Fraction(-5, 12)  # log_2(z)
    
    # We need |log_2(x^exponent_x * y^3 * z^2)|
    # = |exponent_x * log_2(x) + 3 * log_2(y) + 2 * log_2(z)|
    # = |exponent_x * a + 3 * b + 2 * c|
    
    result = exponent_x * a + 3 * b + 2 * c
    result_abs = abs(result)
    
    # result_abs is m/n where m and n are relatively prime
    m = result_abs.numerator
    n = result_abs.denominator
    
    return m + n

result = solve(4)

# 调用 solve
result = solve(inputs['exponent_x'])
print(result)