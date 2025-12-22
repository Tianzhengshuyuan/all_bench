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
    
    # Compute area of each face using Heron's formula
    def triangle_area(a, b, c):
        s = (a + b + c) / 2
        return math.sqrt(s * (s - a) * (s - b) * (s - c))
    
    area_ABC = triangle_area(AB, AC, BC)
    area_ABD = triangle_area(AB, AD, BD)
    area_ACD = triangle_area(AC, AD, CD)
    area_BCD = triangle_area(BC, BD, CD)
    
    # Since all faces are congruent (SSS), areas should be equal
    surface_area = 4 * area_ABC
    
    # Inradius r = 3V / surface_area
    r = 3 * volume / surface_area
    
    # Express r in the form m√n / p
    # r = 3 * volume / (4 * area_ABC)
    # We need to simplify this expression
    
    # Let's compute volume and area_ABC exactly
    # Volume = |det| / 6
    det = dot(AB_vec, cross(AC_vec, AD_vec))
    # det = 4*(5*8 - 0*0) - 5*(0*8 - 0*4) + 0*(0*0 - 5*4) = 4*40 = 160
    volume_exact = 160 / 6
    
    # Area ABC: sides sqrt(41), sqrt(80), sqrt(89)
    a = math.sqrt(41)
    b = math.sqrt(80)
    c = math.sqrt(89)
    s = (a + b + c) / 2
    area_ABC_exact = math.sqrt(s * (s - a) * (s - b) * (s - c))
    
    # But we can compute area_ABC using cross product
    AB_vec = (4, 5, 0)
    AC_vec = (0, 5, 8)
    cross_ABC = cross(AB_vec, AC_vec)
    area_ABC_cross = math.sqrt(dot(cross_ABC, cross_ABC)) / 2
    
    # Use this exact area
    area_ABC_exact = area_ABC_cross
    
    surface_area_exact = 4 * area_ABC_exact
    r_exact = 3 * volume_exact / surface_area_exact
    
    # Simplify r_exact = (3 * 160 / 6) / (4 * area_ABC_exact) = 80 / (4 * area_ABC_exact) = 20 / area_ABC_exact
    # area_ABC_exact = |cross_ABC| / 2
    # cross_ABC = (5*8 - 0*5, 0*0 - 4*8, 4*5 - 5*0) = (40, -32, 20)
    # |cross_ABC| = sqrt(40^2 + 32^2 + 20^2) = sqrt(1600 + 1024 + 400) = sqrt(3024)
    # 3024 = 16 * 189 = 16 * 9 * 21 = 144 * 21
    # So |cross_ABC| = 12 * sqrt(21)
    # area_ABC_exact = 12 * sqrt(21) / 2 = 6 * sqrt(21)
    
    area_ABC_exact = 6 * math.sqrt(21)
    r_exact = 20 / area_ABC_exact
    r_exact = 20 / (6 * math.sqrt(21))
    r_exact = 10 / (3 * math.sqrt(21))
    r_exact = 10 * math.sqrt(21) / (3 * 21)
    r_exact = 10 * math.sqrt(21) / 63
    
    # r = 10√21 / 63
    m = 10
    n = 21
    p = 63
    # Simplify: gcd(10,63)=1, 21 square-free
    return m + n + p

print(solve(41))

# 调用 solve
result = solve(inputs['sqrt41'])
print(result)