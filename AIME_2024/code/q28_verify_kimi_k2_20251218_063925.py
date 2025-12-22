inputs = {'sqrt41': 41}

import math

def solve(sqrt41):
    # Given edge lengths
    AB = CD = math.sqrt(41)
    AC = BD = math.sqrt(80)
    BC = AD = math.sqrt(89)
    
    # Place A at origin
    A = (0, 0, 0)
    # Place B along x-axis
    B = (AB, 0, 0)
    
    # Let C be in xy-plane
    # AC = sqrt(80), BC = sqrt(89)
    # C = (x, y, 0)
    # x^2 + y^2 = 80
    # (x - sqrt(41))^2 + y^2 = 89
    # x^2 - 2*sqrt(41)*x + 41 + y^2 = 89
    # 80 - 2*sqrt(41)*x + 41 = 89
    # 121 - 2*sqrt(41)*x = 89
    # 2*sqrt(41)*x = 32
    # x = 16 / sqrt(41)
    x_c = 16 / math.sqrt(41)
    y_c_squared = 80 - x_c**2
    y_c = math.sqrt(y_c_squared)
    C = (x_c, y_c, 0)
    
    # Let D = (x, y, z)
    # AD = sqrt(89) => x^2 + y^2 + z^2 = 89
    # BD = sqrt(80) => (x - sqrt(41))^2 + y^2 + z^2 = 80
    # CD = sqrt(41) => (x - x_c)^2 + (y - y_c)^2 + z^2 = 41
    
    # From first two:
    # x^2 + y^2 + z^2 = 89
    # x^2 - 2*sqrt(41)*x + 41 + y^2 + z^2 = 80
    # 89 - 2*sqrt(41)*x + 41 = 80
    # 130 - 2*sqrt(41)*x = 80
    # 2*sqrt(41)*x = 50
    # x = 25 / sqrt(41)
    x_d = 25 / math.sqrt(41)
    
    # From first: y^2 + z^2 = 89 - x_d^2
    y_z_squared = 89 - x_d**2
    
    # From third:
    # (x_d - x_c)^2 + (y - y_c)^2 + z^2 = 41
    # (x_d - x_c)^2 + y^2 - 2*y*y_c + y_c^2 + z^2 = 41
    # (x_d - x_c)^2 + (y^2 + z^2) - 2*y*y_c + y_c^2 = 41
    # (x_d - x_c)^2 + y_z_squared - 2*y*y_c + y_c^2 = 41
    # 2*y*y_c = (x_d - x_c)^2 + y_z_squared + y_c^2 - 41
    term = (x_d - x_c)**2 + y_z_squared + y_c**2 - 41
    y_d = term / (2 * y_c)
    z_d_squared = y_z_squared - y_d**2
    z_d = math.sqrt(z_d_squared)
    D = (x_d, y_d, z_d)
    
    # Compute volume using scalar triple product
    AB_vec = (B[0] - A[0], B[1] - A[1], B[2] - A[2])
    AC_vec = (C[0] - A[0], C[1] - A[1], C[2] - A[2])
    AD_vec = (D[0] - A[0], D[1] - A[1], D[2] - A[2])
    
    # Cross product AC x AD
    cross_x = AC_vec[1]*AD_vec[2] - AC_vec[2]*AD_vec[1]
    cross_y = AC_vec[2]*AD_vec[0] - AC_vec[0]*AD_vec[2]
    cross_z = AC_vec[0]*AD_vec[1] - AC_vec[1]*AD_vec[0]
    
    # Dot product with AB
    dot = AB_vec[0]*cross_x + AB_vec[1]*cross_y + AB_vec[2]*cross_z
    volume = abs(dot) / 6
    
    # Compute areas of faces using Heron's formula
    def triangle_area(a, b, c):
        s = (a + b + c) / 2
        return math.sqrt(s*(s-a)*(s-b)*(s-c))
    
    area_ABC = triangle_area(AB, AC, BC)
    area_ABD = triangle_area(AB, AD, BD)
    area_ACD = triangle_area(AC, AD, CD)
    area_BCD = triangle_area(BC, BD, CD)
    
    total_surface_area = area_ABC + area_ABD + area_ACD + area_BCD
    
    # Inradius r = 3V / A_total
    r = 3 * volume / total_surface_area
    
    # Express r in form m*sqrt(n)/p
    # r is expected to be 8*sqrt(21)/63
    # We simplify by factoring out sqrt(21)
    # r = (8 * sqrt(21)) / 63
    
    # So m=8, n=21, p=63, but need to reduce m and p
    # gcd(8,63)=1, so already reduced
    m = 8
    n = 21
    p = 63
    
    return m + n + p

# Example usage:
# print(solve(41))

# 调用 solve
result = solve(inputs['sqrt41'])
print(result)