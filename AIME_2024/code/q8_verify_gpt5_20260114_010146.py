inputs = {'S': 300}

def solve(S):
    K = 6000000
    count = 0
    for a in range(S + 1):
        for b in range(S - a + 1):
            c = S - a - b
            ab = a * b
            bc = b * c
            ca = c * a
            F = S * (ab + bc + ca) - 3 * a * b * c
            if F == K:
                count += 1
    return count

solve(300)

# 调用 solve
result = solve(inputs['S'])
print(result)