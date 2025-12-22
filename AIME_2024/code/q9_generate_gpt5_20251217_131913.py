inputs = {'log_value': 87}

def solve(log_value):
    # From log_x(y^x) = L and log_y(x^{4y}) = L:
    # x*log_x(y) = L and 4y*log_y(x) = L
    # Using log_x(y) * log_y(x) = 1 => 4xy = L^2 => xy = L^2 / 4
    L = float(log_value)
    ans = (L * L) / 4.0
    # Return integer if it's effectively an integer
    if abs(ans - round(ans)) < 1e-12:
        return int(round(ans))
    return ans

# 调用 solve
result = solve(inputs['log_value'])
print(result)