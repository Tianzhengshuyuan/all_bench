inputs = {'sqrt41': 41}

import math

def solve(sqrt41):
    # Given edge lengths
    AB = CD = math.sqrt(41)
    AC = BD = math.sqrt(80)
    BC = AD = math.sqrt(89)

    # Correct coordinates that satisfy all edge lengths
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

    # Compute area of face ABC using cross product
    cross_ABC = cross(AB_vec, AC_vec)
    area_ABC = math.sqrt(dot(cross_ABC, cross_ABC)) / 2

    # All faces congruent => total surface area
    surface_area = 4 * area_ABC

    # Inradius r = 3V / surface_area
    r = 3 * volume / surface_area

    # Express in form m√n / p
    # volume = 160 / 3
    # area_ABC = 6 * sqrt(21)
    # r = 20 * sqrt(21) / 63
    m = 20
    n = 21
    p = 63
    return m + n + p

print(solve(41))

# 调用 solve
result = solve(inputs['sqrt41'])
print(result)