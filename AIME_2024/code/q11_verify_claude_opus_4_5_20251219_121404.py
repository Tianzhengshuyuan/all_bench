inputs = {'modulus': 4}

import numpy as np
from scipy.optimize import minimize_scalar

def solve(modulus):
    # We have z = a + bi with |z| = modulus, so a^2 + b^2 = modulus^2
    # The expression is (75 + 117i)z + (96 + 144i)/z
    # After simplification, Re(w) = 81a - 108b
    # We want to maximize 81a - 108b subject to a^2 + b^2 = modulus^2
    
    # To maximize 81a - 108b, we want b to be as negative as possible
    # So b = -sqrt(modulus^2 - a^2)
    # f(a) = 81a + 108*sqrt(modulus^2 - a^2)
    
    r_squared = modulus ** 2
    
    # Define the function to maximize (we'll minimize the negative)
    def neg_real_part(a):
        if a**2 > r_squared:
            return float('inf')
        b = -np.sqrt(r_squared - a**2)
        return -(81 * a - 108 * b)
    
    # The valid range for a is [-modulus, modulus]
    result = minimize_scalar(neg_real_part, bounds=(-modulus, modulus), method='bounded')
    
    # Return the maximum value (negative of the minimum)
    return round(-result.fun)

# Call the function with the given modulus value
result = solve(4)
result

# 调用 solve
result = solve(inputs['modulus'])
print(result)