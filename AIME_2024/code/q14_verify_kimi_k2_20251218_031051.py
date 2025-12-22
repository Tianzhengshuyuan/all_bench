inputs = {'n': 1000}

def solve(n):
    # We are to find the greatest 4-digit number N such that
    # changing any one digit to 1 yields a multiple of 7.
    # Then compute Q + R where N = 1000*Q + R, 0 <= R < 1000.
    # Note: n is 1000, but we do not use it as a variable in the search.
    
    # Let N = 1000a + 100b + 10c + d, with a in [1,9], b,c,d in [0,9]
    # We require:
    #   1000 + 100b + 10c + d ≡ 0 mod 7
    #   1000a + 100 + 10c + d ≡ 0 mod 7
    #   1000a + 100b + 10 + d ≡ 0 mod 7
    #   1000a + 100b + 10c + 1 ≡ 0 mod 7
    #
    # Reduce coefficients mod 7:
    #   1000 ≡ 6, 100 ≡ 2, 10 ≡ 3
    #
    # So:
    #   6 + 2b + 3c + d ≡ 0 mod 7   ...(1)
    #   6a + 2 + 3c + d ≡ 0 mod 7 ...(2)
    #   6a + 2b + 3 + d ≡ 0 mod 7 ...(3)
    #   6a + 2b + 3c + 1 ≡ 0 mod 7 ...(4)
    
    # From (2)-(1): 6a + 2 + 3c + d - (6 + 2b + 3c + d) ≡ 0 => 6a - 2b - 4 ≡ 0 => 3a - b - 2 ≡ 0 => b ≡ 3a - 2 mod 7
    # From (3)-(2): 6a + 2b + 3 + d - (6a + 2 + 3c + d) ≡ 0 => 2b - 3c + 1 ≡ 0 => 2b - 3c ≡ -1 ≡ 6 mod 7
    # From (4)-(3): 6a + 2b + 3c + 1 - (6a + 2b + 3 + d) ≡ 0 => 3c - d - 2 ≡ 0 => 3c - d ≡ 2 mod 7
    # From (4)-(1): 6a + 2b + 3c + 1 - (6 + 2b + 3c + d) ≡ 0 => 6a - d - 5 ≡ 0 => 6a - d ≡ 5 mod 7
    
    best_N = 0
    # iterate a from 9 down to 1 to find the largest
    for a in range(9, 0, -1):
        b_mod = (3*a - 2) % 7
        # b must be in [0,9] and b ≡ b_mod mod 7
        # we want the largest possible b, so try b = 9,8,... down to 0
        for b in range(9, -1, -1):
            if b % 7 != b_mod:
                continue
            # 2b - 3c ≡ 6 mod 7  =>  3c ≡ 2b - 6 mod 7
            # multiply both sides by inv(3) mod 7 = 5
            rhs = (2*b - 6) % 7
            c_mod = (rhs * 5) % 7
            # c in [0,9], pick largest c satisfying c ≡ c_mod mod 7
            for c in range(9, -1, -1):
                if c % 7 != c_mod:
                    continue
                # 3c - d ≡ 2 mod 7  =>  d ≡ 3c - 2 mod 7
                d_mod = (3*c - 2) % 7
                # d in [0,9], pick largest d ≡ d_mod mod 7
                for d in range(9, -1, -1):
                    if d % 7 != d_mod:
                        continue
                    # Also check 6a - d ≡ 5 mod 7 (redundant due to derivation, but check anyway)
                    if (6*a - d) % 7 != 5:
                        continue
                    # Form N
                    N = 1000*a + 100*b + 10*c + d
                    # Verify all four change-to-1 conditions
                    ok = True
                    if (1000 + 100*b + 10*c + d) % 7 != 0:
                        ok = False
                    if (1000*a + 100 + 10*c + d) % 7 != 0:
                        ok = False
                    if (1000*a + 100*b + 10 + d) % 7 != 0:
                        ok = False
                    if (1000*a + 100*b + 10*c + 1) % 7 != 0:
                        ok = False
                    if ok:
                        if N > best_N:
                            best_N = N
                        # since we are iterating from largest digits, the first valid N for this a is the largest possible
                        # but we must continue to check if larger N exists with same a but larger b,c,d? 
                        # but we are already iterating b,c,d from high to low, so this N is the largest for this a.
                        # We can break inner loops and return after checking all a? 
                        # But we want the absolute largest, so we can break out of c and d loops and continue with smaller b? 
                        # Actually we want the largest N overall, so we can break out of d,c,b loops and continue to next a? 
                        # But we are already iterating from high to low, so we can break out of d,c,b loops and continue to next a.
                        # However, we must not return immediately, because a smaller a might give a larger N? 
                        # No: a is the thousands digit. We are iterating a from 9 down, so the first valid N we find is the largest possible.
                        # But we are inside 4 loops. We can break out and return.
                        # However, we must ensure we pick the largest N. Since we are going from high digits down, the first valid N is the largest.
                        # So we can return immediately.
                        Q = best_N // 1000
                        R = best_N % 1000
                        return Q + R
    # If not returned yet, no solution? but there is one.
    # In case we didn't break early, compute from best_N
    Q = best_N // 1000
    R = best_N % 1000
    return Q + R

# 调用 solve
result = solve(inputs['n'])
print(result)