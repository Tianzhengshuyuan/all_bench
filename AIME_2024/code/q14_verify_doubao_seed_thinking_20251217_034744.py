inputs = {'digit_count': 8}

inv_map = {1: 1, 2: 4, 3: 5, 4: 2, 5: 3, 6: 6}

def solve(digit_count):
    exponents = range(digit_count - 1, -1, -1)
    w = [(10 ** e) % 7 for e in exponents]
    inv_w = [inv_map[wk] for wk in w]
    candidates = []
    
    for C in range(7):
        digits = []
        for k in range(digit_count):
            y_k = (1 + C * inv_w[k]) % 7
            max_d = 9
            min_d = 1 if k == 0 else 0
            d = y_k
            while d + 7 <= max_d:
                d += 7
            digits.append(d)
        
        sum_mod = sum(digits[k] * w[k] for k in range(digit_count)) % 7
        if sum_mod == C:
            number = 0
            for d in digits:
                number = number * 10 + d
            candidates.append(number)
    
    max_num = max(candidates)
    print(f"max_num: {max_num}")
    Q = max_num // 1000
    R = max_num % 1000
    return Q + R

# 调用 solve
result = solve(inputs['digit_count'])
print(result)