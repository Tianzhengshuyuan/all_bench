inputs = {'total_sum': 300}

def solve(total_sum):
    # From the derivation we know that (a-100)(b-100)(c-100)=0
    # So at least one of a,b,c equals 100
    # Let a'=a-100, b'=b-100, c'=c-100, then a'+b'+c'=0 and a',b',c'>=-100
    # We need nonnegative a,b,c => a',b',c'>=-100
    # But since a'+b'+c'=0 and a',b',c'>=-100, we can shift to nonnegative variables
    # Let x=a', y=b', z=c', then x+y+z=0, x,y,z>=-100
    # Let u=x+100, v=y+100, w=z+100, then u+v+w=300, u,v,w>=0
    # And we need at least one of x,y,z to be 0 => at least one of u,v,w to be 100
    # So we count nonnegative integer solutions to u+v+w=300 with at least one of u,v,w equal to 100
    
    # Total solutions without restriction: C(300+3-1, 3-1)=C(302,2)
    # But we want only those with at least one variable equal to 100
    # Use inclusion-exclusion:
    # Let A: u=100, B: v=100, C: w=100
    # |A|: u=100 => v+w=200 => C(202,1)=202
    # |A∩B|: u=100,v=100 => w=100 => 1 solution
    # |A∩B∩C|: 1 solution
    # By inclusion-exclusion:
    # |A∪B∪C| = 3*202 - 3*1 + 1 = 606 - 3 + 1 = 604
    # But wait: our transformation is exact and the condition is equivalent to at least one of a,b,c being 100
    # However, the original derivation shows that exactly the condition (a-100)(b-100)(c-100)=0 is necessary and sufficient
    # So we can directly count:
    # Case 1: exactly one of a,b,c is 100
    #   Choose which one: 3 ways
    #   The other two sum to 200 and neither is 100 => 201 solutions (0 to 200) minus the one where both=100 => 200
    #   So 3*200 = 600
    # Case 2: all three are 100 => 1 solution
    # Total = 600 + 1 = 601
    
    # But we must ensure this logic holds for general total_sum
    # From the derivation: we had (a - k)(b - k)(c - k) = 0 where k = total_sum // 3
    # And indeed the equation reduced to that when k=100 for total_sum=300
    # So generalizing: let k = total_sum // 3
    k = total_sum // 3
    # The condition becomes (a-k)(b-k)(c-k)=0
    # And a+b+c=total_sum
    # So at least one of a,b,c equals k
    # We count nonnegative integer solutions to a+b+c=total_sum with at least one of a,b,c equal to k
    
    # Case 1: exactly one variable equals k
    #   Choose which: 3 ways
    #   The other two sum to total_sum - k = 2k, and neither equals k
    #   Number of nonnegative solutions to x+y=2k is 2k+1
    #   Subtract the one where x=k (then y=k) => 2k solutions
    #   So 3 * 2k = 6k
    case1 = 3 * (2 * k)
    
    # Case 2: all three equal k
    #   Only possible if 3k = total_sum => which is true since k = total_sum//3 and total_sum=300 is divisible by 3
    #   So 1 solution
    case2 = 1
    
    return case1 + case2

# The function is designed for the case where total_sum is divisible by 3
# If not, the condition (a-k)(b-k)(c-k)=0 might not hold, but the problem guarantees it for total_sum=300

# 调用 solve
result = solve(inputs['total_sum'])
print(result)