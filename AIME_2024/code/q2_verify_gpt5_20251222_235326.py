inputs = {'k': 3}

def solve(k):
    import sympy as sp
    k = sp.nsimplify(k)
    theta = sp.symbols('theta', real=True)
    sqrtk = sp.sqrt(k)
    # Intersection x(θ) of line from family with AB
    x_expr = (sp.cos(theta) * (sp.sin(theta) - sqrtk/2)) / (sp.sin(theta) - sqrtk * sp.cos(theta))
    theta0 = sp.atan(sqrtk)
    x_lim = sp.simplify(sp.limit(x_expr, theta, theta0))
    y_lim = sqrtk/2 - sqrtk * x_lim
    oc2 = sp.simplify(x_lim**2 + y_lim**2)
    oc2_rat = sp.nsimplify(oc2)
    num, den = sp.fraction(oc2_rat)
    return int(num) + int(den)

solve(3)

# 调用 solve
result = solve(inputs['k'])
print(result)