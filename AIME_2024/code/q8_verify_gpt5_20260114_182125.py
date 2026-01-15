inputs = {'total': 6000000}

def solve(total):
    S = 300
    if total % 3 != 0:
        return 0
    count = 0
    for a in range(S + 1):
        for b in range(S - a + 1):
            c = S - a - b
            ab = a * b
            bc = b * c
            ca = c * a
            s2 = ab + bc + ca
            s3 = ab * c
            if 300 * s2 - 3 * s3 == total:
                count += 1
    return count

solve(total)

# 调用 solve
result = solve(inputs['total'])
print(result)