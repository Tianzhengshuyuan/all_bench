inputs = {'unit_length': 1}

import sympy as sp
import math
from fractions import Fraction

def solve(unit_length):
    # AB 的方程: y = -sqrt(3) * x + sqrt(3)/2
    # 一般线段 PQ: P(a,0), Q(0,b), 满足 a^2 + b^2 = unit_length^2
    # PQ 的方程: x/a + y/b = 1  =>  b*x + a*y = a*b
    # 将 AB 的 y 代入 PQ 方程，求交点 x
    x, a = sp.symbols('x a', real=True)
    b = sp.sqrt(unit_length**2 - a**2)
    y_AB = -sp.sqrt(3) * x + sp.sqrt(3) / 2
    # 代入 PQ 方程: b*x + a*y_AB = a*b
    eq = b * x + a * y_AB - a * b
    # 解关于 x 的方程
    x_sol = sp.solve(eq, x)
    # 得到 x 关于 a 的表达式
    x_expr = x_sol[0]
    # 构造多项式方程: -a^4 + 2*x*a^3 + (-4*x^2 + 3*x + 1/4)*a^2 - 2*x*a + x^2 = 0
    poly = -a**4 + 2*x*a**3 + (-4*x**2 + 3*x + sp.Rational(1,4))*a**2 - 2*x*a + x**2
    # 因式分解或多项式除法，去掉 (a - 1/2)
    quotient = sp.div(poly, a - sp.Rational(1,2))[0]
    # 令 a = 1/2 代入 quotient = 0，解 x
    eq_x = quotient.subs(a, sp.Rational(1,2))
    x_vals = sp.solve(eq_x, x)
    # 选择 x = 1/8（排除 1/2）
    x_C = sp.Rational(1,8)
    y_C = -float(sp.sqrt(3)) * float(x_C) + float(sp.sqrt(3)) / 2
    # 计算 OC^2
    OC_squared = float(x_C)**2 + y_C**2
    # 返回最简分数形式的分子加分母
    frac = Fraction(OC_squared).limit_denominator()
    p, q = frac.numerator, frac.denominator
    return p + q

# 调用 solve
result = solve(inputs['unit_length'])
print(result)