inputs = {'n': 1000}

def solve(n):
    # We are to find the greatest 4-digit number N such that
    # changing any one of its digits to 1 yields a multiple of 7.
    # Then compute Q + R where N = 1000*Q + R, 0 ≤ R < 1000.
    # Note: n is passed as 1000, but we don't use it beyond understanding division by 1000.

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
    #   6 + 2b + 3c + d ≡ 0  (1)
    #   6a + 2 + 3c + d ≡ 0  (2)
    #   6a + 2b + 3 + d ≡ 0  (3)
    #   6a + 2b + 3c + 1 ≡ 0  (4)
    #
    # From (2)-(1): 6a - 2b - 4 ≡ 0  =>  3a - b ≡ 2 mod 7  =>  b ≡ 3a - 2 mod 7
    # From (3)-(2): 2b - 3c - 1 ≡ 0  =>  2b - 3c ≡ 1 mod 7
    # From (4)-(3): 3c - 2 ≡ 0       =>  3c ≡ 2 mod 7  =>  c ≡ 2 * inv(3,7) ≡ 2*5 ≡ 10 ≡ 3 mod 7
    # From (4)-(1): 6a - d - 5 ≡ 0  =>  6a - d ≡ 5  =>  d ≡ 6a - 5 mod 7
    #
    # So we have:
    #   c ≡ 3 mod 7  => c in {3, 10} but c digit => c=3 or c=10 invalid => c=3
    #   b ≡ 3a - 2 mod 7
    #   d ≡ 6a - 5 mod 7
    #
    # We want largest N => try a=9 down to 1, then b as large as possible, etc.

    # a from 9 down to 1
    for a in range(9, 0, -1):
        b_mod = (3*a - 2) % 7
        # b must be ≡ b_mod mod 7, and 0≤b≤9
        # we want largest b => start from 9 down
        for b in range(9, -1, -1):
            if b % 7 != b_mod:
                continue
            # c can be 3 or 10, but 10 invalid => c=3 or c=10 invalid => c=3
            # But wait: c ≡ 3 mod 7 => c in {3, 10} => only c=3 valid
            c = 3
            d_mod = (6*a - 5) % 7
            # d ≡ d_mod mod 7, 0≤d≤9
            for d in range(9, -1, -1):
                if d % 7 != d_mod:
                    continue
                # Form N
                N = 1000*a + 100*b + 10*c + d
                # Check all four conditions by changing each digit to 1
                # Change a to 1: 1000*1 + 100b + 10c + d
                t1 = 1000 + 100*b + 10*c + d
                # Change b to 1: 1000a + 100*1 + 10c + d
                t2 = 1000*a + 100 + 10*c + d
                # Change c to 1: 1000a + 100b + 10*1 + d
                t3 = 1000*a + 100*b + 10 + d
                # Change d to 1: 1000a + 100b + 10c + 1
                t4 = 1000*a + 100*b + 10*c + 1
                if t1 % 7 == 0 and t2 % 7 == 0 and t3 % 7 == 0 and t4 % 7 == 0:
                    # This is valid. Since we try a descending, b descending, d descending, first valid is largest.
                    Q = N // 1000
                    R = N % 1000
                    return Q + R
    # If none found (should not happen), return 0
    return 0

# 调用 solve
result = solve(inputs['n'])
print(result)