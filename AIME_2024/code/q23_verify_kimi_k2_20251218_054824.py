inputs = {'hyperbola_a_squared': 20}

import math

def solve(hyperbola_a_squared):
    a2 = hyperbola_a_squared
    # From the hyperbola equation x^2/a^2 - y^2/b^2 = 1, we have b^2 = 24
    # But we need to derive b^2 from the given a^2 and the fact that the hyperbola is x^2/a^2 - y^2/b^2 = 1
    # However, the original equation is fixed as x^2/20 - y^2/24 = 1, so b^2 = 24
    # But we want to generalize based on the asymptote slope condition.
    # The asymptotes are y = ±(b/a)x, so slope squared is b^2/a^2.
    # From the original problem, we know that the critical slope squared is 6/5, and b^2/a^2 = 24/20 = 6/5.
    # So we can derive b2 from the asymptote slope relation: b2/a2 = 6/5 → b2 = (6/5)*a2
    b2 = 6 * a2 // 5  # This ensures integer relation as in the original: 24 = 6*20/5
    # Now compute the minimal BD^2
    # From the analysis, the minimal value of BD^2 is 4 * (a2 + b2) * (a2 / (b2 - a2)) ??? 
    # Actually, from the solution: BD^2 = 4 * (x^2 + y^2) = 4 * 120 * (1 + m^2)/(6 - 5*m^2)
    # And minimal occurs as m^2 → 5/6 from above, giving limit 120 → so BD^2 → 480
    # We can re-derive: x^2 + y^2 = (a2*b2*(1 + m^2))/(b2 - a2*m^2)
    # At limit m^2 → a2/b2, we get x^2 + y^2 → (a2*b2*(1 + a2/b2))/(b2 - a2*(a2/b2)) = (a2*b2 + a2^2)/(b2 - a2^2/b2) = a2(b2 + a2)/((b2^2 - a2^2)/b2) = a2*b2*(a2 + b2)/(b2^2 - a2^2)
    # But simpler: from the expression minimized, we know BD^2 = 4 * (x^2 + y^2) = 4 * [a2*b2*(1 + m^2)/(b2 - a2*m^2)]
    # At limit m^2 → b2/a2? No — from original: m^2 → 5/6 = a2/b2? a2=20, b2=24 → a2/b2=20/24=5/6. Yes.
    # So limit as m^2 → a2/b2 from above:
    # x^2 + y^2 → a2*b2*(1 + a2/b2)/(b2 - a2*(a2/b2)) = a2*b2*( (b2 + a2)/b2 ) / ( (b2^2 - a2^2)/b2 ) = a2*(a2 + b2)/((b2 - a2)*(b2 + a2)/b2) → wait
    # Actually:
    # = a2*b2*(1 + a2/b2) / (b2 - a2^2/b2) = a2*b2*( (b2 + a2)/b2 ) / ( (b2^2 - a2^2)/b2 ) = a2*(a2 + b2) / ((b2 - a2)*(b2 + a2)/b2) * b2? No.
    # = [a2*(a2 + b2)] / [(b2^2 - a2^2)/b2] = a2*(a2 + b2)*b2 / (b2^2 - a2^2) = a2*b2*(a2 + b2) / ((b2 - a2)(b2 + a2)) = a2*b2 / (b2 - a2)
    # So x^2 + y^2 → a2*b2 / (b2 - a2)
    # Then BD^2 = 4 * (x^2 + y^2) → 4 * a2 * b2 / (b2 - a2)
    bd2_limit = 4 * a2 * b2 // (b2 - a2)
    return bd2_limit

# But note: in the original, a2=20, b2=24 → 4*20*24 / (24-20) = 4*480 / 4 = 480. Correct.
# So we return this limit — the greatest real number less than BD^2 for all such rhombi.

# 调用 solve
result = solve(inputs['hyperbola_a_squared'])
print(result)