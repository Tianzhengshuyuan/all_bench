inputs = {'divisor': 605}

def solve(divisor):
    # We need to find the greatest four-digit number N such that
    # changing any digit to 1 makes it divisible by divisor
    
    # Let N = 1000a + 100b + 10c + d
    # When we change digit a to 1: 1000 + 100b + 10c + d ≡ 0 (mod divisor)
    # When we change digit b to 1: 1000a + 100 + 10c + d ≡ 0 (mod divisor)
    # When we change digit c to 1: 1000a + 100b + 10 + d ≡ 0 (mod divisor)
    # When we change digit d to 1: 1000a + 100b + 10c + 1 ≡ 0 (mod divisor)
    
    # Search from largest to smallest four-digit number
    for N in range(9999, 999, -1):
        a = N // 1000
        b = (N // 100) % 10
        c = (N // 10) % 10
        d = N % 10
        
        # Check all four conditions
        # Change a to 1
        num1 = 1000 + 100*b + 10*c + d
        # Change b to 1
        num2 = 1000*a + 100 + 10*c + d
        # Change c to 1
        num3 = 1000*a + 100*b + 10 + d
        # Change d to 1
        num4 = 1000*a + 100*b + 10*c + 1
        
        if num1 % divisor == 0 and num2 % divisor == 0 and num3 % divisor == 0 and num4 % divisor == 0:
            # Found the greatest N
            Q = N // 1000
            R = N % 1000
            return Q + R
    
    return None

result = solve(7)

# 调用 solve
result = solve(inputs['divisor'])
print(result)