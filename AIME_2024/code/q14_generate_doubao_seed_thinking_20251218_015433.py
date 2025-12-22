inputs = {'divide_by_value': 851}

def solve(divide_by_value):
    def largest_digit(r):
        return r + 7 if r + 7 <= 9 else r
    
    N = None
    for a in range(9, 0, -1):
        r_b = (3 * a + 5) % 7
        b = largest_digit(r_b)
        
        r_c = (3 * b + 5) % 7
        c = largest_digit(r_c)
        
        r_d = (3 * c - 2) % 7
        d = largest_digit(r_d)
        
        eq1_mod = (6 + 2 * b + 3 * c + d) % 7
        if eq1_mod == 0:
            N = 1000 * a + 100 * b + 10 * c + d
            break
    
    Q = N // divide_by_value
    R = N % divide_by_value
    return Q + R

# 调用 solve
result = solve(inputs['divide_by_value'])
print(result)