inputs = {'side_length_1': 200}

def solve(side_length_1):
    # The triangle has sides 200, 240, 300
    # side_length_1 = 200, and the other sides are 240 and 300
    # The ratio between sides is 200:240:300 = 10:12:15
    
    # Let's denote the three sides of the outer triangle
    # KL = 200, KM = 300, ML = 240 (based on the solution)
    # The sides are in ratio, so we need to figure out which is which
    
    # Given side_length_1 = 200, the original sides are 200, 240, 300
    # The ratio is 200:240:300 = 10:12:15
    
    # From the solution:
    # KL = 200, KM = 300, ML = 240
    # So the sides are assigned as: smallest = 200, middle = 240, largest = 300
    
    # The ratios used in the solution:
    # KL/KM = 200/300 = 2/3
    # LM/KM = 240/300 = 4/5
    
    # Let's work with the general case where side_length_1 corresponds to 200
    # The other sides scale proportionally: 240 = 200 * 1.2, 300 = 200 * 1.5
    
    KL = side_length_1  # 200
    ML = side_length_1 * 1.2  # 240
    KM = side_length_1 * 1.5  # 300
    
    # From the solution:
    # FM = (KL/KM) * x reciprocal... let me re-read
    # Triangle MEF ~ MLK, so EF/KL = FM/KM
    # x/200 = FM/300 => FM = 300 * x / 200 = 3x/2
    
    # Triangle KAB ~ KML, so AB/ML = KA/KM
    # x/240 = KA/300 => KA = 300 * x / 240 = 5x/4
    
    # KA + AF + FM = KM = 300
    # 5x/4 + x + 3x/2 = 300
    # (5/4 + 1 + 3/2)x = 300
    # (5/4 + 4/4 + 6/4)x = 300
    # (15/4)x = 300
    # x = 300 * 4 / 15 = 80
    
    # General formula:
    # FM/KM = x/KL => FM = KM * x / KL
    # KA/KM = x/ML => KA = KM * x / ML
    # KA + x + FM = KM
    # KM * x / ML + x + KM * x / KL = KM
    # x * (KM/ML + 1 + KM/KL) = KM
    # x = KM / (KM/ML + 1 + KM/KL)
    
    x = KM / (KM/ML + 1 + KM/KL)
    
    return int(round(x))

result = solve(200)

# 调用 solve
result = solve(inputs['side_length_1'])
print(result)