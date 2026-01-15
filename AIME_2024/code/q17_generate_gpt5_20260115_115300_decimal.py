inputs = {'surface_area': 94}

from fractions import Fraction
from decimal import Decimal, getcontext
import math

# 设置高精度
getcontext().prec = 50  # 50位精度

def solve(surface_area):
    V = 23  # fixed volume from the problem

    # Try to find rational positive roots of 2a^3 - S a + 4V = 0 using Rational Root Theorem
    roots = []
    S = surface_area

    def divisors(n):
        n = abs(int(n))
        ds = set()
        for i in range(1, int(n**0.5) + 1):
            if n % i == 0:
                ds.add(i)
                ds.add(n // i)
        return sorted(ds)

    if isinstance(S, int):
        A = 2
        C = -S
        D = 4 * V
        p_divs = divisors(D)
        q_divs = divisors(A)
        for p in p_divs:
            for q in q_divs:
                for sign in (-1, 1):
                    cand = Fraction(sign * p, q)
                    val = Fraction(A) * cand**3 + Fraction(C) * cand + Fraction(D)
                    if val == 0:
                        if cand > 0:
                            roots.append(cand)

        # deduplicate
        roots = sorted(set(roots))

    if roots:
        # 使用 Fraction 精确计算
        best_r2 = None
        for a in roots:
            d2 = 2 * (a * a) + (Fraction(V, 1) ** 2) / (a ** 4)
            r2 = d2 / 4
            if best_r2 is None or r2 > best_r2:
                best_r2 = r2
        return best_r2.numerator + best_r2.denominator
    else:
        # 使用 Decimal 进行高精度数值计算
        p = Decimal(-S) / Decimal(2)
        q = Decimal(2 * V)
        delta = (q / 2) ** 2 + (p / 3) ** 3

        def cbrt_decimal(x):
            if x == 0:
                return Decimal(0)
            sign = 1 if x > 0 else -1
            return sign * abs(x) ** (Decimal(1) / Decimal(3))

        real_roots = []
        if delta > 0:
            sqrt_delta = delta.sqrt()
            u = cbrt_decimal(-q / 2 + sqrt_delta)
            v = cbrt_decimal(-q / 2 - sqrt_delta)
            x = u + v
            if x > 0:
                real_roots.append(x)
        else:
            if p != 0:
                r = (-(p / 3) ** 3).sqrt()
                if r == 0:
                    x = cbrt_decimal(-q)
                    if x > 0:
                        real_roots.append(x)
                else:
                    # 使用 Decimal 计算三角函数（需要转换为 float 再转回）
                    arg_val = float(-q / (2 * r))
                    arg_val = max(-1.0, min(1.0, arg_val))
                    phi = Decimal(str(math.acos(arg_val)))
                    m = 2 * (-p / 3).sqrt()
                    for k in range(3):
                        cos_arg = float((phi + 2 * Decimal(str(math.pi)) * k) / 3)
                        x = m * Decimal(str(math.cos(cos_arg)))
                        if x > 0:
                            real_roots.append(x)
            else:
                x = cbrt_decimal(-q)
                if x > 0:
                    real_roots.append(x)

        # 去重（使用 Decimal 比较）
        uniq_roots = []
        for x in real_roots:
            if not any(abs(x - y) < Decimal('1e-20') for y in uniq_roots):
                uniq_roots.append(x)

        max_r2 = None
        for a in uniq_roots:
            a_sq = a * a
            a_4 = a_sq * a_sq
            d2 = 2 * a_sq + (Decimal(V * V)) / a_4
            r2 = d2 / 4
            if max_r2 is None or r2 > max_r2:
                max_r2 = r2

        if max_r2 is None:
            return None

        # 尝试将 Decimal 转换为 Fraction
        # 先尝试精确转换
        try:
            # 如果 r2 是有理数，可以直接转换
            frac_r2 = Fraction(str(max_r2))
        except:
            # 否则使用高精度近似
            frac_r2 = Fraction(str(max_r2)).limit_denominator(10**12)
        
        return frac_r2.numerator + frac_r2.denominator

solve(54)

# 调用 solve
result = solve(inputs['surface_area'])
print(result)

