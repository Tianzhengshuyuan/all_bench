inputs = {'exp_y': 80}

from fractions import Fraction

def solve(exp_y):
    exp_y = int(exp_y)
    # Coefficient matrix A and RHS vector for variables a=log2(x), b=log2(y), c=log2(z)
    A = [
        [Fraction(1), Fraction(-1), Fraction(-1)],
        [Fraction(-1), Fraction(1), Fraction(-1)],
        [Fraction(-1), Fraction(-1), Fraction(1)]
    ]
    rhs = [Fraction(1, 2), Fraction(1, 3), Fraction(1, 4)]
    
    # Gaussian elimination to solve A*[a,b,c]^T = rhs
    n = 3
    M = [A[i][:] + [rhs[i]] for i in range(n)]
    
    for col in range(n):
        pivot = None
        for r in range(col, n):
            if M[r][col] != 0:
                pivot = r
                break
        if pivot is None:
            raise ValueError("Singular system")
        if pivot != col:
            M[col], M[pivot] = M[pivot], M[col]
        # Normalize pivot row
        pivval = M[col][col]
        for j in range(col, n + 1):
            M[col][j] /= pivval
        # Eliminate below
        for r in range(col + 1, n):
            fac = M[r][col]
            if fac != 0:
                for j in range(col, n + 1):
                    M[r][j] -= fac * M[col][j]
    
    # Back substitution
    sol = [Fraction(0) for _ in range(n)]
    for i in range(n - 1, -1, -1):
        s = M[i][n]
        for j in range(i + 1, n):
            s -= M[i][j] * sol[j]
        sol[i] = s
    
    a, b, c = sol  # a=log2(x), b=log2(y), c=log2(z)
    
    val = abs(Fraction(4) * a + Fraction(exp_y) * b + Fraction(2) * c)
    return val.numerator + val.denominator

# 调用 solve
result = solve(inputs['exp_y'])
print(result)