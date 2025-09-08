# Set up stuff to define player as "X" or "O" 
# and alternate to change players

# Extra Credit: Colored Xs and Os
players = ["\033[31mX\033[0m", "\033[32m0\033[0m"]
global players_index
global winner_found
winner_found = False
players_index = 0  # index of the current player

# Initial setup of board
# I strongly suggest you use a 1D array (a list) 
# rather than a 2D array (a list of lists).
board = [["1"], ["2"], ["3"],["4"], ["5"], ["6"], ["7"], ["8"], ["9"]]


# Function to print the current board state
'''
Follow this example: 
 1 │ 2 │ 3 
───┼───┼───
 4 │ 5 │ 6 
───┼───┼───
 7 │ 8 │ 9 
Replace the number by the symbol when the space is filled
'''
def display_board():
    # Use print() with an f-string or a string with .format()
    for i in range(3):
        print(f" {board[3*i][0]} │ {board[3*i+1][0]} │ {board[3*i+2][0]} ")
        if i < 2:
            print("───┼───┼───")
    pass

def threes_in_a_row():
    threes = []
    # rows, columns, diagonals
    threes = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    
    return threes

# Function to check for wins by the current player
def check_win(player):
    # # Rows
    # if board[0][0] == board[1][0] == board[2][0] == player:
    #     return True
    # if board[3][0] == board[4][0] == board[5][0] == player:
    #     return True
    # if board[6][0] == board[7][0] == board[8][0] == player:
    #     return True
    # # Columns
    # if board[0][0] == board[3][0] == board[6][0] == player:
    #     return True
    # if board[1][0] == board[4][0] == board[7][0] == player:
    #     return True
    # if board[2][0] == board[5][0] == board[8][0] == player:
    #     return True
    # # Diagonals
    # if board[0][0] == board[4][0] == board[8][0] == player:
    #     return True
    # if board[2][0] == board[4][0] == board[6][0] == player:
    #     return True
    # return False
    threes = threes_in_a_row()
    for combo in threes:
        if board[combo[0]][0] == player and board[combo[1]][0] == player and board[combo[2]][0] == player:
            return True
    return False
    
def switch_player():
    global players_index
    players_index = (players_index + 1) % 2
    return players[players_index]

def print_all_wins():
    threes = threes_in_a_row()
    for combo in threes:
        board_display = []
        for i in range(9):
            if i in combo:
                board_display.append("X")
            else:
                board_display.append(" ")
        # Print the board
        print(f" {board_display[0]} │ {board_display[1]} │ {board_display[2]} ")
        print("───┼───┼───")
        print(f" {board_display[3]} │ {board_display[4]} │ {board_display[5]} ")
        print("───┼───┼───")
        print(f" {board_display[6]} │ {board_display[7]} │ {board_display[8]} ")
        print()
      
    pass

prompt = input("Press [enter] to begin: ")
if prompt == "print":
    print_all_wins()

# Call display_board()
display_board()

# Loop for a maximum of 9 turns, then it's a draw
winner_found = False
for i in range(9):
    # Ask for input repeatedly until valid (while True ... if break)
    while True:
        move = input(f"Player {players[players_index]}, choose a space (1-9): ")
        if move.isnumeric() and int(move) in range(1, 10) and board[int(move)-1][0] not in players:
            board[int(move)-1][0] = players[players_index]
            if check_win(players[players_index]):
                print(f"Player {players[players_index]} wins!")
                winner_found = True
                break
            # Alternate players
            switch_player()
            break
        else:
            print(f"{move} is not a valid choice.  Try again.")
    # **Look up string.isnumeric() and the in keyword to help you with this**

    # Display the updated board
    display_board()

    if winner_found:
        break
else:  # else block on if only runs if the for loop ends normally (not with a break)
    # Print message for a draw
    print("It's a draw!")

    pass
