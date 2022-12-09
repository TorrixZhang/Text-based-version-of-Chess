"""
Chess Game
Assignment 1
Semester 2, 2021
CSSE1001/CSSE7030
"""

from typing import Optional, Tuple

from a1_support import *

# Replace these <strings> with your name, student number and email address.
__author__ = "Yutao Zhang, 46642538"
__email__ = "yutao.zhang@uqconnect.edu.au"


def initial_state() -> Board:
    """Return the board state for a new game.

    Returns:
        (Board): The board state for a new game.
    """
    return ("".join(BLACK_PIECES)[:-1], BLACK_PAWN * 8, EMPTY * 8, EMPTY * 8,
            EMPTY * 8, EMPTY * 8, WHITE_PAWN * 8, "".join(WHITE_PIECES)[:-1])


def print_board(board: Board) -> None:
    """Print a human-readable board.

    Parameter:
        board (Board): The current board state.
    """
    row_num = 8
    for row in board:
        print(row, '', row_num)
        row_num -= 1
    print('\nabcdefgh')


def square_to_position(square: str) -> Position:
    """Convert chess notation to its (row, col): Position equivalent.

    Parameter:
        square (str): The chess notation
    
    Returns:
        (str): The position in the board state.
    """
    col_list = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    row = 8 - int(square[1])
    col = col_list[square[0]]
    return row, col


def process_move(user_input: str) -> Move:
    """Assume the user_input is valid and convert the user input to a move based on (row, col): Position.

    Parameter:
        user_input (str): The current chess notation and new chess notation of the piece

    Returns:
        (tuple<position>): A tuple of the piece's current position and new position in the board state.
    """
    current_position, space, new_position = user_input.partition(" ")
    return square_to_position(current_position), square_to_position(new_position)


def change_position(board: Board, position: Position, character: str) -> Board:
    """Return a copy of board with the character at position changed to character.

    Parameter:
        board (Board): The current board state
        position (Position): The position in the board state where user want to change the character
        character (str): The character user want to change to.

    Returns:
        (board): A copy of board with the character at position changed to character.
    """
    board = list(board)
    row = position[0]
    column = position[1]
    board[row] = board[row][:column] + character + board[row][column + 1:]  # Put the character in the place we need
    return tuple(board)


def clear_position(board: Board, position: Position) -> Board:
    """Clear the piece at position (i.e. replace with an empty square) and return the resulting board.

    Parameter:
        board (Board): The current board state
        position (Position): The position in the board state where user want to clear the piece.

    Returns:
        (board): The board state with the piece at position is cleared.
    """
    return change_position(board, position, EMPTY)


def update_board(board: Board, move: Move) -> Board:
    """Assume the move is valid and return an updated version of the board with the move made.

    Parameter:
        board (Board): The current board state
        move (Move): The current position and new position of a piece.

    Returns:
        (board): The updated version of the board with the move made.
    """
    (x1, y1), (x2, y2) = move
    piece = board[x1][y1]
    board = change_position(board, (x2, y2), piece)
    board = clear_position(board, (x1, y1))
    return board


def is_current_players_piece(piece: str, whites_turn: bool) -> bool:
    """Returns true only when piece is belongs to the player whose turn it is.

    Parameter:
        piece (str): The name of piece
        whites_turn (bool): True iff it's white's turn.

    Returns:
        (bool): True iff the piece is belongs to the current player.
    """
    return whites_turn and piece in WHITE_PIECES or not whites_turn and piece in BLACK_PIECES


def is_move_valid(move: Move, board: Board, whites_turn: bool) -> bool:
    """Returns true only when the move is valid on the current board state for the player whose turn it is.

    Parameter:
        move (Move): The current position and new position of a piece.
        board (Board): The current board state
        whites_turn (bool): True iff it's white's turn.

    Returns:
        (bool): True iff the piece's move is valid on the current board state for the player whose turn it is.
    """
    current_position, next_position = move
    current_piece = board[current_position[0]][current_position[1]]  # The current position of the piece
    next_piece = board[next_position[0]][next_position[1]]  # The next position of the piece (after the move)

    return not out_of_bounds(current_position) and not out_of_bounds(next_position) \
           and current_position != next_position \
           and is_current_players_piece(current_piece, whites_turn) \
           and (next_piece == EMPTY or not is_current_players_piece(next_piece, whites_turn)) \
           and next_position in get_possible_moves(current_position, board) \
           and not is_in_check(update_board(board, move), whites_turn)
    # First line: Both positions in the move exist on the board;
    # Second line: The positions in the move are different;
    # The third line: The piece being moved belongs to the player who is trying to move it;
    # The fourth line: The square the piece is being moved to is empty or contains a piece of the opposite colour;
    # The fifth line: The move is a valid for the type of piece being moved;
    # The sixth line: The move does not put the player whose turn it is in check.




def can_move(board: Board, whites_turn: bool) -> bool:
    """Returns true only when the player can make a valid move which does not put them in check

    Parameters:
        board (Board): The current board state
        whites_turn (bool): True iff it's white's turn.

    Returns:
        (bool): True iff the player can make a valid move which does not put them in check.
    """
    piece_possible_pos = []
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            while is_current_players_piece(board[row][column], whites_turn):
                piece_possible_pos.append((row, column))  # Find out all piece's position on the board
                break

    for current_pos in piece_possible_pos:
        for next_pos in get_possible_moves(current_pos, board):  # Get possible moves of the existed pieces
            move = (current_pos, next_pos)
            if is_move_valid(move, board, whites_turn):  # Find out if the existed pieces can make any valid move
                return True
    return False


def is_stalemate(board: Board, whites_turn: bool) -> bool:
    """Returns true only when a stalemate has been reached.

    Parameters:
        board (Board): The current board state
        whites_turn (bool): True iff it's white's turn.

    Returns:
        (bool): True iff a stalemate has been reached.
    """
    return not is_in_check(board, whites_turn) and not can_move(board, whites_turn)
    # When a player is not in check but cannot make any move, return ture


def check_game_over(board: Board, whites_turn: bool) -> bool:
    """Returns true only when the game is over (either due to checkmate or stalemate).

    Parameters:
        board (Board): The current board state
        whites_turn (bool): True iff it's white's turn.

    Returns:
        (bool): True iff the game is over (either due to checkmate or stalemate).
    """
    if is_in_check(board, whites_turn):
        if not can_move(board, whites_turn):  # When a player is in check and cannot make any move, then it's checkmate
            print("\nCheckmate")
            return True
        elif whites_turn is True:
            print("\nWhite is in check")
            return False
        else:
            print("\nBlack is in check")
            return False
    elif is_stalemate(board, whites_turn):  # When a player is not in check but cannot make any move, it's stalemate
        print("\nStalemate")
        return True
    else:
        return False


def attempt_promotion(board: Board, whites_turn: bool) -> Board:
    """Checks whether there is a pawn on the board that needs to be promoted.

    Parameters:
        board (Board): The current board state
        whites_turn (bool): True iff it's white's turn.

    Returns:
        (board): The new board with the pawn is promoted.
    """
    wh_piece_dir = {"q": WHITE_QUEEN, "n": WHITE_KNIGHT, "r": WHITE_ROOK, "b": WHITE_BISHOP}
    bl_piece_dir = {"q": BLACK_QUEEN, "n": BLACK_KNIGHT, "r": BLACK_ROOK, "b": BLACK_BISHOP}

    if whites_turn:
        if WHITE_PAWN in board[0]:
            column = board[0].index(WHITE_PAWN)  # Find out the column of the piece which is going to be promoted
            while True:
                promote_piece = input("What piece would you like (q, n, r, b)? ")
                if promote_piece in wh_piece_dir:  # If user choose a piece within the range of (q, n, r, b)
                    board = change_position(board, (0, column), wh_piece_dir[promote_piece])
                    # use function change_position to promote the piece
                    break
                else:
                    print("Not a valid piece. ", end='')
    else:
        if BLACK_PAWN in board[7]:
            column = board[7].index(BLACK_PAWN)  # Find out the column of the piece which is going to be promoted
            while True:
                promote_piece = input("What piece would you like (q, n, r, b)? ")
                if promote_piece in bl_piece_dir:  # If user choose a piece within the range of (q, n, r, b)
                    board = change_position(board, (0, column), bl_piece_dir[promote_piece])
                    # use function change_position to promote the piece
                    break
                else:
                    print("Not a valid piece. ", end='')
    return board


def is_valid_castle_attempt(move: Move, board: Board, whites_turn: bool,
                            castling_info: Tuple[bool, bool, bool]) -> bool:
    """Returns true only when the given move is a valid attempt at castling for the current board state.

    Args:
        move:
        board:
        whites_turn:
        castling_info:

    Returns:

    """
    pass


def perform_castling(move: Move, board: Board) -> Board:
    """Given a valid castling move, returns the resulting board state.

    Args:
        move:
        board:

    Returns:

    """
    pass


def is_valid_en_passant(move: Move, board: Board, whites_turn: bool, en_passant_position: Optional[Position]) -> bool:
    """Returns true only when the supplied move constitutes a valid en passant move.

    Args:
        move:
        board:
        whites_turn:
        en_passant_position:

    Returns:

    """
    pass


def perform_en_passant(move: Move, board: Board, whites_turn: bool) -> Board:
    """Given a valid en passant move, returns the resulting board state.

    Args:
        move:
        board:
        whites_turn:

    Returns:

    """
    pass


def update_castling_info(move: Move, whites_turn: bool, castling_info: Tuple[bool, bool, bool]) -> Tuple[
    bool, bool, bool]:
    """Returns the updated castling information for the player whose turn it is, after performing the given valid move.

    Args:
        move:
        whites_turn:
        castling_info:

    Returns:

    """
    pass


def update_en_passant_position(move: Move, board: Board, whites_turn: bool) -> Optional:
    """If the current player’s pawn just moved forward two squares, returns the position that an opponent pawn could
     take to perform a valid en passant move.

    Args:
        move:
        board:
        whites_turn:

    Returns:

    """
    pass


def main():
    """Entry point to gameplay"""
    board = initial_state()
    whites_turn = True
    while True:
        print_board(board)
        if check_game_over(board, whites_turn):
            break
        if whites_turn:
            user_input = input("\nWhite's move: ")
        else:
            user_input = input("\nBlack's move: ")

        if user_input in "hH":  # If user call a help menu
            print(HELP_MESSAGE)
        elif user_input in "qQ":  # If user want to quit
            user_input = input("Are you sure you want to quit? ")
            while user_input in "yY":
                return
        elif not valid_move_format(user_input):  # Determine if the move user input is in valid format
            print("Invalid move\n")
        else:
            move = process_move(user_input)
            if is_move_valid(move, board, whites_turn):
                board = update_board(board, move)
                whites_turn = not whites_turn
            else:  # Those moves in valid format but cannot achieved according to the rules
                print("Invalid move\n")
    return


if __name__ == "__main__":
    main()
