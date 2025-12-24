inputs = {'log_abs_x4y3z2': 8}

from fractions import Fraction

def solve(log_abs_x4y3z2):
    # Given:
    # -a + b - c = 1/3
    # -a - b + c = 1/4
    # |4a + 3b + 2c| = 25 / log_abs_x4y3z2
    # Target: log2(x/(yz)) = a - b - c = 1/N -> return N
    
    S = Fraction(25, log_abs_x4y3z2)
    # Derived: a = -7/24, b - c = 1/24
    # Then A = a - b - c = -3/4 ± (2/5)S
    candidates = [Fraction(-3, 4) - Fraction(2, 5) * S,
                  Fraction(-3, 4) + Fraction(2, 5) * S]
    
    # Choose the positive candidate (since it's 1/N with N>0)
    A_pos = None
    for A in candidates:
        if A > 0:
            A_pos = A
            break
    if A_pos is None:
        # Fallback: choose the larger candidate if none are positive
        A_pos = max(candidates)
    
    N = Fraction(1, A_pos)
    return int(N) if N.denominator == 1 else N

solve(8)

# 调用 solve
result = solve(inputs['log_abs_x4y3z2'])
print(result)