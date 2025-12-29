inputs = {'xy': 25}

import math

def solve(xy):
    # From N^2 = 4*xy, with x,y>1 => N>0
    return 2 * math.sqrt(xy)

solve(25)

# 调用 solve
result = solve(inputs['xy'])
print(result)