inputs = {'total_sets': 863}

def solve(total_sets):
    # The number of sets B with maximum element k is 2^(k-1)
    # So we need to find a set A of positive integers such that
    # sum of 2^(a-1) for a in A equals total_sets
    
    # This is equivalent to finding the binary representation of total_sets
    # where each bit position i (0-indexed) that is 1 corresponds to element (i+1) in A
    
    # Convert total_sets to binary and find which positions have 1s
    # If bit at position i is 1, then element (i+1) is in A
    
    A = []
    n = total_sets
    position = 0
    
    while n > 0:
        if n & 1:  # if the least significant bit is 1
            A.append(position + 1)  # element is position + 1
        n >>= 1
        position += 1
    
    return sum(A)

result = solve(2024)

# 调用 solve
result = solve(inputs['total_sets'])
print(result)