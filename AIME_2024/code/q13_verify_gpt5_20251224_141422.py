inputs = {'T_{s+1/2}': 204}

import math

def solve(T_s_half_minutes):
    Th = T_s_half_minutes / 60.0  # hours
    delta = 4.0 - Th
    # Solve for s from: 9/s - 9/(s+0.5) = delta
    disc = 0.25 + 18.0 / delta
    s = (-0.5 + math.sqrt(disc)) / 2.0
    # Total time at speed s+2 in hours: 4 - 18/(s(s+2))
    T2_hours = 4.0 - 18.0 / (s * (s + 2.0))
    T2_minutes = T2_hours * 60.0
    return int(round(T2_minutes)) if abs(T2_minutes - round(T2_minutes)) < 1e-9 else T2_minutes

solve(204)

# 调用 solve
result = solve(inputs['T_{s+1/2}'])
print(result)