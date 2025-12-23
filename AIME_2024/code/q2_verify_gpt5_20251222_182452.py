inputs = {'radicand': 3}

import sympy as sp

def solve(radicand):
    R = sp.nsimplify(radicand)
    s = sp.sqrt(R)
    a0 = 1 / sp.sqrt(1 + R)  # cos(theta0)
    x = a0**3
    y = s/2 - s*x
    oc2 = sp.nsimplify(sp.simplify(x**2 + y**2))
    if isinstance(oc2, sp.Rational):
        return int(oc2.p + oc2.q)
    oc2_rat = sp.nsimplify(oc2.evalf())
    if isinstance(oc2_rat, sp.Rational):
        return int(oc2_rat.p + oc2_rat.q)
    return None

solve(3)

# 调用 solve
result = solve(inputs['radicand'])
print(result)