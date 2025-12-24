inputs = {'xy': 25}

def solve(xy):
    import cmath

    # From N = x*log_x(y) = 4y*log_y(x) and log_x(y)*log_y(x)=1, we get N^2 = 4*xy
    # Hence N = 2*sqrt(xy). Use principal complex sqrt for generality.
    res = 2 * cmath.sqrt(xy)

    if abs(res.imag) < 1e-12:
        r = res.real
        if abs(r - round(r)) < 1e-12:
            return int(round(r))
        return r
    return res

solve(25)

# 调用 solve
result = solve(inputs['xy'])
print(result)