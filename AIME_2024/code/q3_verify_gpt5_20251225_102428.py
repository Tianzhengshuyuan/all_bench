inputs = {'prize_prob_denominator': 115}

def solve(prize_prob_denominator):
    from math import comb
    # counts for matches k = 0..4
    counts = [comb(4, k) * comb(6, 4 - k) for k in range(5)]
    # Try N from 0 to 4 (allowing the edge case N=0 -> denominator 210)
    for N in range(0, 5):
        denom = sum(counts[k] for k in range(N, 5))
        if denom == prize_prob_denominator:
            return N
    return -1

solve(prize_prob_denominator)

# 调用 solve
result = solve(inputs['prize_prob_denominator'])
print(result)