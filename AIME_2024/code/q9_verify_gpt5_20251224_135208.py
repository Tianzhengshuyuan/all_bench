inputs = {'xy': 25}

def solve(xy):
    import cmath
    N = 2 * cmath.sqrt(xy)
    if abs(N.imag) < 1e-12:
        r = N.real
        if abs(r - round(r)) < 1e-9:
            return int(round(r))
        return r
    return N

solve(25)

# 调用 solve
result = solve(inputs['xy'])
print(result)