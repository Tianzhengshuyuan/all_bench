inputs = {'walk_distance': 77}

def solve(walk_distance):
    """
    Solve the walking problem.
    
    Given:
    - Walk distance: walk_distance km
    - At speed s km/h, total time is 4 hours (including t minutes at coffee shop)
    - At speed (s+2) km/h, total time is 2 hours 24 minutes = 2.4 hours (including t minutes at coffee shop)
    - Find total time at speed (s + 0.5) km/h
    
    Equations:
    walk_distance/s + t = 4 (hours)
    walk_distance/(s+2) + t = 2.4 (hours)
    
    Subtracting: walk_distance/s - walk_distance/(s+2) = 1.6
    """
    
    # From the two equations:
    # walk_distance/s + t = 4
    # walk_distance/(s+2) + t = 2.4
    # Subtracting: walk_distance/s - walk_distance/(s+2) = 1.6
    
    # walk_distance * (s+2) - walk_distance * s = 1.6 * s * (s+2)
    # walk_distance * 2 = 1.6 * s * (s+2)
    # 2 * walk_distance = 1.6 * s^2 + 3.2 * s
    # Multiply by 5/2: 5 * walk_distance = 4 * s^2 + 8 * s
    # 4 * s^2 + 8 * s - 5 * walk_distance = 0
    
    # Using quadratic formula: s = (-8 + sqrt(64 + 80*walk_distance)) / 8
    import math
    
    a = 4
    b = 8
    c = -5 * walk_distance
    
    discriminant = b**2 - 4*a*c
    s = (-b + math.sqrt(discriminant)) / (2*a)
    
    # Now find t from first equation: t = 4 - walk_distance/s (in hours)
    t = 4 - walk_distance / s
    
    # Time at speed (s + 0.5):
    new_speed = s + 0.5
    total_time_hours = walk_distance / new_speed + t
    
    # Convert to minutes
    total_time_minutes = total_time_hours * 60
    
    return round(total_time_minutes)


result = solve(9)

# 调用 solve
result = solve(inputs['walk_distance'])
print(result)