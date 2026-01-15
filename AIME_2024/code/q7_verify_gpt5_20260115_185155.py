from fractions import Fraction
inputs = {'P': Fraction(115, 256)}

from fractions import Fraction

def solve(P):
    def rotate_left(mask, r, N):
        if N == 0:
            return 0
        r %= N
        if r == 0:
            return mask & ((1 << N) - 1)
        return ((mask << r) | (mask >> (N - r))) & ((1 << N) - 1)

    def satisfies(mask, N):
        if mask == 0:
            return True
        for r in range(0, N // 2 + 1):
            if (mask & rotate_left(mask, r, N)) == 0:
                return True
        return False

    def probability(N):
        total = 1 << N
        count = 0
        for mask in range(total):
            if satisfies(mask, N):
                count += 1
        return Fraction(count, total)

    # Search for N such that probability equals P
    # Start with a modest upper bound and extend if needed
    for N in range(1, 21):
        if probability(N) == P:
            return N
    for N in range(21, 31):
        if probability(N) == P:
            return N
    return None

solve(Fraction(115, 256))

# 调用 solve
result = solve(inputs['P'])
print(result)