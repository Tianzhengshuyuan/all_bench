inputs = {'k': 26}

def solve(k):
    from fractions import Fraction
    try:
        fk = Fraction(k).limit_denominator()
        res = fk * fk / 4
        return res.numerator if res.denominator == 1 else float(res)
    except Exception:
        r = (k ** 2) / 4
        try:
            return int(r) if float(r).is_integer() else r
        except Exception:
            return r

solve(10)

# 调用 solve
result = solve(inputs['k'])
print(result)