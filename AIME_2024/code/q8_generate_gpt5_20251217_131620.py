inputs = {'sum_target': 300}

def solve(sum_target: int) -> int:
    # Derivation:
    # Given a + b + c = n and sum of symmetric terms S = a^2b + a^2c + b^2a + b^2c + c^2a + c^2b,
    # we have S = n(ab+bc+ca) - 3abc.
    # The condition S = 2n^3/9 is equivalent to (n/3 - a)(n/3 - b)(n/3 - c) = 0,
    # hence one of a, b, c equals n/3. For integer solutions, n must be divisible by 3.
    # Count triples with at least one variable equal to t = n/3:
    # Count = 3*(2t+1) - 3*1 + 1 = 6t + 1.
    if sum_target % 3 != 0:
        return 0
    t = sum_target // 3
    return 6 * t + 1

# 调用 solve
result = solve(inputs['sum_target'])
print(result)