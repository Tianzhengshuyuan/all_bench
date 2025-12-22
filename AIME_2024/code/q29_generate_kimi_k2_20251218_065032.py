inputs = {'BC_length': 87}

def solve(BC_length):
    # Given constants
    AB = 107
    FG = 17
    EF = 184
    
    # Using the equation derived from the perpendicular bisector approach
    # (x + 92)^2 + 8^2 = 25^2 + 92^2
    # Solving for x = DE
    # x^2 + 184x + 8464 + 64 = 625 + 8464
    # x^2 + 184x + 64 = 625
    # x^2 + 184x - 561 = 0
    a = 1
    b = 184
    c = -561
    discriminant = b**2 - 4*a*c
    x = (-b + discriminant**0.5) / (2*a)  # positive root
    
    # CE = CD - DE = AB - x
    CE = AB - x
    return int(round(CE))

# 调用 solve
result = solve(inputs['BC_length'])
print(result)