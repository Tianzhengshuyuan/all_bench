inputs = {'bob_win_count': 809}

def solve(bob_win_count):
    c = int(bob_win_count)
    if c < 0:
        return None
    q, r = divmod(c, 2)
    return 5 * q + (1 if r == 0 else 4)

solve(809)

# 调用 solve
result = solve(inputs['bob_win_count'])
print(result)