inputs = {'count_threshold': 12}

def solve(count_threshold):
    t = int(count_threshold)
    if t < 0:
        return 2
    m = t + 1
    k = m.bit_length()
    s = 1
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
            s *= candidate
        candidate += 1 if candidate == 2 else 2
    return s + 1

solve(10)

# 调用 solve
result = solve(inputs['count_threshold'])
print(result)