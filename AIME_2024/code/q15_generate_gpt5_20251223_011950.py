inputs = {'turns': 6}

def solve(turns):
    def C(n, k):
        if k < 0 or k > n:
            return 0
        k = min(k, n - k)
        if k == 0:
            return 1
        num = 1
        den = 1
        for i in range(1, k + 1):
            num *= n - k + i
            den *= i
        return num // den

    def compositions_count(total, parts):
        if parts < 1 or parts > total:
            return 0
        return C(total - 1, parts - 1)

    N = 8  # steps right and up each
    k_first = (turns + 2) // 2
    k_other = (turns + 1) - k_first

    ways_start_R = compositions_count(N, k_first) * compositions_count(N, k_other)
    ways_start_U = compositions_count(N, k_other) * compositions_count(N, k_first)

    return ways_start_R + ways_start_U

solve(4)

# 调用 solve
result = solve(inputs['turns'])
print(result)