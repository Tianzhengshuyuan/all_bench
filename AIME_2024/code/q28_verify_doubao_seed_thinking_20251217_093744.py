inputs = {'ac_bd_squared_length': 80}

import math

def prime_factors(n):
    factors = {}
    while n % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        n = n // 2
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors[i] = factors.get(i, 0) + 1
            n = n // i
        i += 2
    if n > 1:
        factors[n] = 1
    return factors

def solve(ac_bd_squared_length):
    x = 41  # AB² = CD²
    y = ac_bd_squared_length  # AC² = BD²
    z = 89  # BC² = AD²
    
    a_sq = (x + z - y) // 2
    b_sq = (x + y - z) // 2
    c_sq = (y + z - x) // 2
    
    a = math.isqrt(a_sq)
    b = math.isqrt(b_sq)
    c = math.isqrt(c_sq)
    
    abc = a * b * c
    term = a_sq * b_sq + a_sq * c_sq + b_sq * c_sq
    
    factors = prime_factors(term)
    k = 1
    n_val = 1
    for p, exp in factors.items():
        k *= p ** (exp // 2)
        n_val *= p ** (exp % 2)
    
    num = abc * k
    den = 2 * term
    gcd_val = math.gcd(num, den)
    
    m = num // gcd_val
    p_val = den // gcd_val
    
    return m + n_val + p_val

# 调用 solve
result = solve(inputs['ac_bd_squared_length'])
print(result)