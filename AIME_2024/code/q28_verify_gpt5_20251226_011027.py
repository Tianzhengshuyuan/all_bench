inputs = {'r': '20√21/63'}

from math import sqrt, acos, cos, pi
import re

def solve(r):
    # Parse r if it's a string like "20√21/63" or "20*sqrt(21)/63"
    def parse_r(val):
        if isinstance(val, (int, float)):
            return float(val)
        s = str(val).strip()
        s = s.replace(' ', '')
        s = s.replace('√', 'sqrt')
        # Insert multiplication sign before sqrt if missing (e.g., 20sqrt(21) -> 20*sqrt(21))
        s = re.sub(r'(\d|\))(?=sqrt)', r'\1*', s)
        # Ensure sqrt arguments are parenthesized (e.g., sqrt21 -> sqrt(21))
        s = re.sub(r'sqrt([0-9.]+)', r'sqrt(\1)', s)
        s = s.replace('^', '**')
        return float(eval(s, {"__builtins__": {}}, {"sqrt": sqrt}))

    r_val = parse_r(r)
    s = 16.0 * (r_val * r_val)

    # Cubic: 2 N^3 - (260 + s) N^2 - (4608 - 260 s) N - (2304 s - 599040) = 0
    a = 2.0
    b = -(260.0 + s)
    c = -(4608.0 - 260.0 * s)
    d = -(2304.0 * s - 599040.0)

    # Depressed cubic y^3 + p y + q = 0 via x = y - b/(3a)
    b1 = b / a
    c1 = c / a
    d1 = d / a
    p = c1 - (b1 * b1) / 3.0
    q = (2.0 * b1 * b1 * b1) / 27.0 - (b1 * c1) / 3.0 + d1
    disc = (q / 2.0) ** 2 + (p / 3.0) ** 3

    def cbrt(x):
        return (abs(x)) ** (1.0 / 3.0) * (1 if x >= 0 else -1)

    roots = []
    if disc > 1e-15:
        A = -q / 2.0 + sqrt(disc)
        B = -q / 2.0 - sqrt(disc)
        y = cbrt(A) + cbrt(B)
        x = y - b1 / 3.0
        roots.append(x)
    elif abs(disc) <= 1e-15:
        y1 = 2.0 * cbrt(-q / 2.0)
        y2 = -cbrt(-q / 2.0)
        roots.append(y1 - b1 / 3.0)
        roots.append(y2 - b1 / 3.0)
    else:
        r3 = sqrt(max(0.0, -p / 3.0))
        denom = r3 ** 3 if r3 != 0 else 1.0
        theta = acos(max(-1.0, min(1.0, (-q / 2.0) / denom)))
        for k in range(3):
            y = 2.0 * r3 * cos((theta + 2.0 * pi * k) / 3.0)
            roots.append(y - b1 / 3.0)

    # Filter physically valid solutions N in (48, 130)
    eps = 1e-7
    candidates = []
    for N in roots:
        if 48.0 - eps <= N <= 130.0 + eps:
            denom = 260.0 * N - N * N - 2304.0
            if abs(denom) < 1e-12:
                continue
            s_check = 2.0 * (130.0 - N) * (N * N - 2304.0) / denom
            residual = abs(s_check - s)
            candidates.append((residual, N))

    if not candidates:
        # Fallback: search for minimal residual in [48,130]
        best = (float('inf'), None)
        for i in range(10001):
            N = 48.0 + (130.0 - 48.0) * i / 10000.0
            denom = 260.0 * N - N * N - 2304.0
            if abs(denom) < 1e-12:
                continue
            s_check = 2.0 * (130.0 - N) * (N * N - 2304.0) / denom
            residual = abs(s_check - s)
            if residual < best[0]:
                best = (residual, N)
        N_ans = best[1]
    else:
        # Choose the candidate with smallest residual; if tie, choose the smaller N
        candidates.sort(key=lambda x: (x[0], x[1]))
        min_res = candidates[0][0] + 1e-9
        small_candidates = [N for (res, N) in candidates if res <= min_res]
        N_ans = min(small_candidates)

    # Return integer if very close
    if abs(round(N_ans) - N_ans) < 1e-9:
        return int(round(N_ans))
    return N_ans

solve(20*sqrt(21)/63)

# 调用 solve
result = solve(inputs['r'])
print(result)