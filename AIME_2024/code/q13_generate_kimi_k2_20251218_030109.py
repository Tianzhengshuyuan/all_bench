inputs = {'walk_length': 767}

def solve(walk_length):
    # walk_length is 9 km
    # Let s be speed in km/h, t be coffee time in hours
    # Equation 1: walk_length/s + t = 4
    # Equation 2: walk_length/(s+2) + t = 2.4  (2h 24m = 2.4 h)
    
    # Subtract: (walk_length/s - walk_length/(s+2)) = 4 - 2.4 = 1.6
    # => walk_length * (1/s - 1/(s+2)) = 1.6
    # => walk_length * ( (s+2 - s) / (s(s+2)) ) = 1.6
    # => walk_length * 2 / (s(s+2)) = 1.6
    # => 2 * walk_length = 1.6 * s(s+2)
    # => 1.6 s^2 + 3.2 s - 2*walk_length = 0
    # Multiply by 5: 8 s^2 + 16 s - 10*walk_length = 0
    # => 4 s^2 + 8 s - 5*walk_length = 0
    
    a = 4
    b = 8
    c = -5 * walk_length
    
    # Quadratic formula: s = (-b ± sqrt(b^2 - 4ac)) / (2a)
    import math
    discriminant = b**2 - 4*a*c
    s1 = (-b + math.sqrt(discriminant)) / (2*a)
    s2 = (-b - math.sqrt(discriminant)) / (2*a)
    
    # Choose positive speed
    s = s1 if s1 > 0 else s2
    
    # Find t from first equation: t = 4 - walk_length/s
    t_hours = 4 - walk_length / s
    
    # Now compute time for speed s + 0.5
    new_speed = s + 0.5
    walk_time_hours = walk_length / new_speed
    total_time_hours = walk_time_hours + t_hours
    
    # Convert to minutes
    total_minutes = total_time_hours * 60
    return int(round(total_minutes))

# 调用 solve
result = solve(inputs['walk_length'])
print(result)