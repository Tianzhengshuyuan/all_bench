inputs = {'target_sum': 300}

def solve(target_sum):
    """
    Find the number of triples of nonnegative integers (a,b,c) satisfying:
    a + b + c = target_sum
    a^2*b + a^2*c + b^2*a + b^2*c + c^2*a + c^2*b = target_sum * (target_sum/3)^2 * 2/3 * 10
    
    Based on the solution approach:
    The expression simplifies to (a-100)(b-100)(c-100) = 0 when target_sum = 300
    More generally, with k = target_sum/3, we need (a-k)(b-k)(c-k) = 0
    """
    # The key insight from the solution:
    # a^2(b+c) + b^2(a+c) + c^2(a+b) = 6,000,000
    # With a+b+c = 300, this becomes:
    # 300(ab+bc+ca) - 3abc = 6,000,000
    # 100(ab+bc+ca) - abc = 2,000,000
    # (100-a)(100-b)(100-c) = 1,000,000 - 10000*300 + 100(ab+bc+ca) - abc = 0
    
    # For general target_sum, let k = target_sum/3
    # The second equation scales as (target_sum/300)^3 * 6,000,000
    # So we need (k-a)(k-b)(k-c) = 0
    
    k = target_sum // 3
    
    # The target value for the second equation
    # From the pattern: when target_sum = 300, target_expr = 6,000,000 = 2 * 100^3 * 3
    target_expr = 2 * k * k * k * 3
    
    count = 0
    
    # Iterate through all possible (a, b, c) with a + b + c = target_sum
    for a in range(target_sum + 1):
        for b in range(target_sum + 1 - a):
            c = target_sum - a - b
            # Check the second condition
            expr = a*a*b + a*a*c + b*b*a + b*b*c + c*c*a + c*c*b
            if expr == target_expr:
                count += 1
    
    return count


result = solve(300)

# 调用 solve
result = solve(inputs['target_sum'])
print(result)