inputs = {'distance_km': 9}

def solve(distance_km):
    import math
    total1_hours = 4.0
    total2_hours = 2.0 + 24.0 / 60.0
    delta = total1_hours - total2_hours  # 1.6 hours

    # Solve for s from distance*(1/s - 1/(s+2)) = delta
    # => s^2 + 2s - 2*distance/delta = 0
    disc = 4.0 + 8.0 * distance_km / delta
    s = (-2.0 + math.sqrt(disc)) / 2.0

    t_hours = total1_hours - distance_km / s
    total_hours_new_speed = distance_km / (s + 0.5) + t_hours
    minutes = total_hours_new_speed * 60.0

    if abs(minutes - round(minutes)) < 1e-9:
        return int(round(minutes))
    return minutes

solve(9)

# 调用 solve
result = solve(inputs['distance_km'])
print(result)