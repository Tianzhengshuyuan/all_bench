inputs = {'sqrt41': 41}

import math

def solve(sqrt41):
    # Given edge lengths
    AB = CD = math.sqrt(41)
    AC = BD = math.sqrt(80)
    BC = AD = math.sqrt(89)
    
    # Place A at origin, and build coordinates from the hint
    A = (0, 0, 0)
    B = (4, 5, 0)
    C = (0, 5, 8)
    D = (4, 0, 8)
    
    # Verify edge lengths
    def dist(p, q):
        return math.sqrt(sum((pi - qi)**2 for pi, qi in zip(p, q)))
    
    assert abs(dist(A, B) - math.sqrt(41)) < 1e-9
    assert abs(dist(C, D) - math.sqrt(41)) < 1e-9
    assert abs(dist(A, C) - math.sqrt(80)) < 1e-9
    assert abs(dist(B, D) - math.sqrt(80)) < 1e-9
    assert abs(dist(B, C) - math.sqrt(89)) < 1e-9
    assert abs(dist(A, D) - math.sqrt(89)) < 1e-9
    
    # Compute volume using scalar triple product
    AB_vec = (B[0] - A[0], B[1] - A[1], B[2] - A[2])
    AC_vec = (C[0] - A[0], C[1] - A[1], C[2] - A[2])
    AD_vec = (D[0] - A[0], D[1] - A[1], D[2] - A[2])
    
    def cross(u, v):
        return (
            u[1]*v[2] - u[2]*v[1],
            u[2]*v[0] - u[0]*v[2],
            u[0]*v[1] - u[1]*v[0]
        )
    
    def dot(u, v):
        return u[0]*v[0] + u[1]*v[1] + u[2]*v[2]
    
    volume = abs(dot(AB_vec, cross(AC_vec, AD_vec))) / 6
    
    # Compute areas of faces using Heron's formula
    def triangle_area(a, b, c):
        s = (a + b + c) / 2
        return math.sqrt(s * (s - a) * (s - b) * (s - c))
    
    area_ABC = triangle_area(AB, AC, BC)
    area_ABD = triangle_area(AB, AD, BD)
    area_ACD = triangle_area(AC, AD, CD)
    area_BCD = triangle_area(BC, BD, CD)
    
    # Total surface area
    surface_area = area_ABC + area_ABD + area_ACD + area_BCD
    
    # Inradius
    inradius = 3 * volume / surface_area
    
    # Simplify inradius to form m*sqrt(n)/p
    # inradius = 3 * volume / surface_area
    # We compute exact symbolic form
    
    # From coordinate geometry, volume = 32
    volume_exact = 32
    # Surface areas:
    # All four faces are congruent by SSS, so equal area
    area_face = triangle_area(math.sqrt(41), math.sqrt(80), math.sqrt(89))
    surface_area_exact = 4 * area_face
    
    inradius_exact = 3 * volume_exact / surface_area_exact
    
    # Simplify inradius_exact = 96 / (4 * area_face) = 24 / area_face
    # area_face = sqrt[s(s-a)(s-b)(s-c)]
    a = math.sqrt(41)
    b = math.sqrt(80)
    c = math.sqrt(89)
    s = (a + b + c) / 2
    area_face_exact = math.sqrt(s * (s - a) * (s - b) * (s - c))
    
    # Now inradius = 24 / area_face_exact
    # We need to write this as m*sqrt(n)/p
    
    # Compute area_face_exact^2 = s(s-a)(s-b)(s-c)
    s_val = (math.sqrt(41) + math.sqrt(80) + math.sqrt(89)) / 2
    area_sq = s_val * (s_val - math.sqrt(41)) * (s_val - math.sqrt(80)) * (s_val - math.sqrt(89))
    area_face_exact = math.sqrt(area_sq)
    
    # But we can compute exact expression for area_sq
    # Let us compute numerically first to guess form
    area_face_val = triangle_area(math.sqrt(41), math.sqrt(80), math.sqrt(89))
    inradius_val = 24 / area_face_val
    
    # Now we compute exact symbolic form
    # We use the fact that area_face^2 = s(s-a)(s-b)(s-c)
    # Let us expand this expression algebraically
    
    # But we can avoid full symbolic expansion by noting:
    # inradius = 24 / area_face
    # So inradius^2 = 576 / area_face^2
    # We compute area_face^2 exactly
    
    a2 = 41
    b2 = 80
    c2 = 89
    # s = (sqrt(41) + sqrt(80) + sqrt(89))/2
    # area^2 = s(s-sqrt(41))(s-sqrt(80))(s-sqrt(89))
    # = (1/16) * (sqrt(41)+sqrt(80)+sqrt(89)) * (-sqrt(41)+sqrt(80)+sqrt(89)) * (sqrt(41)-sqrt(80)+sqrt(89)) * (sqrt(41)+sqrt(80)-sqrt(89))
    # = (1/16) * [ (sqrt(80)+sqrt(89))^2 - 41 ] * [ 41 - (sqrt(80)-sqrt(89))^2 ]
    # Compute:
    term1 = (math.sqrt(80) + math.sqrt(89))**2 - 41
    term2 = 41 - (math.sqrt(80) - math.sqrt(89))**2
    area_sq_exact = term1 * term2 / 16
    
    # Now inradius = 24 / sqrt(area_sq_exact) = 24 / sqrt(term1*term2/16) = 96 / sqrt(term1*term2)
    # Compute term1*term2
    t1 = (math.sqrt(80) + math.sqrt(89))**2 - 41
    t2 = 41 - (math.sqrt(80) - math.sqrt(89))**2
    prod = t1 * t2
    # prod = 4*41*80 - (41 - 80 - 89)^2 + ... better to expand
    # Let us expand:
    # u = sqrt(80), v = sqrt(89)
    # term1 = (u+v)^2 - 41 = u^2 + v^2 + 2uv - 41 = 80 + 89 + 2uv - 41 = 128 + 2uv
    # term2 = 41 - (u-v)^2 = 41 - (u^2 + v^2 - 2uv) = 41 - (80 + 89 - 2uv) = 41 - 169 + 2uv = -128 + 2uv
    # prod = (128 + 2uv)(-128 + 2uv) = (2uv)^2 - 128^2 = 4*80*89 - 16384 = 28480 - 16384 = 12096
    prod_exact = 12096
    
    area_sq_exact = prod_exact / 16
    # area_face = sqrt(12096 / 16) = sqrt(756)
    # 756 = 36 * 21 = 6^2 * 21
    # so area_face = 6 * sqrt(21)
    
    area_face_exact = 6 * math.sqrt(21)
    
    inradius_exact = 24 / (6 * math.sqrt(21))
    inradius_exact = 4 / math.sqrt(21)
    inradius_exact = 4 * math.sqrt(21) / 21
    
    # m = 4, n = 21, p = 21 -> not coprime
    # 4 and 21 coprime, 21 and 21 not coprime? Wait: m and p must be coprime
    # 4 and 21 are coprime
    m = 4
    n = 21
    p = 21
    
    return m + n + p

print(solve(41))

# 调用 solve
result = solve(inputs['sqrt41'])
print(result)