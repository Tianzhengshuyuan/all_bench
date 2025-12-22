inputs = {'threshold': 43}

def solve(threshold):
    def prime_factors(n):
        """Return list of distinct prime factors of n"""
        factors = []
        d = 2
        temp = n
        while d * d <= temp:
            if temp % d == 0:
                factors.append(d)
                while temp % d == 0:
                    temp //= d
            d += 1
        if temp > 1:
            factors.append(temp)
        return factors
    
    def count_b_beautiful(b):
        """Count the number of b-beautiful integers for a given base b"""
        count = 0
        # n has exactly two digits in base b: n = x*b + y where x in [1, b-1], y in [0, b-1]
        # The two digits sum to sqrt(n): x + y = sqrt(n)
        # So n = (x + y)^2 and n = x*b + y
        # Therefore (x + y)^2 = x*b + y
        
        for x in range(1, b):
            for y in range(0, b):
                s = x + y
                n = s * s
                if n == x * b + y:
                    count += 1
        return count
    
    def count_b_beautiful_fast(b):
        """
        Faster counting using the mathematical analysis:
        z(z-1) = (b-1)x where z = x + y
        z in {2, 3, ..., b-1}, x in {1, 2, ..., b-1}
        """
        b_prime = b - 1
        count = 0
        
        for z in range(2, b):
            # Check if z(z-1) is divisible by (b-1) and gives valid x
            product = z * (z - 1)
            if product % b_prime == 0:
                x = product // b_prime
                if 1 <= x <= b - 1:
                    y = z - x
                    if 0 <= y <= b - 1:
                        count += 1
        return count
    
    # We need to find the least b >= 2 such that count > threshold
    # Based on the solution, b' = b - 1 needs to have enough prime factors
    # The number of solutions is at most 2^n - 1 where n is the number of distinct prime factors
    # For more than 10 solutions, we need 2^n - 1 > 10, so n >= 4
    
    # Start searching from b = 2
    b = 2
    while True:
        count = count_b_beautiful_fast(b)
        if count > threshold:
            return b
        b += 1
        # Safety limit
        if b > 10000:
            break
    
    return -1

result = solve(10)

# 调用 solve
result = solve(inputs['threshold'])
print(result)