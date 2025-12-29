from fractions import Fraction
inputs = {'p_gp_given_prize': Fraction(1, 115)}

from fractions import Fraction
from math import comb

def solve(p_gp_given_prize):
    # S has 10 elements, she picks 4. Grand prize: match all 4.
    # P(G | Prize(N)) = 1 / sum_{k=N..4} C(4,k) * C(6, 4-k)
    def count_k(k):
        return comb(4, k) * comb(6, 4 - k)
    for N in range(1, 5):
        total = sum(count_k(k) for k in range(N, 5))
        if Fraction(1, total) == p_gp_given_prize:
            return N
    return None

solve(Fraction(1, 115))

# 调用 solve
result = solve(inputs['p_gp_given_prize'])
print(result)