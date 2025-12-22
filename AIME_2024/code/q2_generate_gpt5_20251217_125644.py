inputs = {'exponent': 2}

def solve(exponent):
    from fractions import Fraction
    from math import isqrt

    # Points:
    # O(0,0), A(1/2, 0), B(0, sqrt(3)/2)
    # Line AB has slope m = -sqrt(3), so tan^2(theta0) = 3.
    # Compute tan^2(theta0) exactly from squared rise/run:
    dy2 = Fraction(3, 4)  # (sqrt(3)/2)^2
    dx2 = Fraction(1, 4)  # (0 - 1/2)^2
    tan2 = dy2 / dx2      # = 3

    # L'Hôpital setup gives x = cos^3(theta0) where tan(theta0) = sqrt(3)
    # Use identity cos(theta0) = 1/sqrt(1 + tan^2(theta0)) exactly.
    total = tan2 + 1      # = 4
    # total is a rational perfect square here: 4 = 2^2
    num, den = total.numerator, total.denominator
    rt_num, rt_den = isqrt(num), isqrt(den)
    if rt_num * rt_num != num or rt_den * rt_den != den:
        # Fallback to float if not a perfect square (not expected in this problem)
        from math import sqrt
        cos_theta = Fraction.from_float(1 / sqrt(float(total))).limit_denominator(10**9)
    else:
        # sqrt(total) = sqrt(num/den) = rt_num/rt_den, so cos = 1/sqrt(total) = rt_den/rt_num
        cos_theta = Fraction(rt_den, rt_num)

    x = cos_theta ** 3  # Fraction for x-coordinate of C on AB

    # Using AB: y = -sqrt(3) x + sqrt(3)/2, so y^2 = 3(1/2 - x)^2
    half = Fraction(1, 2)
    oc2 = x * x + 3 * (half - x) * (half - x)  # This equals OC^2, a rational number

    # We want OC^exponent = (OC^2)^(exponent/2). For this problem exponent=2.
    if exponent % 2 != 0:
        # In general, OC^(odd) is not rational here; problem uses exponent=2.
        raise ValueError("Exponent must be even for OC^exponent to be rational.")
    k = exponent // 2
    val = oc2 ** k  # Fraction p/q

    return val.numerator + val.denominator

# 调用 solve
result = solve(inputs['exponent'])
print(result)