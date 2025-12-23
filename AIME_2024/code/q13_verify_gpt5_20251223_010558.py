inputs = {'distance_km': 9}

def solve(distance_km):
    import math
    d = distance_km
    s = -1 + math.sqrt(1 + 5 * d / 4)
    t_minutes = 60 * (4 - d / s)
    total_minutes = 60 * d / (s + 0.5) + t_minutes
    return int(round(total_minutes))

solve(9)

# 调用 solve
result = solve(inputs['distance_km'])
print(result)