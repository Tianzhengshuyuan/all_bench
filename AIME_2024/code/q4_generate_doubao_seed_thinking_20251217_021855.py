inputs = {'max_stack_size': 494}

def solve(max_stack_size):
    count0 = max_stack_size // 5
    count2 = ((max_stack_size - 2) // 5) + 1
    return count0 + count2

# 调用 solve
result = solve(inputs['max_stack_size'])
print(result)