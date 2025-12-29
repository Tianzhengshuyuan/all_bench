from fractions import Fraction
inputs = {'r2': Fraction(657, 64)}

from fractions import Fraction

def solve(r2):
    # Given: surface area 54 -> ab+bc+ca=27; volume 23 -> abc=23
    # At maximum diagonal, two sides are equal: let a=b=x, c=y
    # Constraints: x^2 + 2xy = 27, x^2 y = 23
    # => x satisfies cubic: x^3 - 27x + 46 = 0
    s = Fraction(27, 1)
    v = Fraction(23, 1)
    target_d2 = 4 * r2

    def P(x):
        return x**3 - s * x + 2 * v

    # Find rational roots among divisors of 2*v (here 46)
    D = abs(int(2 * v))
    candidates = []
    for d in range(1, D + 1):
        if D % d == 0:
            for sign in (1, -1):
                x = Fraction(sign * d, 1)
                if P(x) == 0 and x > 0:
                    candidates.append(x)

    # Among candidates, pick the one matching the given r^2 if possible; else the maximizing diagonal
    best_x = None
    best_d2 = None
    for x in candidates:
        y = v / (x * x)
        d2 = 2 * x * x + y * y
        if d2 == target_d2:
            return x
        if best_d2 is None or d2 > best_d2:
            best_d2 = d2
            best_x = x

    return best_x

solve(Fraction(657, 64))

# 调用 solve
result = solve(inputs['r2'])
print(result)