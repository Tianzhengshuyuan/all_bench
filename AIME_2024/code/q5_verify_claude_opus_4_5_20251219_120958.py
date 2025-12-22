inputs = {'large_circle_radius': 34}

from fractions import Fraction

def solve(large_circle_radius):
    """
    Solve the problem of finding the inradius of triangle ABC.
    
    Given:
    - 8 circles of radius large_circle_radius (34) are sequentially tangent
    - 2024 circles of radius 1 can be arranged in the same manner
    - Two circles are tangent to AB and BC of triangle ABC respectively
    
    The key insight is that the configurations are similar, and we can use
    the similarity ratio to find the inradius.
    """
    r1 = large_circle_radius  # radius of large circles = 34
    r2 = 1  # radius of small circles
    n1 = 8  # number of large circles
    n2 = 2024  # number of small circles
    
    # For n circles of radius r arranged sequentially tangent between two sides
    # of a triangle, the length along the base BC consists of:
    # - The distance from B to the first tangent point: x (for small circles)
    # - The diameters of the middle circles: 2*r*(n-2)
    # - The two end circles contribute their radii: 2*r
    # - The distance from the last tangent point to C: same as x by symmetry (isosceles)
    
    # For small circles (radius 1, count 2024):
    # BC = 2*x + 2*1*(2024-2) + 2*1 = 2*x + 2*2022 + 2 = 2*x + 4046
    
    # For large circles (radius 34, count 8):
    # By similarity, the distance from B to first tangent point is 34*x
    # BC = 2*(34*x) + 2*34*(8-2) + 2*34 = 68*x + 2*34*6 + 68 = 68*x + 408 + 68 = 68*x + 476
    
    # Setting equal:
    # 2*x + 4046 = 68*x + 476
    # 4046 - 476 = 68*x - 2*x
    # 3570 = 66*x
    # x = 3570/66 = 595/11
    
    # The length along BC for small circles:
    # BC = 2*x + 2*r2*(n2-2) + 2*r2 = 2*x + 2*(n2-1)
    small_circle_contribution = 2 * r2 * (n2 - 2) + 2 * r2  # = 2*(n2-1) = 4046
    
    # The length along BC for large circles:
    # BC = 2*(r1*x) + 2*r1*(n1-2) + 2*r1 = 2*r1*x + 2*r1*(n1-1)
    large_circle_contribution = 2 * r1 * (n1 - 2) + 2 * r1  # = 2*r1*(n1-1) = 476
    
    # From similarity: 2*x + small_circle_contribution = 2*r1*x + large_circle_contribution
    # 2*x + 4046 = 68*x + 476
    # 4046 - 476 = (2*r1 - 2)*x
    # x = (4046 - 476) / (2*r1 - 2)
    
    x = Fraction(small_circle_contribution - large_circle_contribution, 2 * r1 - 2)
    
    # For the incircle with radius r, it's like having 1 circle of radius r
    # The formula becomes: BC = 2*r*x (since there's just one circle, no middle part)
    # But we also have BC = 2*x + 4046
    # So: 2*r*x = 2*x + 4046
    # r*x = x + 2023
    # r = 1 + 2023/x
    
    # With n2 = 2024 small circles of radius 1:
    # The contribution is 2*1*(2024-1) = 4046, so 2023 = (n2-1)*r2
    
    inradius = 1 + Fraction((n2 - 1) * r2, x)
    
    # Simplify and get m + n
    m = inradius.numerator
    n = inradius.denominator
    
    return m + n

result = solve(34)

# 调用 solve
result = solve(inputs['large_circle_radius'])
print(result)