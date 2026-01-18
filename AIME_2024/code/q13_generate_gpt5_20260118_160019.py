inputs = {'distance': 10}

import math

def solve(distance):
    d = float(distance)
    # Solve for s using: d/s - d/(s+2) = 1.6  => s^2 + 2s - (5/4)d = 0
    s = (-2 + math.sqrt(4 + 5 * d)) / 2.0
    # t in hours from total time at speed s
    t_hours = 4 - d / s
    # Total time in hours when walking at speed s + 0.5
    total_hours = d / (s + 0.5) + t_hours
    # Return total minutes, rounded to nearest integer
    return int(round(total_hours * 60))

# 调用 solve
result = solve(inputs['distance'])
print(result)