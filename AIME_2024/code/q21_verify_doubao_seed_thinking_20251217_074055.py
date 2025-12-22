inputs = {'threshold': 10}

def solve(threshold):
    if threshold < 0:
        raise ValueError("Threshold must be non-negative")
    target = threshold + 1
    k = 1
    while (2 ** k) <= target:
        k += 1
    
    primes = []
    num = 2
    while len(primes) < k:
        is_prime = True
        for p in primes:
            if p * p > num:
                break
            if num % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
        num += 1
    
    product = 1
    for p in primes:
        product *= p
    
    return product + 1

# 调用 solve
result = solve(inputs['threshold'])
print(result)