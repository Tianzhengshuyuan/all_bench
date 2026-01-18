inputs = {'AB': 100}

def solve(AB):
    import math
    BC = 16.0
    FG = 17.0
    EF = 184.0
    # Solve x(x + EF) = FG * (BC + FG) for x > 0
    disc = EF * EF + 4 * FG * (BC + FG)
    x = (-EF + math.sqrt(disc)) / 2.0
    CE = AB - x
    # If CE is effectively an integer, return int
    if abs(CE - round(CE)) < 1e-9:
        return int(round(CE))
    return CE

# 调用 solve
result = solve(inputs['AB'])
print(result)