# ChatGPT generated
def create_board():
    return [[' ' for _ in range(3)] for _ in range(3)]

def print_board(board):
    for row in board:
        print("|".join(row))
        print("-----")

def is_valid_move(board, row, col):
    return board[row][col] == ' '

def make_move(board, row, col, player):
    new_board = [row.copy() for row in board]
    new_board[row][col] = player
    return new_board

def switch_player(player):
    return 'O' if player == 'X' else 'X'

def is_winner(board, player):
    for row in range(3):
        if all(cell == player for cell in board[row]):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_full(board):
    return all(board[row][col] != ' ' for row in range(3) for col in range(3))

def game_loop(board, player):
    print_board(board)

    if is_winner(board, switch_player(player)):
        print(f"{switch_player(player)} wins!")
        return
    elif is_full(board):
        print("It's a draw!")
        return

    row, col = map(int, input(f"{player}'s turn. Enter row and column (0-2): ").split())
    if is_valid_move(board, row, col):
        new_board = make_move(board, row, col, player)
        game_loop(new_board, switch_player(player))
    else:
        print("Invalid move, please try again.")
        game_loop(board, player)

def main():
    initial_board = create_board()
    game_loop(initial_board, 'X')

if __name__ == "__main__":
    main()
