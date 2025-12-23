inputs = {'distance_km': 1}

def solve(distance_km):
    d = float(distance_km)
    total1_hours = 4.0
    total2_hours = 2.0 + 24.0 / 60.0  # 2 hours 24 minutes
    diff = total1_hours - total2_hours  # time difference in hours

    # From d/s - d/(s+2) = diff -> s^2 + 2s = 2d/diff
    val = 2.0 * d / diff
    s = -1.0 + (1.0 + val) ** 0.5  # positive root

    t_hours = total1_hours - d / s  # coffee time in hours
    desired_speed = s + 0.5
    total_time_hours = d / desired_speed + t_hours
    minutes = total_time_hours * 60.0

    if abs(minutes - round(minutes)) < 1e-9:
        return int(round(minutes))
    return minutes

solve(9)

# 调用 solve
result = solve(inputs['distance_km'])
print(result)