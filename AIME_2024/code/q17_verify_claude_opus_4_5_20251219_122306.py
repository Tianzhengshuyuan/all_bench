inputs = {'volume': 23}

from fractions import Fraction
import math
import numpy as np
from scipy.optimize import minimize_scalar

def solve(volume):
    S = 27  # ab + bc + ca = 27
    V = volume  # abc = V
    
    # Search for maximum diagonal squared over all valid boxes
    # Parameterize by c, solve for a, b
    def get_diag_sq(c):
        if c <= 0:
            return None
        ab = V / c
        s = (S * c - V) / (c ** 2)  # a + b
        
        if s <= 0:
            return None
        
        discriminant = s ** 2 - 4 * ab
        if discriminant < 0:
            return None
        
        a = (s + math.sqrt(discriminant)) / 2
        b = (s - math.sqrt(discriminant)) / 2
        
        if a <= 0 or b <= 0:
            return None
        
        return a ** 2 + b ** 2 + c ** 2
    
    # Find the maximum by searching
    max_diag_sq = 0
    
    # Dense search
    for c in np.linspace(0.1, 15, 10000):
        result = get_diag_sq(c)
        if result is not None and result > max_diag_sq:
            max_diag_sq = result
    
    # Check boundary cases: two dimensions equal
    # x^3 - 27x + 2V = 0
    coeffs = [1, 0, -S, 2 * V]
    roots = np.roots(coeffs)
    
    for r in roots:
        if abs(r.imag) < 1e-10 and r.real > 0:
            x = r.real
            c = V / (x ** 2)
            if c > 0:
                diag_sq = 2 * x ** 2 + c ** 2
                if diag_sq > max_diag_sq:
                    max_diag_sq = diag_sq
            
            a = V / (x ** 2)
            if a > 0:
                diag_sq = a ** 2 + 2 * x ** 2
                if diag_sq > max_diag_sq:
                    max_diag_sq = diag_sq
    
    r_squared = max_diag_sq / 4
    
    # For V = 23: x = 2 gives a = b = 2, c = 23/4
    # diag_sq = 8 + 529/16 = 657/16
    # r^2 = 657/64
    
    # Exact calculation
    numerator = 128 + V ** 2
    denominator = 64
    
    frac = Fraction(numerator, denominator)
    p = frac.numerator
    q = frac.denominator
    
    return p + q

result = solve(23)

# 调用 solve
result = solve(inputs['volume'])
print(result)