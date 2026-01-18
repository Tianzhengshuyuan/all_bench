inputs = {'distance_km': 9}

def solve(distance_km):
    from math import sqrt
    T1 = 4.0
    T2 = 2.0 + 24.0 / 60.0
    delta = T1 - T2
    k = 2.0 * distance_km / delta
    s = -1.0 + sqrt(1.0 + k)
    t_hours = T1 - distance_km / s
    total_minutes = (distance_km / (s + 0.5) + t_hours) * 60.0
    if abs(total_minutes - round(total_minutes)) < 1e-9:
        return int(round(total_minutes))
    return total_minutes

solve(9)

# 调用 solve
result = solve(inputs['distance_km'])
print(result)