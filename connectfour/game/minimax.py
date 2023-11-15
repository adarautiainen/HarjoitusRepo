from board import GameBoard


def evaluate(board):
    scoreX = calculate_score(board, 'X')
    scoreO = calculate_score(board, 'O')

    return scoreX - scoreO


def game_over(board):
    pass


def calculate_score(board, symbol):
    score = 0

    # horizontal check
    for row in board.board:
        score += count_consecutive(row, symbol)

    # vertical check
    for col in range(board.columns):
        column = [board.board[row][col] for row in range(board.rows)]
        score += count_consecutive(column, symbol)

    # diagonal check left->right
    for i in range(board.rows - 3):
        for j in range(board.columns - 3):
            diagonal = [board.board[i + k][j + k] for k in range(4)]
            score += count_consecutive(diagonal, symbol)

    # diagonal check right->left
    for i in range(3, board.rows):
        for j in range(board.columns - 3):
            diagonal = [board.board[i - k][j + k] for k in range(4)]
            score += count_consecutive(diagonal, symbol)

    return score


def count_consecutive(line, symbol):
    consecutive = 0
    maxc = 0

    for i in line:
        if i == symbol:
            consecutive += 1
            maxc = max(maxc, consecutive)
        else:
            consecutive = 0

    return maxc


def minimax(board, depth, maximizing):
    pass
