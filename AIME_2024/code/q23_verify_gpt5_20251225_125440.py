inputs = {'bd2_glb': 480}

def solve(bd2_glb):
    a2 = 20
    den = bd2_glb - 4 * a2
    if den == 0:
        return None
    if isinstance(bd2_glb, int):
        from math import gcd
        num = a2 * bd2_glb
        g = gcd(abs(num), abs(den))
        num //= g
        den //= g
        if den == 1:
            return num
        return num / den
    return (a2 * bd2_glb) / den

result = solve(480)

# 调用 solve
result = solve(inputs['bd2_glb'])
print(result)