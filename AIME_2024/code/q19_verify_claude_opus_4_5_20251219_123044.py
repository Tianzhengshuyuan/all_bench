inputs = {'circumradius': 13}

def solve(circumradius):
    """
    Solve for AB * AC given the circumradius R.
    
    Given:
    - Circumradius R = circumradius
    - Inradius r = 6
    - IA perpendicular to OI
    
    Using the solution approach:
    1. AB * AC = 3 * AI^2
    2. AI^2 = AO^2 - OI^2 (since triangle AOI is right-angled at I)
    3. AO = R (circumradius)
    4. OI^2 = R(R - 2r) (Euler's formula)
    """
    R = circumradius
    r = 6  # inradius is fixed at 6
    
    # Euler's formula for distance between incenter and circumcenter
    OI_squared = R * (R - 2 * r)
    
    # Since IA is perpendicular to OI, triangle AOI is right-angled at I
    # AO = R (circumradius), so AI^2 = AO^2 - OI^2
    AO = R
    AI_squared = AO**2 - OI_squared
    
    # From the solution: AB * AC = 3 * AI^2
    result = 3 * AI_squared
    
    return result

# Call the function with the given circumradius
answer = solve(13)

# 调用 solve
result = solve(inputs['circumradius'])
print(result)