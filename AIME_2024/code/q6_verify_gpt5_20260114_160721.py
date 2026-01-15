inputs = {'k': 3}

def solve(k):
    import math

    eps = 1e-12
    t = abs(k)

    def C_nonext(t, a):
        # Count solutions to |cos(theta)| = a for theta in [0, t*pi]
        m = int(math.floor(t / 2.0 + eps))  # number of full 2π blocks
        s = t - 2 * m  # normalized remainder in [0, 2)
        alpha_over_pi = math.acos(a) / math.pi
        vals = [alpha_over_pi, 1.0 - alpha_over_pi, 1.0 + alpha_over_pi, 2.0 - alpha_over_pi]
        c = sum(1 for v in vals if v <= s + eps)
        return 4 * m + c

    # For p(x): y = h(sin(2πx)) over x in [0,1]
    # Np_min = 8 (y=0 hits), Np_max = 9 (y=1 hits), hence Mx = 16
    Mx = 16

    # For q(y): x = h(cos(kπ y)) over y in [0,1]
    Nq_min = C_nonext(t, 0.25) + C_nonext(t, 0.75)
    Count1 = int(math.floor(t + eps)) + 1            # |cos| = 1
    Count0 = int(math.floor(t + 0.5 + eps))          # |cos| = 0
    Nq_half = C_nonext(t, 0.5)                       # |cos| = 1/2
    Nq_max = Count1 + Count0 + Nq_half

    My = Nq_min + Nq_max - 1

    base = Mx * My

    # Boundary correction: intersection on top edge (y=1) if x_top in {0, 1}
    c_top = abs(math.cos(math.pi * k))
    h_top = 4.0 * abs(abs(c_top - 0.5) - 0.25)
    delta = 1 if (abs(h_top - 0.0) <= eps or abs(h_top - 1.0) <= eps) else 0

    return base + delta

solve(3)

# 调用 solve
result = solve(inputs['k'])
print(result)