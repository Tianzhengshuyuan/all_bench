inputs = {'r': '\\frac{20\\sqrt{21}}{63}'}

def solve(r):
    import math
    import re
    from fractions import Fraction

    def parse_t2(val):
        # returns r^2 as float, parsing LaTeX like \frac{20\sqrt{21}}{63}
        if isinstance(val, (int, float)):
            v = float(val)
            return v * v
        if not isinstance(val, str):
            v = float(val)
            return v * v

        s = val.strip()
        if len(s) >= 2 and s[0] == '$' and s[-1] == '$':
            s = s[1:-1]
        s = s.replace(' ', '')

        def extract_braced(text, i):
            if i < 0 or i >= len(text) or text[i] != '{':
                return None, i
            depth = 1
            j = i + 1
            start = j
            while j < len(text) and depth > 0:
                if text[j] == '{':
                    depth += 1
                elif text[j] == '}':
                    depth -= 1
                j += 1
            if depth != 0:
                return None, j
            return text[start:j - 1], j

        def num_sq_from_str(snum):
            m = re.fullmatch(r'([+-]?\d+)?\\sqrt\{([+-]?\d+)\}', snum)
            if m:
                coef_str, rad_str = m.group(1), m.group(2)
                coef = int(coef_str) if coef_str not in (None, '') else 1
                rad = int(rad_str)
                return Fraction(coef * coef * rad, 1)
            if snum.startswith('\\sqrt'):
                idx = snum.find('{')
                if idx != -1:
                    inside, _ = extract_braced(snum, idx)
                    if inside is not None:
                        try:
                            rad = int(inside)
                            return Fraction(rad, 1)
                        except:
                            pass
            try:
                f = Fraction(snum)
                return f * f
            except:
                try:
                    f = Fraction.from_float(float(snum)).limit_denominator()
                    return f * f
                except:
                    return None

        if s.startswith('\\frac'):
            i = s.find('{', 5)
            if i != -1:
                num_str, pos = extract_braced(s, i)
                if num_str is not None:
                    j = s.find('{', pos)
                    if j != -1:
                        den_str, _ = extract_braced(s, j)
                        if den_str is not None:
                            num_sq = num_sq_from_str(num_str)
                            try:
                                den_val = Fraction(den_str)
                            except:
                                try:
                                    den_val = Fraction.from_float(float(den_str)).limit_denominator()
                                except:
                                    den_val = None
                            if num_sq is not None and den_val is not None and den_val != 0:
                                t2_frac = num_sq / (den_val * den_val)
                                return float(t2_frac)

        m2 = re.fullmatch(r'([+-]?\d+)?\\sqrt\{([+-]?\d+)\}', s)
        if m2:
            coef = int(m2.group(1)) if m2.group(1) not in (None, '') else 1
            rad = int(m2.group(2))
            return float(Fraction(coef * coef * rad, 1))

        try:
            v = float(s)
            return v * v
        except:
            expr = s.replace('\\sqrt', 'sqrt').replace('{', '(').replace('}', ')')
            expr = re.sub(r'(\d)(\()', r'\1*\2', expr)
            expr = re.sub(r'(\d)(sqrt)', r'\1*\2', expr)
            expr = re.sub(r'(\))(\d)', r'\1*\2', expr)
            try:
                from math import sqrt
                v = eval(expr, {"__builtins__": {}}, {"sqrt": sqrt})
                return float(v) * float(v)
            except:
                return float('nan')

    t2 = parse_t2(r)

    def poly(N):
        # 8*t2*(-N^2 + 338N - 81) - (N^2 - 81)(169 - N) = 0
        Nf = float(N)
        return 8.0 * t2 * (-Nf * Nf + 338.0 * Nf - 81.0) - ((Nf * Nf - 81.0) * (169.0 - Nf))

    a, b = 9.0 + 1e-8, 169.0 - 1e-8

    steps = 20000
    dx = (b - a) / steps
    roots = []
    prev_x = a
    prev_f = poly(prev_x)
    for i in range(1, steps + 1):
        x = a + i * dx
        fx = poly(x)
        if math.isfinite(prev_f) and math.isfinite(fx):
            if abs(fx) < 1e-14:
                roots.append(x)
            elif prev_f * fx < 0:
                left, right = prev_x, x
                fl, fr = prev_f, fx
                for _ in range(100):
                    mid = (left + right) / 2.0
                    fm = poly(mid)
                    if abs(fm) < 1e-16:
                        left = right = mid
                        break
                    if fl * fm <= 0:
                        right = mid
                        fr = fm
                    else:
                        left = mid
                        fl = fm
                roots.append((left + right) / 2.0)
        prev_x, prev_f = x, fx

    uniq = []
    for rt in roots:
        if all(abs(rt - u) > 1e-7 for u in uniq):
            uniq.append(rt)

    if not uniq:
        # fallback Newton guesses
        for guess in (41.0, 120.0, 100.0):
            x = guess
            for _ in range(80):
                f = poly(x)
                h = 1e-6
                df = (poly(x + h) - poly(x - h)) / (2 * h)
                if not math.isfinite(df) or abs(df) < 1e-18:
                    break
                x_new = x - f / df
                if not (a <= x_new <= b):
                    break
                if abs(x_new - x) < 1e-14:
                    x = x_new
                    break
                x = x_new
            if a <= x <= b and abs(poly(x)) < 1e-10:
                uniq.append(x)
                break

    if not uniq:
        return None

    candidates = [rt for rt in uniq if 9.0 <= rt <= 169.0] or uniq
    best = min(candidates, key=lambda v: (abs(v - round(v)), v))
    best_int = int(round(best))
    if abs(best - best_int) < 1e-6:
        return best_int
    return best

try:
    solve(r)
except NameError:
    pass

# 调用 solve
result = solve(inputs['r'])
print(result)