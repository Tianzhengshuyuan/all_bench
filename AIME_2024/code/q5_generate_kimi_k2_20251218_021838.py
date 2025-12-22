inputs = {'large_radius': 638}

def solve(large_radius):
    # 设小圆半径为1，大圆半径为large_radius
    small_radius = 1
    
    # 根据题意，2024个小圆排成一排，总长度为 2*2022 + 1 + 1 + a + b = 4046 + a + b
    # 8个大圆排成一排，总长度为 6*2*large_radius + large_radius + large_radius + large_radius*a + large_radius*b
    # 即 12*large_radius + 2*large_radius + large_radius*(a + b) = 14*large_radius + large_radius*(a + b)
    
    # 由相似三角形，两种排列方式下，两端超出部分满足比例关系：
    # a + b (小圆情形) 与 large_radius*(a + b) (大圆情形) 对应，
    # 但更重要的是，整个底边长度相等：
    # 4046 + (a + b) = 14*large_radius + large_radius*(a + b)
    
    # 令 s = a + b，则
    # 4046 + s = 14*large_radius + large_radius * s
    # 4046 - 14*large_radius = s*(large_radius - 1)
    # s = (4046 - 14*large_radius) / (large_radius - 1)
    
    s = (4046 - 14 * large_radius) / (large_radius - 1)
    
    # 底边长度 BC = 4046 + s
    BC = 4046 + s
    
    # 由相似三角形，内切圆半径 r 满足：
    # 在小圆情形中，两端各伸出 x，则 BC = 2x + 4046
    # 同时，内切圆情形可看作“一个圆”排布，其伸出部分为 x_r，满足 BC = 2x_r + 0
    # 由相似比，x_r / x = r / small_radius
    # 但更简单的是：内切圆半径 r 满足 BC = 2 * x_r，且 x_r = r * (x / small_radius)
    # 但我们已有 x = s/2？不，我们直接用：
    # 由 Solution2 的思路：BC = 2x + 4046，且 x = s/2？不，s = a + b = 2x
    # 所以 x = s/2
    x = s / 2
    
    # 然后 r = 1 + 2023 / x
    r = 1 + 2023 / x
    
    # 化简为分数
    from fractions import Fraction
    r_frac = Fraction(r).limit_denominator()
    m, n = r_frac.numerator, r_frac.denominator
    return m + n

# 调用 solve
result = solve(inputs['large_radius'])
print(result)