inputs = {'axis_distance': 7}

def solve(axis_distance):
    from fractions import Fraction
    R = 11
    a = 3
    # Convert axis_distance to a Fraction safely
    try:
        D = Fraction(axis_distance)
    except TypeError:
        # For floats or other types, approximate rationally
        D = Fraction(axis_distance).limit_denominator()
    diff = Fraction(R * 2 * a, R * R - a * a) * D  # r_i - r_o
    return diff.numerator + diff.denominator

# 调用 solve
result = solve(inputs['axis_distance'])
print(result)