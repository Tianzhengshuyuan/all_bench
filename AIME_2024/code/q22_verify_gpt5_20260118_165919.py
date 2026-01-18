inputs = {'triangle_side_b': 240}

def solve(triangle_side_b):
    s1 = 200.0  # KL
    s3 = 300.0  # KM
    s2 = float(triangle_side_b)  # LM (variable)
    denom = 1.0 + s3 / s2 + s3 / s1
    x = s3 / denom
    # Return integer if it's effectively an integer
    xr = round(x)
    return int(xr) if abs(x - xr) < 1e-9 else x

# 调用 solve
result = solve(inputs['triangle_side_b'])
print(result)