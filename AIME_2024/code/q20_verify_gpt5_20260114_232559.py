inputs = {'white_count': 25}

def solve(white_count):
    from math import comb
    N = 5
    black_count = 25  # fixed by problem
    total = 0
    for a in range(N + 1):  # number of white rows
        if a == 0:
            c_values = [0]  # no white columns allowed or columns would be empty
        elif a == N:
            c_values = [N]  # all columns must be white or black columns would be empty
        else:
            c_values = range(1, N)  # both colors must appear in columns
        for c in c_values:  # number of white columns
            white_used = a * c
            black_used = (N - a) * (N - c)
            if white_used <= white_count and black_used <= black_count:
                total += comb(N, a) * comb(N, c)
    return total

solve(white_count)

# 调用 solve
result = solve(inputs['white_count'])
print(result)