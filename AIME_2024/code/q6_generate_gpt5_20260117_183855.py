inputs = {'n': 4}

def solve(n):
    import math

    # Work with absolute value of n (cos is even in its frequency)
    an = abs(float(n))
    # Handle near-integer n robustly
    rn = round(an)
    if abs(an - rn) < 1e-12:
        m = int(rn)
        f = 0.0
    else:
        m = int(math.floor(an))
        f = an - m

    pi = math.pi

    # Helper: number of extra hits in the leftover fraction f of a |cos|-period for |cos|=c (c in (0,1))
    # In each full |cos| period (length pi in theta), there are exactly 2 solutions for |cos|=c.
    # Over the leftover fraction f in [0,1), we add 1 if f >= alpha/pi (descending cross),
    # and another 1 if f >= 1 - alpha/pi (ascending cross), where alpha = arccos(c).
    def extra_hits_for_c(f, c):
        alpha_frac = math.acos(c) / pi  # in (0, 0.5]
        eps = 1e-15
        s = 0
        if f + eps >= alpha_frac:
            s += 1
        if f + eps >= 1 - alpha_frac:
            s += 1
        return s

    # Counts for q(y)=0 correspond to |cos| in {1/4, 3/4}
    s1 = extra_hits_for_c(f, 1.0 / 4.0)
    s2 = extra_hits_for_c(f, 3.0 / 4.0)
    zeros_q = (2 * m + s1) + (2 * m + s2)  # 4*m + s1 + s2

    # Counts for q(y)=1 correspond to |cos| in {0, 1/2, 1}
    # |cos|=0 occurs once per full |cos| period, plus one if leftover >= 1/2 period
    zeros_abs = m + (1 if f + 1e-15 >= 0.5 else 0)
    # |cos|=1/2 uses the same extra_hits_for_c logic
    sh = extra_hits_for_c(f, 1.0 / 2.0)
    half_hits = 2 * m + sh
    # |cos|=1 occurs at theta = k*pi, k=0..m inclusive => m+1
    ones_abs = m + 1

    ones_q = zeros_abs + half_hits + ones_abs  # = 4*m + 1 + sh + I

    # Number of up/down "waves" for q over y in [0,1]
    Wq = (zeros_q + ones_q - 1)  # subtract 1 to count monotone segments
    # For p (sin(2πx)) over x in [0,1], the counts are fixed: zeros 8, ones 9 -> waves 16
    Wp = 16

    # Intersections = Wp * Wq plus the corner (1,1) which is not included in the wave-crossing product
    intersections = Wp * Wq + 1
    return int(intersections)

solve(3)

# 调用 solve
result = solve(inputs['n'])
print(result)