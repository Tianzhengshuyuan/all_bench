inputs = {'b': 368}

def solve(b):
    # We are to find the least b >= 2 such that there are more than ten b-eautiful integers.
    # From the analysis, we know that b' = b - 1 must have at least 4 distinct prime factors
    # to yield more than 10 solutions (since 2^4 = 16 > 10).
    # We are to return the least such b.
    
    # But the function is called with a specific b, and we are to return the answer to the problem.
    # The problem asks for the least b >= 2 with more than ten b-eautiful integers.
    # From the solution, that b is 211.
    
    # However, the function must be general and compute it.
    # So we implement the counting of b-eautiful numbers for increasing b until we find the first b with >10.
    
    def count_b_eautiful(b):
        if b < 2:
            return 0
        b_prime = b - 1
        # We need to count the number of z in [2, b_prime] such that:
        # z(z-1) is divisible by b_prime, and x = z(z-1)//b_prime satisfies 1 <= x <= b_prime
        # and also z = x + y with 0 <= y <= b-1, which is automatically satisfied if x <= b_prime and z <= b_prime
        count = 0
        for z in range(2, b_prime + 1):
            if (z * (z - 1)) % b_prime == 0:
                x = (z * (z - 1)) // b_prime
                if 1 <= x <= b_prime:
                    # y = z - x, must be in [0, b-1]
                    y = z - x
                    if 0 <= y <= b - 1:
                        count += 1
        return count
    
    # We now find the least b >= 2 such that count_b_eautiful(b) > 10
    b_test = 2
    while True:
        if count_b_eautiful(b_test) > 10:
            return b_test
        b_test += 1

# 调用 solve
result = solve(inputs['b'])
print(result)