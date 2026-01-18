inputs = {}

def solve(_):
    # Given constants
    d = 9.0  # distance in km
    T1 = 4.0  # total time in hours for speed s
    T2 = 2.0 + 24.0 / 60.0  # total time in hours for speed s+2 (2h24m)
    delta = T1 - T2  # difference in total times

    # From 9/s - 9/(s+2) = delta => 18 / (s(s+2)) = delta => s^2 + 2s - 18/delta = 0
    K = 18.0 / delta
    disc = 1.0 + K
    s = -1.0 + disc ** 0.5
    if s <= 0:
        s = -1.0 - disc ** 0.5  # fallback, though not expected

    # Compute coffee time t (in hours)
    t_h = T1 - d / s

    # Total time when walking at s + 0.5 km/h
    T3 = d / (s + 0.5) + t_h  # hours
    return int(round(T3 * 60.0))  # minutes

# 调用 solve
result = solve(inputs)
print(result)