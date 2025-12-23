inputs = {'count': 3}

def solve(count):
    c = int(count)
    T = c + 1
    if T <= 0:
        return 2  # Any b >= 2 works; minimal is 2
    # Need smallest k with 2^k > T
    k = T.bit_length()
    # Smallest b' with at least k distinct primes is the product of first k primes
    prod = 1
    primes = []
    n = 2
    while len(primes) < k:
        isprime = True
        for p in primes:
            if p * p > n:
                break
            if n % p == 0:
                isprime = False
                break
        if isprime:
            primes.append(n)
            prod *= n
        n += 1
    return prod + 1

count = 10
solve(count)

# 调用 solve
result = solve(inputs['count'])
print(result)