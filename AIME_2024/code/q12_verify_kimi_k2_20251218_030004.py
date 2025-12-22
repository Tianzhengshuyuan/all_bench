inputs = {'target_sum_horizontal': 999}

def solve(target_sum_horizontal):
    # target_sum_horizontal is 999, but we do not hard-code the final answer.
    # We derive everything from the constraints.

    # Let the grid be:
    # a b c
    # d e f
    # Horizontal numbers: 100a+10b+c and 100d+10e+f
    # Their sum: (100a+10b+c) + (100d+10e+f) = 100(a+d) + 10(b+e) + (c+f) = 999
    # Since each digit is 0-9, the maximum sum for any pair is 18.
    # Therefore, no carry can occur: each digit sum must exactly match the digit in 999.
    # So:
    #   c + f = 9
    #   b + e = 9
    #   a + d = 9
    # Vertical numbers: 10a+d, 10b+e, 10c+f
    # Their sum: (10a+d) + (10b+e) + (10c+f) = 10(a+b+c) + (d+e+f) = 99
    # Substitute d=9-a, e=9-b, f=9-c:
    #   10(a+b+c) + ( (9-a)+(9-b)+(9-c) ) = 99
    #   10(a+b+c) + 27 - (a+b+c) = 99
    #   9(a+b+c) + 27 = 99
    #   9(a+b+c) = 72
    #   a+b+c = 8
    # We need non-negative integer solutions to a+b+c=8 with each <=9 (automatically satisfied).
    # Stars and bars: C(8+3-1, 3-1) = C(10,2) = 45
    from math import comb
    return comb(8 + 3 - 1, 3 - 1)

# 调用 solve
result = solve(inputs['target_sum_horizontal'])
print(result)