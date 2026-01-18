inputs = {'distance_km': 9}

import math

def solve(distance_km):
    D = float(distance_km)
    s = 0.5 * (-2.0 + math.sqrt(4.0 + 5.0 * D))
    total_hours = D / (s + 0.5) + (4.0 - D / s)
    minutes = 60.0 * total_hours
    return int(round(minutes)) if abs(minutes - round(minutes)) < 1e-9 else minutes

solve(9)

# 调用 solve
result = solve(inputs['distance_km'])
print(result)