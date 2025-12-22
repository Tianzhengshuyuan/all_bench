inputs = {'hyperbola_a_squared': 30}

def solve(hyperbola_a_squared):
    """
    Solve for the greatest real number less than BD^2 for all rhombi ABCD
    inscribed in the hyperbola x^2/a^2 - y^2/b^2 = 1 with diagonals intersecting at origin.
    
    The hyperbola is x^2/20 - y^2/24 = 1, so a^2 = 20, b^2 = 24.
    The ratio b^2/a^2 determines the asymptote slopes.
    """
    a_squared = hyperbola_a_squared  # a^2 = 20
    # From the original problem, b^2/a^2 = 24/20 = 6/5
    # So b^2 = a^2 * (6/5)
    b_squared = a_squared * 6 / 5  # b^2 = 24
    
    # The asymptotes have slopes ±b/a = ±sqrt(b^2/a^2) = ±sqrt(6/5)
    # For a rhombus with diagonals through origin and perpendicular:
    # Let BD have slope m, then AC has slope -1/m
    # Both lines must intersect the hyperbola (not be parallel to asymptotes)
    
    # For line y = mx to intersect the hyperbola x^2/a^2 - y^2/b^2 = 1:
    # x^2/a^2 - m^2*x^2/b^2 = 1
    # x^2 * (1/a^2 - m^2/b^2) = 1
    # x^2 * (b^2 - m^2*a^2)/(a^2*b^2) = 1
    # x^2 = a^2*b^2 / (b^2 - m^2*a^2)
    
    # For real intersection, we need b^2 - m^2*a^2 > 0, i.e., m^2 < b^2/a^2 = 6/5
    # Similarly for y = -x/m: need 1/m^2 < 6/5, i.e., m^2 > 5/6
    
    # So m^2 ∈ (5/6, 6/5)
    
    # For line y = mx:
    # x^2 = a^2*b^2 / (b^2 - m^2*a^2)
    # y^2 = m^2 * x^2
    # (BD/2)^2 = x^2 + y^2 = x^2(1 + m^2) = a^2*b^2*(1 + m^2) / (b^2 - m^2*a^2)
    
    # BD^2 = 4 * a^2*b^2*(1 + m^2) / (b^2 - m^2*a^2)
    
    # Let's substitute: let k = m^2, k ∈ (5/6, 6/5)
    # BD^2 = 4*a^2*b^2*(1 + k) / (b^2 - k*a^2)
    
    # To find the infimum, we analyze the function f(k) = (1 + k) / (b^2 - k*a^2)
    # f'(k) = [(b^2 - k*a^2) + a^2*(1 + k)] / (b^2 - k*a^2)^2
    #       = [b^2 - k*a^2 + a^2 + k*a^2] / (b^2 - k*a^2)^2
    #       = [b^2 + a^2] / (b^2 - k*a^2)^2 > 0
    
    # So f(k) is increasing in k. The infimum is at k → 5/6 (from above)
    
    # At k = 5/6:
    # BD^2 = 4*a^2*b^2*(1 + 5/6) / (b^2 - (5/6)*a^2)
    #      = 4*a^2*b^2*(11/6) / (b^2 - 5*a^2/6)
    
    k_limit = 5 / 6
    numerator = 4 * a_squared * b_squared * (1 + k_limit)
    denominator = b_squared - k_limit * a_squared
    
    # With a^2 = 20, b^2 = 24:
    # denominator = 24 - (5/6)*20 = 24 - 100/6 = 144/6 - 100/6 = 44/6 = 22/3
    # numerator = 4 * 20 * 24 * (11/6) = 4 * 20 * 24 * 11 / 6 = 4 * 20 * 4 * 11 = 3520
    # BD^2 = 3520 / (22/3) = 3520 * 3 / 22 = 10560 / 22 = 480
    
    result = numerator / denominator
    
    return round(result)


# Call the function with the given value
answer = solve(20)

# 调用 solve
result = solve(inputs['hyperbola_a_squared'])
print(result)