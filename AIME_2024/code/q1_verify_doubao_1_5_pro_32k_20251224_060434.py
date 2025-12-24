inputs = {'m + n': 33}

def solve(m_plus_n):
    import sympy as sp
    a, b, c = sp.symbols('a b c')
    eq1 = sp.Eq(-a + b - c, sp.Rational(1, 3))
    eq2 = sp.Eq(-a - b + c, sp.Rational(1, 4))
    # 遍历可能的m和n组合
    for m in range(1, m_plus_n):
        n = m_plus_n - m
        if sp.gcd(m, n) == 1:
            eq3_pos = sp.Eq(4*a + 3*b + 2*c, sp.Rational(m, n))
            eq3_neg = sp.Eq(4*a + 3*b + 2*c, -sp.Rational(m, n))
            solutions_pos = sp.solve((eq1, eq2, eq3_pos), (a, b, c), dict=True)
            solutions_neg = sp.solve((eq1, eq2, eq3_neg), (a, b, c), dict=True)
            all_solutions = solutions_pos + solutions_neg
            for sol in all_solutions:
                m_check, n_check = sp.fraction(sp.simplify(sp.Abs(4*sol[a] + 3*sol[b] + 2*sol[c])))
                if m_check + n_check == m_plus_n:
                    result = sol[a] - sol[b] - sol[c]
                    return result


solve(33)


# 调用 solve
result = solve(inputs['m + n'])
print(result)