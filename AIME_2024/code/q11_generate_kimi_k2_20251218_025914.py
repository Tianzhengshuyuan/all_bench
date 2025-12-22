inputs = {'z_mag': 967}

import math

def solve(z_mag):
    # Constants from the problem
    A = 75
    B = 117
    C = 96
    D = 144
    
    # Simplify the expression to real part: 81*a - 108*b
    # We want to maximize 81*a - 108*b subject to a^2 + b^2 = z_mag^2
    # Let b = -sqrt(z_mag^2 - a^2) to maximize
    # f(a) = 81*a + 108*sqrt(z_mag^2 - a^2)
    # f'(a) = 81 - 108*a / sqrt(z_mag^2 - a^2) = 0
    # 81 = 108*a / sqrt(z_mag^2 - a^2)
    # 81*sqrt(z_mag^2 - a^2) = 108*a
    # sqrt(z_mag^2 - a^2) = (108/81)*a = (4/3)*a
    # z_mag^2 - a^2 = (16/9)*a^2
    # z_mag^2 = a^2 + (16/9)*a^2 = (25/9)*a^2
    # a^2 = (9/25)*z_mag^2
    a = (3/5) * z_mag
    b = -math.sqrt(z_mag**2 - a**2)
    
    real_part = 81*a - 108*b
    return int(round(real_part))

# 调用 solve
result = solve(inputs['z_mag'])
print(result)