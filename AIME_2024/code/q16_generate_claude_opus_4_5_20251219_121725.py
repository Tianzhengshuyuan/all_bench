inputs = {'exponent': 4}

def solve(exponent):
    def is_prime(n):
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    def find_least_prime(exp):
        # For n^exp + 1 to be divisible by p^2, we need:
        # 1. p | n^exp + 1, so n^exp ≡ -1 (mod p)
        # 2. This means n^(2*exp) ≡ 1 (mod p) but n^exp ≢ 1 (mod p)
        # So the order of n mod p divides 2*exp but not exp
        # This means the order is exactly 2*exp (or a divisor of 2*exp that doesn't divide exp)
        # By Fermat's Little Theorem, order divides p-1
        # So 2*exp | p-1, meaning p ≡ 1 (mod 2*exp)
        
        # For p^2 | n^exp + 1, we need the order of n mod p^2 to be 2*exp
        # This requires 2*exp | φ(p^2) = p(p-1)
        # Since p is odd prime and 2*exp is even, we need 2*exp | p-1
        
        p = 2
        while True:
            if is_prime(p):
                # Check if there exists n such that p^2 | n^exp + 1
                p_squared = p * p
                found = False
                for n in range(1, p_squared):
                    if pow(n, exp, p_squared) == p_squared - 1:
                        found = True
                        break
                if found:
                    return p
            p += 1
            if p > 10000:  # Safety limit
                break
        return None
    
    def find_least_m(p, exp):
        p_squared = p * p
        m = 1
        while True:
            if pow(m, exp, p_squared) == p_squared - 1:
                return m
            m += 1
            if m > 1000000:  # Safety limit
                break
        return None
    
    # Find the least prime p
    p = find_least_prime(exponent)
    
    # Find the least positive integer m
    m = find_least_m(p, exponent)
    
    return m

result = solve(4)

# 调用 solve
result = solve(inputs['exponent'])
print(result)