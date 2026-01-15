inputs = {'abac': 468}

def solve(abac):
    r = 6
    R = abac / (6 * r)
    try:
        if abs(R - round(R)) < 1e-12:
            return int(round(R))
    except TypeError:
        pass
    return R

solve(468)

# 调用 solve
result = solve(inputs['abac'])
print(result)