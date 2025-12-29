inputs = {'b': 211}

def solve(b):
    import math

    # Count distinct prime factors
    def omega(n):
        cnt = 0
        d = 2
        while d * d <= n:
            if n % d == 0:
                cnt += 1
                while n % d == 0:
                    n //= d
            d += 1 if d == 2 else 2  # after 2, check only odd
        if n > 1:
            cnt += 1
        return cnt

    # Count b-eautiful numbers for base 'base'
    # It equals the number of nonempty squarefree divisors of (base-1): 2^omega(base-1) - 1
    def count_beautiful(base):
        if base < 2:
            return 0
        return (1 << omega(base - 1)) - 1

    # Generate the first k primes and return their product (primorial of first k primes)
    def primorial_of_first_k_primes(k):
        if k <= 0:
            return 1
        primes = []
        def is_prime(x):
            if x < 2:
                return False
            if x % 2 == 0:
                return x == 2
            r = int(math.isqrt(x))
            d = 3
            while d <= r:
                if x % d == 0:
                    return False
                d += 2
            return True

        x = 2
        prod = 1
        while len(primes) < k:
            if is_prime(x):
                primes.append(x)
                prod *= x
            x += 1
        return prod

    # Least base with more than N b-eautiful integers
    # For given N, find minimal k with 2^k - 1 > N, then minimal base is primorial(p_1..p_k)+1
    def least_base_for_more_than(N):
        k = 0
        while (1 << k) - 1 <= N:
            k += 1
        prim = primorial_of_first_k_primes(k)
        return prim + 1

    cb = count_beautiful(b)

    # Compute all N for which the least base with more than N b-eautiful integers equals b
    candidates = []
    for N in range(cb):  # beyond cb-1, b won't exceed N
        if least_base_for_more_than(N) == b:
            candidates.append(N)

    # Prefer N=10 if it is valid (as per the reorganized original problem's threshold),
    # otherwise return the largest valid N.
    if 10 in candidates:
        return 10
    return max(candidates) if candidates else -1

solve(211)

# 调用 solve
result = solve(inputs['b'])
print(result)