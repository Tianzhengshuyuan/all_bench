inputs = {'n': 83}

import numpy as np

def solve(n):
    def f(x):
        return np.abs(np.abs(x) - 0.5)
    def g(x):
        return np.abs(np.abs(x) - 0.25)
    def h(x):
        return 4 * g(f(x))
    
    # number of sub-intervals for x in [0,1]
    # chosen so that sin(n*pi*x) changes slowly and h is sampled adequately
    M = 400000
    xs = np.linspace(0, 1, M+1)          # M+1 points
    F = np.empty(M+1, dtype=np.float64)
    
    for i, x in enumerate(xs):
        s = np.sin(np.pi * n * x)
        y = h(s)
        c = np.cos(3 * np.pi * y)
        F[i] = x - h(c)
    
    # count roots via sign changes / exact zeros
    count = 0
    for i in range(M):
        fi = F[i]
        if fi == 0:
            count += 1
        elif fi * F[i+1] < 0:
            count += 1
    # last point
    if abs(F[M]) < 1e-12:
        count += 1
    return count

# 调用 solve
result = solve(inputs['n'])
print(result)