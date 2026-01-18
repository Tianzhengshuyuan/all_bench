inputs = {'S': 300}

def solve(S):
    M = 6000000
    count = 0
    for a in range(S + 1):
        rem = S - a
        for b in range(rem + 1):
            c = rem - b
            ab = a * b
            bc = b * c
            ca = c * a
            if S * (ab + bc + ca) - 3 * (ab * c) == M:
                count += 1
    return count

solve(300)

# 调用 solve
result = solve(inputs['S'])
print(result)