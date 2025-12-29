inputs = {'b': 211}

def solve(b):
    import math

    def count_beautiful(base):
        cnt = 0
        for x in range(1, base):
            # y can be deduced from z=x+y and n=base*x+y=z^2
            # We just brute-force y as base is small enough (<= b)
            for y in range(base):
                n = base * x + y
                z = math.isqrt(n)
                if z * z == n and z == x + y:
                    cnt += 1
        return cnt

    # Precompute counts for all bases up to b
    counts = [0] * (b + 1)
    for t in range(2, b + 1):
        counts[t] = count_beautiful(t)

    cb = counts[b]

    # Find the smallest N such that the least base with more than N
    # b-eautiful integers equals b. This matches the intended "reorganized" target.
    # We search N from 0 up to cb-1 (since for N >= cb, b won't qualify).
    for N in range(cb):
        # find the least base with count > N among bases up to b
        least = None
        for t in range(2, b + 1):
            if counts[t] > N:
                least = t
                break
        if least == b:
            return N

    # If no such N exists, return -1 as a fallback
    return -1

solve(211)

# 调用 solve
result = solve(inputs['b'])
print(result)