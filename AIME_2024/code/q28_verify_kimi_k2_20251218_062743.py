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
        return math.sqrt(sum((p[i]-q[i])**2 for i in range(3)))
    
    assert abs(dist(A, B) - math.sqrt(41)) < 1e-9
    assert abs(dist(C, D) - math.sqrt(41)) < 1e-9
    assert abs(dist(A, C) - math.sqrt(80)) < 1e-9
    assert abs(dist(B, D) - math.sqrt(80)) < 1e-9
    assert abs(dist(B, C) - math.sqrt(89)) < 1e-9
    assert abs(dist(A, D) - math.sqrt(89)) < 1e-9
    
    # Volume via scalar triple product
    AB_vec = (B[0]-A[0], B[1]-A[1], B[2]-A[2])
    AC_vec = (C[0]-A[0], C[1]-A[1], C[2]-A[2])
    AD_vec = (D[0]-A[0], D[1]-A[1], D[2]-A[2])
    
    def cross(u, v):
        return (u[1]*v[2] - u[2]*v[1],
                u[2]*v[0] - u[0]*v[2],
                u[0]*v[1] - u[1]*v[0])
    
    def dot(u, v):
        return u[0]*v[0] + u[1]*v[1] + u[2]*v[2]
    
    cross_AC_AD = cross(AC_vec, AD_vec)
    volume = abs(dot(AB_vec, cross_AC_AD)) / 6
    
    # Area of face BCD
    BC_vec = (C[0]-B[0], C[1]-B[1], C[2]-B[2])
    BD_vec = (D[0]-B[0], D[1]-B[1], D[2]-B[2])
    cross_BC_BD = cross(BC_vec, BD_vec)
    area_BCD = math.sqrt(dot(cross_BC_BD, cross_BC_BD)) / 2
    
    # All four faces congruent => same area
    face_area = area_BCD
    
    # Inradius r = 3V / surface_area
    surface_area = 4 * face_area
    r = 3 * volume / surface_area
    
    # Express r in form m sqrt(n) / p
    # r = 3V / (4 * area) = 3 * (80 sqrt(21)/63) / (4 * (sqrt(21)*sqrt(21*89)/2)) simplifies to 80 sqrt(21) / (63 * sqrt(89))
    # But we need to rationalize and simplify to lowest terms
    
    # Recompute exactly
    # Volume = 80 sqrt(21) / 63
    vol_num = 80
    vol_den = 63
    vol_sqrt = 21
    
    # Area = sqrt(21 * 89) / 2 * sqrt(21) = sqrt(21) * sqrt(89) * sqrt(21) / 2 = 21 sqrt(89) / 2
    area_num = 21
    area_den = 2
    area_sqrt = 89
    
    # r = 3 * (80 sqrt(21)/63) / (4 * (21 sqrt(89)/2))
    #   = (240 sqrt(21) / 63) / (84 sqrt(89) / 2)
    #   = (240 sqrt(21) / 63) * (2 / (84 sqrt(89)))
    #   = 480 sqrt(21) / (63 * 84 sqrt(89))
    #   = 480 sqrt(21) sqrt(89) / (63 * 84 * 89)
    #   = 480 sqrt(1869) / (5292 * 89)
    #   = 480 sqrt(1869) / 471108
    #   = 40 sqrt(1869) / 39259
    
    # But 1869 = 21 * 89 = 3 * 7 * 89 => square-free
    # gcd(40, 39259) = 1
    
    m = 40
    n = 1869
    p = 39259
    
    return m + n + p

print(solve(41))

# 调用 solve
result = solve(inputs['sqrt41'])
print(result)