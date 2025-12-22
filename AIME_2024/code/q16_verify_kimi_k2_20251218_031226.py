inputs = {'n': 4}

def solve(n):
    # n is 4, but we use it generically for exponent in n^4+1
    # Step 1: find the least prime p such that p^2 divides m^n + 1 for some m
    # From theory: p must satisfy 2n | (p-1)  => 8 | (p-1)  => p ≡ 1 mod 8
    # So p is the least prime ≡1 mod 8, which is 17
    
    def is_prime(num):
        if num < 2:
            return False
        for d in range(2, int(num**0.5)+1):
            if num % d == 0:
                return False
        return True
    
    p = 17
    # Verify p=17 is the least such prime
    # We need to check that 17^2 divides m^4+1 for some m
    # We will find minimal m later
    
    # Step 2: find least m>0 such that p^2 | m^n + 1, i.e., 17^2 | m^4+1
    # We know from theory m mod 17 must be in {±2, ±8}
    candidates_mod = [2, 17-2, 8, 17-8]  # [2,15,8,9]
    
    best_m = None
    for r in candidates_mod:
        # We want m ≡ r mod 17, and m^4 ≡ -1 mod 17^2
        # Let m = 17*k + r, expand (17k+r)^4 mod 17^2
        # (17k+r)^4 ≡ r^4 + 4*r^3*(17k) mod 17^2
        # ≡ r^4 + 68*k*r^3 mod 289
        # We need this ≡ -1 mod 289
        # => r^4 + 68*k*r^3 ≡ -1 mod 289
        # => 68*k*r^3 ≡ -1 - r^4 mod 289
        # Solve for k mod 17 (since 68=4*17, and 289=17^2)
        # Divide equation by 17:
        # 4*k*r^3 ≡ (-1 - r^4)//17 mod 17
        # But we must be cautious: compute right-hand side modulo 17
        rhs = (-1 - pow(r,4,289)) % 289
        # We want 68*k*r^3 ≡ rhs mod 289
        # Let A = 68*r^3, B = rhs
        A = (68 * pow(r,3,289)) % 289
        B = rhs % 289
        # Solve A*k ≡ B mod 289
        # Use extended gcd
        def extended_gcd(a,b):
            if a==0:
                return (b,0,1)
            g,x1,y1 = extended_gcd(b%a, a)
            x = y1 - (b//a)*x1
            y = x1
            return (g,x,y)
        g, x, y = extended_gcd(A, 289)
        if B % g != 0:
            continue
        k0 = (x * (B//g)) % (289//g)
        # least k>=0
        k = k0 % (289//g)
        m = 17*k + r
        if best_m is None or m < best_m:
            best_m = m
    
    return best_m

# The variable n in the problem is 4, so we call solve(4)
# print(solve(4))  # -> 110

# 调用 solve
result = solve(inputs['n'])
print(result)