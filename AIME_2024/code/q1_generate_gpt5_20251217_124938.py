inputs = {'denominator': 55}

def solve(denominator):
    from fractions import Fraction
    # Given system:
    # log2(x/(yz)) = 1/2
    # log2(y/(xz)) = 1/denominator
    # log2(z/(xy)) = 1/4
    #
    # Let a=log2(x), b=log2(y), c=log2(z)
    # Then:
    # a - b - c = s1
    # -a + b - c = s2
    # -a - b + c = s3
    # Solve:
    # a = -(s2 + s3)/2, b = -(s1 + s3)/2, c = -(s1 + s2)/2
    # Target: |4a + 3b + 2c|
    s1 = Fraction(1, 2)
    s2 = Fraction(1, denominator)
    s3 = Fraction(1, 4)

    a = -(s2 + s3) / 2
    b = -(s1 + s3) / 2
    c = -(s1 + s2) / 2

    value = abs(4 * a + 3 * b + 2 * c)  # This is |log2(x^4 y^3 z^2)|
    return value.numerator + value.denominator

# 调用 solve
result = solve(inputs['denominator'])
print(result)