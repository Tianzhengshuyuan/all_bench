inputs = {'K': 6058800}

def solve(K):
    S = 300
    count = 0
    for a in range(S + 1):
        for b in range(S - a + 1):
            c = S - a - b
            if a*a*(S - a) + b*b*(S - b) + c*c*(S - c) == K:
                count += 1
    return count

# 调用 solve
result = solve(inputs['K'])
print(result)