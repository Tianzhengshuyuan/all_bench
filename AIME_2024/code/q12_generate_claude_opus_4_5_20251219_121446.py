inputs = {'target_sum_horizontal': 630}

from math import comb

def solve(target_sum_horizontal):
    # The grid is:
    # | a | b | c |
    # | d | e | f |
    
    # Reading left to right gives two numbers:
    # First row: 100a + 10b + c
    # Second row: 100d + 10e + f
    # Sum = target_sum_horizontal (999)
    
    # Reading top to bottom gives three numbers:
    # First column: 10a + d
    # Second column: 10b + e
    # Third column: 10c + f
    # Sum = 99 (this is fixed based on the problem)
    
    target_sum_vertical = 99
    
    # From the horizontal sum:
    # (100a + 10b + c) + (100d + 10e + f) = target_sum_horizontal
    # 100(a+d) + 10(b+e) + (c+f) = target_sum_horizontal
    
    # For target_sum_horizontal = 999:
    # Since each digit is 0-9, a+d, b+e, c+f are each at most 18
    # For the sum to be 999, we need:
    # c+f = 9 (no carry), b+e = 9 (no carry), a+d = 9 (no carry)
    
    # Let's verify this works for general target_sum_horizontal
    # We need 100(a+d) + 10(b+e) + (c+f) = target_sum_horizontal
    # where 0 <= a+d, b+e, c+f <= 18
    
    # For the vertical sum:
    # (10a + d) + (10b + e) + (10c + f) = 99
    # 10(a+b+c) + (d+e+f) = 99
    
    count = 0
    
    # Iterate over possible sums for each column pair
    for sum_ad in range(19):  # a+d can be 0 to 18
        for sum_be in range(19):  # b+e can be 0 to 18
            for sum_cf in range(19):  # c+f can be 0 to 18
                # Check horizontal constraint
                if 100 * sum_ad + 10 * sum_be + sum_cf != target_sum_horizontal:
                    continue
                
                # Now we need to count valid (a,b,c,d,e,f) where:
                # a+d = sum_ad, b+e = sum_be, c+f = sum_cf
                # and 10(a+b+c) + (d+e+f) = 99
                
                # From a+d = sum_ad, we have d = sum_ad - a
                # From b+e = sum_be, we have e = sum_be - b
                # From c+f = sum_cf, we have f = sum_cf - c
                
                # Substituting into vertical constraint:
                # 10(a+b+c) + (sum_ad - a + sum_be - b + sum_cf - c) = 99
                # 10(a+b+c) + sum_ad + sum_be + sum_cf - (a+b+c) = 99
                # 9(a+b+c) = 99 - sum_ad - sum_be - sum_cf
                
                rhs = target_sum_vertical - sum_ad - sum_be - sum_cf
                if rhs < 0 or rhs % 9 != 0:
                    continue
                
                sum_abc = rhs // 9
                
                # Now we need to count ways to choose a, b, c such that:
                # a + b + c = sum_abc
                # 0 <= a <= 9, 0 <= b <= 9, 0 <= c <= 9
                # 0 <= sum_ad - a <= 9, 0 <= sum_be - b <= 9, 0 <= sum_cf - c <= 9
                
                # For a: max(0, sum_ad - 9) <= a <= min(9, sum_ad)
                # For b: max(0, sum_be - 9) <= b <= min(9, sum_be)
                # For c: max(0, sum_cf - 9) <= c <= min(9, sum_cf)
                
                a_min = max(0, sum_ad - 9)
                a_max = min(9, sum_ad)
                b_min = max(0, sum_be - 9)
                b_max = min(9, sum_be)
                c_min = max(0, sum_cf - 9)
                c_max = min(9, sum_cf)
                
                # Count solutions to a + b + c = sum_abc with constraints
                for a in range(a_min, a_max + 1):
                    for b in range(b_min, b_max + 1):
                        c = sum_abc - a - b
                        if c_min <= c <= c_max:
                            count += 1
    
    return count

result = solve(999)

# 调用 solve
result = solve(inputs['target_sum_horizontal'])
print(result)