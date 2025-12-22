inputs = {'minutes': 28}

def solve(minutes):
    from math import sqrt

    # Constants from the problem
    distance_km = 9.0
    base_time_hours = 4.0
    faster_time_hours = 2.0 + (minutes / 60.0)
    speed_increment = 2.0
    extra_speed = 0.5

    # Compute delta between the two total times
    delta = base_time_hours - faster_time_hours  # equals 2 - minutes/60

    # Solve for s using: 9*(1/s - 1/(s+2)) = delta -> s(s+2) = 18/delta
    if delta == 0:
        raise ValueError("Invalid minutes leading to zero time difference.")
    rhs = 2 * distance_km / delta  # 18/delta

    # Quadratic: s^2 + 2s - rhs = 0
    disc = 4 + 4 * rhs
    s1 = (-2 + sqrt(disc)) / 2
    s2 = (-2 - sqrt(disc)) / 2
    s = s1 if s1 > 0 else s2

    # Compute coffee time t (in hours)
    t_hours = base_time_hours - distance_km / s

    # Total time at speed s + 0.5
    total_hours = distance_km / (s + extra_speed) + t_hours
    total_minutes = int(round(total_hours * 60))

    return total_minutes

# 调用 solve
result = solve(inputs['minutes'])
print(result)