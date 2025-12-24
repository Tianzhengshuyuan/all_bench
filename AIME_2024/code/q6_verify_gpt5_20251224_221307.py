inputs = {'intersection_count': 385}

def solve(intersection_count):
    # Intersections follow: count = 128*N + 1 => N = (count - 1)/128
    n = intersection_count - 1
    if n % 128 != 0:
        from fractions import Fraction
        return Fraction(n, 128)
    return n // 128

intersection_count = 385
result = solve(intersection_count)

# 调用 solve
result = solve(inputs['intersection_count'])
print(result)