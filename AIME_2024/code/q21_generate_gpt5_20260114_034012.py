inputs = {'count_threshold': 25}

def solve(count_threshold):
    # Find minimal L such that 2^L - 1 > count_threshold
    L = 0
    while (1 << L) - 1 <= count_threshold:
        L += 1

    # Generate first L primes
    def first_k_primes(k):
        primes = []
        cand = 2
        while len(primes) < k:
            is_p = True
            for p in primes:
                if p * p > cand:
                    break
                if cand % p == 0:
                    is_p = False
                    break
            if is_p:
                primes.append(cand)
            cand += 1 if cand == 2 else 2  # after 2, test only odds
        return primes

    prod = 1
    for p in first_k_primes(L):
        prod *= p
    return prod + 1

solve(10)

# 调用 solve
result = solve(inputs['count_threshold'])
print(result)