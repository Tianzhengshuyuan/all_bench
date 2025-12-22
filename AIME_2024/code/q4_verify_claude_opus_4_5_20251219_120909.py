inputs = {'tokens_per_move_option': 4}

def solve(tokens_per_move_option):
    """
    Solve the token game problem where Alice and Bob take turns.
    Alice goes first. Each player can remove 1 token or tokens_per_move_option tokens.
    Whoever removes the last token wins.
    
    We need to find how many positive integers n <= 2024 are winning positions for Bob.
    """
    max_n = 2024
    
    # Use dynamic programming to find winning/losing positions
    # True = Alice wins (winning position for the player to move)
    # False = Bob wins (losing position for the player to move, i.e., Alice loses)
    
    # We need to handle n from 0 to max_n
    # n = 0 means the previous player took the last token and won
    # So if it's your turn and n = 0, you've already lost (but this shouldn't happen in normal play)
    
    # A position is a losing position (for the player to move) if ALL moves lead to winning positions
    # A position is a winning position (for the player to move) if ANY move leads to a losing position
    
    # alice_wins[n] = True if Alice wins when there are n tokens and it's Alice's turn
    # Since Alice always goes first, we just need to compute who wins from each starting position
    
    # Let's define: win[n] = True if the player whose turn it is will win with optimal play
    # win[0] is undefined (game already over), but we can say win[0] = False (you lose if no tokens left on your turn)
    
    win = [False] * (max_n + 1)
    
    # Base cases
    # n = 0: if it's your turn and there are 0 tokens, you can't move, you lose
    win[0] = False
    
    # For n >= 1, compute based on possible moves
    for n in range(1, max_n + 1):
        # Possible moves: take 1 token or take tokens_per_move_option tokens
        can_win = False
        
        # Take 1 token
        if n >= 1:
            # After taking 1, opponent faces n-1 tokens
            if not win[n - 1]:
                can_win = True
        
        # Take tokens_per_move_option tokens
        if n >= tokens_per_move_option:
            # After taking tokens_per_move_option, opponent faces n - tokens_per_move_option tokens
            if not win[n - tokens_per_move_option]:
                can_win = True
        
        win[n] = can_win
    
    # Count positions where Bob wins (i.e., Alice loses, i.e., win[n] = False)
    bob_wins_count = 0
    for n in range(1, max_n + 1):
        if not win[n]:
            bob_wins_count += 1
    
    return bob_wins_count


result = solve(4)

# 调用 solve
result = solve(inputs['tokens_per_move_option'])
print(result)