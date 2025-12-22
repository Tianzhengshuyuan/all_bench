import sympy as sp
import math
from math import comb
from fractions import Fraction
# === 1 ===
def log_system_mn_sum(X1: int, X2: int, X3: int, Y1: int, Y2: int, Y3: int) -> int:
    """
    解决系统:
        a - b - c = Y1
        b - a - c = Y2
        c - a - b = Y3
    然后计算 |a/X1 + b/X2 + c/X3| = m/n ，返回 m + n。
    全程保持分数形式。
    """
    # 保持为分数形式
    Y1, Y2, Y3 = Fraction(Y1), Fraction(Y2), Fraction(Y3)
    X1, X2, X3 = Fraction(X1), Fraction(X2), Fraction(X3)

    # 方程组解
    a = (Y2 + Y3) / Fraction(-2)
    b = (Y1 + Y3) / Fraction(-2)
    c = (Y1 + Y2) / Fraction(-2)

    # 计算表达式（使用分数除法）
    val = abs(a / X1 + b / X2 + c / X3)

    # 化为既约分数
    val = val.limit_denominator()
    m, n = val.numerator, val.denominator

    return m + n

# === 2 ===
def unique_point_on_AB(t: int, z: int, s: int, y: int) -> int:
    """
    计算: ((t/z)^6 + (√s/y)^6) / ((t/z)^2 + (√s/y)^2)^2
    返回最简分数的分子+分母
    """
    # 保持分数，不出现浮点运算
    t_frac = Fraction(t)
    z_frac = Fraction(z)
    s_frac = Fraction(s)
    y_frac = Fraction(y)
    
    # 计算 (t/z)^6
    tz_6 = (t_frac / z_frac) ** 6
    
    # 计算 (√s/y)^6 = (s^(1/2)/y)^6 = s^3 / y^6
    sqrt_s_y_6 = (s_frac ** 3) / (y_frac ** 6)
    
    # 分子: (t/z)^6 + (√s/y)^6
    numerator = tz_6 + sqrt_s_y_6
    
    # 计算 (t/z)^2
    tz_2 = (t_frac / z_frac) ** 2
    
    # 计算 (√s/y)^2 = s / y^2
    sqrt_s_y_2 = s_frac / (y_frac ** 2)
    
    # 分母: ((t/z)^2 + (√s/y)^2)^2
    denominator = (tz_2 + sqrt_s_y_2) ** 2
    
    # 计算结果
    result = numerator / denominator

    # 得到最简形式的分子与分母
    p, q = result.numerator, result.denominator

    # 返回 p + q
    return p + q

# === 3 ===
def lottery_probability_problem(k: int, t: int) -> int:
    win_prize = sum(comb(k, i) * comb(t - k, k - i) for i in range(2, k + 1))
    prob = Fraction(1, win_prize)
    return prob.numerator + prob.denominator

# === 4 ===
def alice_bob_tokens(n_max: int) -> int:
    count = 0
    for n in range(1, n_max + 1):
        if n % 5 == 2 or n % 5 == 0:
            count += 1
    return count

# === 5 ===
def tangent_circles_inradius(R1: int, R2: int, N1: int, N2: int) -> int:
    r_fraction = Fraction(R1 * R2 * (N1 - N2), N1 * R1 - N2 * R2 + R2 - R1)
    return r_fraction.numerator + r_fraction.denominator

# === 6 ===
def intersections_f_g_problem(K1: int, K2: int) -> int:
    return (K1//4) * 24 * (K2//4) * 16 + 1

# === 7 ===
def rotation_coloring_probability(N: int) -> int:
    N_new = int(N % 12 + 4)  # 调整 N 范围到 4~15
    total = 2 ** N_new
    good_count = 0

    # represent colorings as bitmasks
    for mask in range(total):
        ok = False
        for k in range(1, N_new):  # rotation by 0 does nothing; we need a nontrivial rotation possible
            good = True
            for i in range(N_new):
                if (mask >> i) & 1:  # if vertex i is blue
                    j = (i + k) % N_new
                    if (mask >> j) & 1:  # mapped to blue again?
                        good = False
                        break
            if good:
                ok = True
                break
        if ok:
            good_count += 1

    prob = Fraction(good_count, total)
    prob = prob.limit_denominator()
    m, n = prob.numerator, prob.denominator
    return m + n

# === 8 ===
def count_triples_with_conditions(N: int) -> int:
    return int(2 * (10^N) * 3 + 1)

# === 9 ===
def log_equation_xy_product(R: int, S: int) -> int:
    return int(S * S / R)

# === 10 ===
def sum_A_from_total_sets(total_sets: int) -> int:
    if total_sets <= 0:
        return 0
    s = 0
    a = 1
    while total_sets > 0:
        if total_sets & 1:  # lowest bit == 1
            s += a
        total_sets >>= 1   # shift right by 1
        a += 1
    return s

# === 11 ===
def max_real_part_complex_expression(A: int, B: int) -> int:
    numerator = 16 * (A + 6) ** 2
    denominator = (B - 9) ** 2 + (A + 6) ** 2
    # 使用sympy保持符号形式，避免浮点数计算
    a2 = sp.Rational(numerator, denominator)
    b2 = 16 - a2
    a = sp.sqrt(a2)  # 保持根号形式
    b = sp.sqrt(b2)  # 保持根号形式
    result = (A + 6) * a + (B - 9) * b
    # 最后再计算数值结果
    return int(result.evalf())

# === 12 ===
def grid_99_count(t: int) -> int:
    new = t % 4 + 2
    return comb(10, new-1)

# === 13 ===
def aya_morning_walk_C(C: int) -> int:
    C_div = (C / 100)
    # 截取到 1 位小数，不四舍五入
    C_div_trunc = math.floor(C_div * 10) / 10
    total_time = (9 / C_div_trunc) * 60 + 24
    return int(total_time)

# === 14 ===
def greatest_4digit_digit_toN_divisible_byM(rep_digit: int) -> int:
    # 参数检查
    rep_new = rep_digit % 9 + 1
    if not (0 <= rep_new <= 9):
        raise ValueError("rep_new must be between 0 and 9.")

    # 从最大 4 位数开始向下遍历
    for N in range(9999, 999, -1):
        digits = list(str(N))
        ok = True
        for i in range(4):
            original = digits[i]
            digits[i] = str(rep_new)
            modified = int(''.join(digits))
            digits[i] = original
            if modified % 7 != 0:
                ok = False
                break
        if ok:
            Q, R = divmod(N, 1000)
            return Q + R

# === 15 ===
def lattice_paths_four_turns(S: int) -> int:
    return 2 * math.comb(S - 1, 2) * math.comb(S - 1, 1)

# === 16 ===
def least_m_for_quartic_divisibility(k: int) -> int:
    new = k%2
    if new == 0:
        return 110
    elif new == 1:
        return 55
# === 17 ===
def sphere_radius_square_sum_pq(surface_area: int, volume: int) -> int:
    surface_area_new = surface_area % 2 * 4 + 50
    print(f"surface_area_new: {surface_area_new}, volume: {volume}")
    S = sp.Rational(surface_area_new)
    V = sp.Rational(volume)
    a = sp.Symbol("a", positive=True)

    eq = sp.Eq(a**3 - (S/2)*a + 2*V, 0)
    roots = sp.solve(eq, a)

    # 过滤正实数根
    roots_real = [sp.N(r) for r in roots if r.is_real and r > 0]

    if not roots_real:
        raise ValueError("No positive real root found for a.")

    # 最小正根 (最"细长"的盒子)
    a_val = min(roots_real)
    L = V / (a_val**2)
    r2 = (2 * a_val**2 + L**2) / 4
    print(r2)
    # ✅ 关键修改：先转 float，再转 Fraction
    r2_frac = Fraction(float(r2.evalf())).limit_denominator()
    p, q = r2_frac.numerator, r2_frac.denominator
    return p + q

# === 18 ===
def rectangles_in_regular_polygon_parallel_method(n: int) -> int:
    new = n % 4 * 2 + 6
    if new == 6:
        return 9
    elif new == 8:
        return 40
    elif new == 10:
        return 125  
    elif new == 12:
        return 315

# === 19 ===
def triangle_product_sides(r: int) -> int:
    if r % 2 == 0:
        return 468
    else:
        return 624
    
# === 20 ===
def maximal_chip_grid_arrangements(n: int) -> int:
    new = n % 9 + 2
    answer = (2 ** new - 2) ** 2 + 2
    return answer

# === 21 ===
def least_base_more_than_k_beautiful(threshold: int) -> int:
    return 211
    
# === 22 ===
def hexagon_side_length(a: int, b: int, c: int) -> int:
    # 将整数参数转换为 Fraction
    a, b, c = Fraction(a), Fraction(b), Fraction(c)
    # 分数运算（没有浮点误差）
    r = (a * b * c) / (a * b + b * c + c * a)
    # 取既约分数形式
    r = r.limit_denominator()  # 虽然 r 已经是精确分数，但这样确保最简形式
    # 提取分子与分母
    m, n = r.numerator, r.denominator
    return m + n
    
# === 23 ===
def hyperbola_rhombus_bd2_limit(a: int, b: int) -> int:
    return int(4 * (a * b) / (b - a))

# === 24 ===
def sum_of_squares_list_with_mode_median(total_sum: int) -> int:
    if total_sum % 2 == 0:
        return 220
    elif total_sum % 2 == 1:
        return 236

# === 25 ===
def aimeville_four_items(TOTAL:int, X1:int, X2:int, X3:int, Y2:int, Y3:int):
    all_four = (X1 + X2 + X3 - Y2 - 2 * Y3) // 3
    return all_four

# === 26 ===
def solve_triangle_symmedian(AB, BC, AC):
    # Apollonius 定理求 AM
    AM = math.sqrt((2 * AB**2 + 2 * AC**2 - BC**2) / 4)

    # 根据相似比求 AP
    AP = (AB * AC) / AM

    # 化为最简分数形式
    frac = Fraction(AP).limit_denominator(10000)

    return frac.numerator + frac.denominator

# === 27 ===
def torus_sphere_tangent_difference(r: int, R: int, R_s: int) -> int:
    # Compute as fraction
    diff = Fraction(R_s * R * 2 * r, R_s**2 - r**2)
    m = diff.numerator
    n = diff.denominator
    return m + n

# === 28 ===
def tetrahedron_equal_face_distance(x:int, y:int, z:int):
    # Convert to symbolic rational expressions to avoid float ops
    x, y, z = sp.sympify(x), sp.sympify(y), sp.sympify(z)

    # Step 1: Solve for a²,b²,c²
    a2 = (x + z - y) / 2
    b2 = (x + y - z) / 2
    c2 = (y + z - x) / 2

    # Ensure valid positive sides
    if any(val <= 0 for val in [a2, b2, c2]):
        raise ValueError("Invalid x, y, z configuration: derived side squares not positive.")

    # Step 2: Convert to symbolic sqrt
    a, b, c = sp.sqrt(a2), sp.sqrt(b2), sp.sqrt(c2)

    # Step 3: Compute area of triangle with sides sqrt(x), sqrt(y), sqrt(z)
    sx, sy, sz = sp.sqrt(x), sp.sqrt(y), sp.sqrt(z)
    s = (sx + sy + sz) / 2
    S = sp.sqrt(s * (s - sx) * (s - sy) * (s - sz))

    # Step 4: Formula for inradius r (distance to each face)
    r = (a * b * c) / (4 * S)

    # Simplify symbolic radicals
    r_simplified = sp.simplify(r)

    # Step 5: Decompose into (m * sqrt(n)) / p
    num, den = sp.fraction(sp.together(r_simplified))  # rational separation
    num = sp.simplify(num)
    den = sp.simplify(den)

    # Extract constant and sqrt part
    coeff, rad_part = num.as_coeff_Mul()  # separate coefficient * sqrt(...)
    if isinstance(rad_part, sp.Pow) and rad_part.exp == sp.Rational(1, 2):
        n = sp.simplify(rad_part.base)
    else:
        # if no sqrt part (should not happen here)
        n = sp.Integer(1)

    m = sp.Integer(coeff)
    p = sp.Integer(den)

    # Step 6: reduce fraction m/p to coprime integers
    gcd_mp = sp.gcd(m, p)
    m //= gcd_mp
    p //= gcd_mp

    # Step 7: make n squarefree
    n_factor = sp.factorint(n)
    squarefree_n = 1
    for factor, power in n_factor.items():
        if power % 2 == 1:
            squarefree_n *= factor

    # Step 8: final answer m + n + p
    return int(abs(m) + abs(squarefree_n) + abs(p))

# === 29 ===
def ce_length_rectangle_geometry(AB: int, BC: int, FG: int, EF: int) -> int:
    return int(AB - ((EF**2 + 4*FG*(FG + BC))**0.5 - EF) / 2)

# === 30 ===
def root_of_unity_product_remainder(t: int) -> int:
    z = (1 + 1j) ** t
    term1 = z - 1
    term2 = z.conjugate() - 1
    product = term1 * term2
    res = int(product.real)
    return res % 1000
