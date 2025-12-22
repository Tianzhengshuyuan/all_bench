inputs = {'n': 2}

def solve(n):
    from fractions import Fraction
    # Let a = log2(x), b = log2(y), c = log2(z)
    # System:
    # a - b - c = 1/2
    # -a + b - c = 1/3
    # -a - b + c = 1/4
    A = [
        [1, -1, -1],
        [-1, 1, -1],
        [-1, -1, 1]
    ]
    rhs = [Fraction(1, 2), Fraction(1, 3), Fraction(1, 4)]

    # Solve 3x3 system
    import copy
    M = copy.deepcopy(A)
    for i in range(3):
        M[i].append(rhs[i])

    # Forward elimination
    for col in range(3):
        # partial pivot
        max_row = col
        for r in range(col+1, 3):
            if abs(M[r][col]) > abs(M[max_row][col]):
                max_row = r
        M[col], M[max_row] = M[max_row], M[col]

        pivot = M[col][col]
        for c in range(col, 4):
            M[col][c] = Fraction(M[col][c]) / pivot

        for r in range(col+1, 3):
            factor = M[r][col]
            for c in range(col, 4):
                M[r][c] -= factor * M[col][c]

    # Back substitution
    sol = [Fraction(0), Fraction(0), Fraction(0)]
    for r in range(2, -1, -1):
        s = sum(M[r][j] * sol[j] for j in range(r+1, 3))
        sol[r] = (M[r][3] - s) / M[r][r]

    a, b, c = sol
    val = 4*a + 3*b + 2*c
    abs_val = abs(val)
    return abs_val.numerator + abs_val.denominator

# 调用 solve
result = solve(inputs['n'])
print(result)