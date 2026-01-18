inputs = {'side_CD': 240}

def solve(side_CD):
    a = 200
    b = 300
    c = side_CD
    return (a * b * c) / (a * b + b * c + c * a)

solve(240)

# 调用 solve
result = solve(inputs['side_CD'])
print(result)