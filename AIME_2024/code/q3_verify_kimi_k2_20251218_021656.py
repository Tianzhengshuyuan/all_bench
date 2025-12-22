inputs = {'total_numbers': 10}

from math import comb

def solve(total_numbers):
    # Jen picks 4 distinct numbers
    jen_pick = 4
    # 4 numbers are randomly chosen from total_numbers
    drawn = 4
    
    # Ways to win grand prize: match all 4
    grand = 1
    
    # Ways to match exactly 3: C(4,3)*C(total_numbers - 4, 1)
    match3 = comb(4, 3) * comb(total_numbers - 4, 1)
    
    # Ways to match exactly 2: C(4,2)*C(total_numbers - 4, 2)
    match2 = comb(4, 2) * comb(total_numbers - 4, 2)
    
    # Total ways to win a prize (at least 2 matches)
    total_prize = grand + match3 + match2
    
    # Conditional probability: P(grand | prize) = grand / total_prize
    prob_num = grand
    prob_den = total_prize
    
    # Since grand=1, prob = 1 / total_prize
    # We need m+n where prob = m/n in lowest terms
    # Here m=1, n=total_prize, so m+n = 1 + total_prize
    return 1 + total_prize

# Example: solve(10) returns 116

# 调用 solve
result = solve(inputs['total_numbers'])
print(result)