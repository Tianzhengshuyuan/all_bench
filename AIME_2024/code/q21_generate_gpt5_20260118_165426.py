inputs = {'count_threshold': 14}

def solve(count_threshold):
    T = int(count_threshold)
    if T < 0:
        return 2

    k = (T + 1).bit_length()

    primes = []
    candidate = 2
    while len(primes) < k:
        is_prime = True
        for p in primes:
            if p * p > candidate:
                break
            if candidate % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 1 if candidate == 2 else 2

    prod = 1
    for p in primes:
        prod *= p

    return prod + 1

# 调用 solve
result = solve(inputs['count_threshold'])
print(result)