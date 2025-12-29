inputs = {'prize_prob_denominator': 115}

def solve(prize_prob_denominator):
    from math import comb
    counts = [comb(4, k) * comb(6, 4 - k) for k in range(5)]
    for N in range(0, 5):
        denom = sum(counts[k] for k in range(N, 5))
        if denom == prize_prob_denominator:
            return N
    return -1

solve(globals().get('prize_prob_denominator', 115))

# 调用 solve
result = solve(inputs['prize_prob_denominator'])
print(result)