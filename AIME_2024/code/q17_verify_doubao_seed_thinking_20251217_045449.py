inputs = {'volume': 23}

from sympy import symbols, solve, nsimplify

def solve(volume):
    V = volume
    b = symbols('b')
    equation = b**3 - 27*b + 2*V
    roots = solve(equation, b)
    positive_roots = [root for root in roots if root.is_real and root > 0]
    sum_values = []
    for b_val in positive_roots:
        a = V / (b_val ** 2)
        sum_val = a + 2 * b_val
        sum_values.append(sum_val)
    max_sum = max(sum_values)
    r_squared = (max_sum ** 2 - 54) / 4
    simplified = nsimplify(r_squared, rational=True)
    return simplified.numerator + simplified.denominator

# 调用 solve
result = solve(inputs['volume'])
print(result)