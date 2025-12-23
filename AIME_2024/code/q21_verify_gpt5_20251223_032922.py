inputs = {'count': 10}

def solve(count):
    c = int(count)
    T = c + 1
    if T <= 0:
        k = 0
    else:
        k = T.bit_length()  # minimal k such that 2^k > T
    prod = 1
    if k > 0:
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

solve(count)

# 调用 solve
result = solve(inputs['count'])
print(result)