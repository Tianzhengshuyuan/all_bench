inputs = {'num_triples': 601}

def solve(num_triples):
    t = int(num_triples)
    d = t - 1
    q, r = divmod(d, 6)
    return q if r == 0 else d / 6

solve(601)

# 调用 solve
result = solve(inputs['num_triples'])
print(result)