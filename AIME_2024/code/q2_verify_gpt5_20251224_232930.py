inputs = {'OC_squared': 7}

def solve(OC_squared):
    import math
    # OC^2 is given as OC_squared / 16
    num = OC_squared
    den = 16
    g = math.gcd(num, den)
    p = num // g
    q = den // g
    return p + q

solve(7)

# 调用 solve
result = solve(inputs['OC_squared'])
print(result)