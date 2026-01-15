inputs = {'volume': 23}

def solve(volume):
    from fractions import Fraction
    import math

    s2 = 27.0  # ab+bc+ca fixed by surface area 54

    V = volume
    try:
        V_float = float(V)
    except:
        return None

    if V_float <= 0:
        return None

    Vmax = (s2 / 3.0) ** 1.5
    if V_float > Vmax + 1e-12:
        return None

    # Helper for equation x^2 + 2V/x = s2
    def h(x):
        return x * x + 2.0 * V_float / x - s2

    # Try exact integer-root path for cubic x^3 - s2*x + 2V = 0 (rational root theorem)
    # Use it only if it gives the smaller positive root (x < V^{1/3})
    def integer_root_path():
        from math import isclose

        # detect integer volume
        V_is_int = False
        if isinstance(V, int):
            V_is_int = True
            Vi = V
        else:
            # check closeness to integer
            Vi = int(round(V_float))
            if abs(V_float - Vi) < 1e-12:
                V_is_int = True

        if not V_is_int:
            return None

        def divisors(n):
            n = abs(n)
            divs = set()
            i = 1
            while i * i <= n:
                if n % i == 0:
                    divs.add(i)
                    divs.add(n // i)
                i += 1
            return sorted(divs)

        candidates = []
        for d in divisors(2 * Vi):
            for r in (d, -d):
                if r > 0 and (r ** 3 - int(s2) * r + 2 * Vi) == 0:
                    candidates.append(r)
        if not candidates:
            return None

        xstar = V_float ** (1.0 / 3.0)
        # pick the smallest positive integer root that is below xstar (the maximizing one)
        below = [r for r in candidates if r < xstar + 1e-12]
        if not below:
            return None
        x = min(below)

        # Compute r^2 exactly using Fractions: s1 = (3/2)x + 27/(2x), then r^2 = (s1^2 - 54)/4
        xF = Fraction(x, 1)
        s1 = Fraction(3, 2) * xF + Fraction(27, 2) * Fraction(1, xF)
        r2 = (s1 * s1 - Fraction(54, 1)) / 4
        return r2

    r2_exact = integer_root_path()
    if r2_exact is not None:
        r2_frac = r2_exact.limit_denominator()
        return r2_frac.numerator + r2_frac.denominator

    # Numerical bisection for the smaller positive root
    xstar = V_float ** (1.0 / 3.0)
    # bracket [lo, hi] with h(lo) > 0, h(hi) <= 0
    lo = min(1.0, xstar * 0.5 if xstar > 0 else 1e-6)
    # ensure h(lo) > 0
    for _ in range(100):
        if h(lo) > 0:
            break
        lo *= 0.5
    else:
        lo = 1e-12

    hi = xstar
    # ensure h(hi) <= 0 (feasible region)
    if h(hi) > 0:
        # if V is at maximum, the root is at x=3 exactly
        hi = min(math.sqrt(s2), max(hi, 3.0))
    # bisection
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        val = h(mid)
        if val > 0:
            lo = mid
        else:
            hi = mid
        if abs(hi - lo) < 1e-15:
            break
    x = 0.5 * (lo + hi)

    # s1 = a+b+c at this stationary point: s1 = (3/2)x + 27/(2x)
    s1 = 1.5 * x + 27.0 / (2.0 * x)
    r2 = (s1 * s1 - 54.0) / 4.0

    # Convert to fraction if possible
    r2_frac = Fraction(r2).limit_denominator(10**12)
    return r2_frac.numerator + r2_frac.denominator


solve(23)

# 调用 solve
result = solve(inputs['volume'])
print(result)