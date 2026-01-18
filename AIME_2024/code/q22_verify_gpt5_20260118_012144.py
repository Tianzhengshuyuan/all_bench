inputs = {'side_CD': 240}

def solve(side_CD):
    # Let KL=200, LM=side_CD, KM=300 be the sides of the reference triangle
    KL = 200
    KM = 300
    LM = side_CD
    # From similarity and segment addition: x = KM / (KM/LM + 1 + KM/KL)
    # Equivalent to: x = KM*KL*LM / (KM*KL + KL*LM + KM*LM)
    num = KM * KL * LM
    den = KM * KL + KL * LM + KM * LM
    return num // den if num % den == 0 else num / den

solve(240)

# 调用 solve
result = solve(inputs['side_CD'])
print(result)