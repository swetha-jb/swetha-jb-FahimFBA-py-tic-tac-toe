import sys, os, types
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'py-tic-tac-toe')))

# Auto-mock tkinter for headless environments
try:
    import tkinter as tk
except ImportError:
    import sys, types
    class _WidgetMock:
        def __init__(self, *a, **k): self._text = ""
        def config(self, **kwargs): 
            if "text" in kwargs: self._text = kwargs["text"]
        def cget(self, key): return self._text if key == "text" else None
        def get(self): return self._text
        def grid(self, *a, **k): return []
        def pack(self, *a, **k): return []
        def place(self, *a, **k): return []
        def destroy(self): return None
        def __getattr__(self, item): return lambda *a, **k: None
    tk = types.ModuleType("tkinter")
    for widget in ["Tk","Label","Button","Entry","Frame","Canvas","Text","Scrollbar","Checkbutton",
                "Radiobutton","Spinbox","Menu","Toplevel","Listbox"]:
        setattr(tk, widget, _WidgetMock)
    for const in ["N","S","E","W","NE","NW","SE","SW","CENTER","NS","EW","NSEW"]:
        setattr(tk, const, const)
    sys.modules["tkinter"] = tk

import pytest
from unittest.mock import patch
from io import StringIO

# Assuming the source code is in a file named main.py
# from main import TicTacToe

# If the source code is in the same file as the tests, you can use it directly:
class TicTacToe:

    def __init__(self):
        self.board = []

    def create_board(self):
        # Initialize an empty 3x3 board with dashes '-'
        self.board = [['-' for _ in range(3)] for _ in range(3)]

    def get_random_first_player(self):
        # Randomly choose which player goes first (0 for 'O', 1 for 'X')
        return random.randint(0, 1)

    def fix_spot(self, row, col, player):
        # Mark the spot on the board with the player's symbol
        self.board[row][col] = player

    def has_player_won(self, player):
        # Check if the player has won in rows, columns, or diagonals
        n = len(self.board)
        for i in range(n):
            # Check rows
            if all(self.board[i][j] == player for j in range(n)):
                return True

            # Check columns
            if all(self.board[j][i] == player for j in range(n)):
                return True

        # Check diagonals
        if all(self.board[i][i] == player for i in range(n)):
            return True
        if all(self.board[i][n - i - 1] == player for i in range(n)):
            return True

        return False

    def is_board_filled(self):
        # Check if the board is completely filled with symbols
        return all(self.board[i][j] != '-' for i in range(3) for j in range(3))

    def swap_player_turn(self, player):
        # Swap player turn between 'X' and 'O'
        return 'X' if player == 'O' else 'O'

    def show_board(self):
        # Display the current state of the board
        for row in self.board:
            print(' '.join(row))
        print()

    def start(self):
        self.create_board()
        player = 'X' if self.get_random_first_player() == 1 else 'O'
        game_over = False

        while not game_over:
            try:
                self.show_board()
                print(f'Player {player} turn')

                # Get user input for row and column to fix the spot
                row, col = list(map(int, input('Enter row & column numbers to fix spot: ').split()))
                print()

                # Convert to 0-based index for internal board representation
                row -= 1
                col -= 1

                # Check if the spot is valid and not already taken
                if 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == '-':
                    self.fix_spot(row, col, player)

                    # Check if the current player has won
                    if self.has_player_won(player):
                        print(f'Player {player} wins the game!')
                        game_over = True
                    elif self.is_board_filled():
                        print('Match Draw!')
                        game_over = True
                    else:
                        player = self.swap_player_turn(player)
                else:
                    print('Invalid spot. Try again!')

            except ValueError as err:
                print(err)

        print()
        self.show_board()


@pytest.fixture
def ttt_game():
    game = TicTacToe()
    game.create_board()
    return game

def test_create_board(ttt_game):
    assert ttt_game.board == [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

def test_fix_spot(ttt_game):
    ttt_game.fix_spot(0, 0, 'X')
    assert ttt_game.board[0][0] == 'X'
    ttt_game.fix_spot(1, 2, 'O')
    assert ttt_game.board[1][2] == 'O'

def test_has_player_won_row(ttt_game):
    ttt_game.fix_spot(0, 0, 'X')
    ttt_game.fix_spot(0, 1, 'X')
    ttt_game.fix_spot(0, 2, 'X')
    assert ttt_game.has_player_won('X') == True

def test_has_player_won_column(ttt_game):
    ttt_game.fix_spot(0, 1, 'O')
    ttt_game.fix_spot(1, 1, 'O')
    ttt_game.fix_spot(2, 1, 'O')
    assert ttt_game.has_player_won('O') == True

def test_has_player_won_diagonal_main(ttt_game):
    ttt_game.fix_spot(0, 0, 'X')
    ttt_game.fix_spot(1, 1, 'X')
    ttt_game.fix_spot(2, 2, 'X')
    assert ttt_game.has_player_won('X') == True

def test_has_player_won_diagonal_anti(ttt_game):
    ttt_game.fix_spot(0, 2, 'O')
    ttt_game.fix_spot(1, 1, 'O')
    ttt_game.fix_spot(2, 0, 'O')
    assert ttt_game.has_player_won('O') == True

def test_has_player_won_no_win(ttt_game):
    ttt_game.fix_spot(0, 0, 'X')
    ttt_game.fix_spot(0, 1, 'O')
    ttt_game.fix_spot(0, 2, 'X')
    assert ttt_game.has_player_won('X') == False
    assert ttt_game.has_player_won('O') == False

def test_is_board_filled_true(ttt_game):
    for r in range(3):
        for c in range(3):
            ttt_game.fix_spot(r, c, 'X' if (r+c)%2 == 0 else 'O')
    assert ttt_game.is_board_filled() == True

def test_is_board_filled_false(ttt_game):
    ttt_game.fix_spot(0, 0, 'X')
    assert ttt_game.is_board_filled() == False

def test_swap_player_turn():
    game = TicTacToe()
    assert game.swap_player_turn('X') == 'O'
    assert game.swap_player_turn('O') == 'X'

@patch('builtins.input', side_effect=['0 0', '1 1', '0 1', '2 2', '0 2', '2 0', '1 0', '1 2', '2 1'])
@patch('sys.stdout', new_callable=StringIO)
def test_start_player_x_wins(mock_stdout, mock_input):
    game = TicTacToe()
    with patch('random.randint', return_value=1): # Ensure 'X' goes first
        game.start()

    output = mock_stdout.getvalue()
    assert "Player X wins the game!" in output

@patch('builtins.input', side_effect=['0 0', '1 1', '0 1', '2 2', '0 2', '2 0', '1 0', '1 2', '2 1'])
@patch('sys.stdout', new_callable=StringIO)
def test_start_player_o_wins(mock_stdout, mock_input):
    game = TicTacToe()
    with patch('random.randint', return_value=0): # Ensure 'O' goes first
        game.start()

    output = mock_stdout.getvalue()
    assert "Player O wins the game!" in output

@patch('builtins.input', side_effect=['0 0', '1 1', '0 1', '2 2', '0 2', '1 0', '1 2', '2 0', '2 1'])
@patch('sys.stdout', new_callable=StringIO)
def test_start_draw(mock_stdout, mock_input):
    game = TicTacToe()
    with patch('random.randint', return_value=1): # Doesn't matter who starts for draw
        game.start()

    output = mock_stdout.getvalue()
    assert "Match Draw!" in output

@patch('builtins.input', side_effect=['0 0', '0 0', '1 1', '0 1', '2 2', '0 2', '1 0', '1 2', '2 1'])
@patch('sys.stdout', new_callable=StringIO)
def test_start_invalid_spot_twice(mock_stdout, mock_input):
    game = TicTacToe()
    with patch('random.randint', return_value=1):
        game.start()

    output = mock_stdout.getvalue()
    assert "Invalid spot. Try again!" in output
    assert output.count('Player X turn') == 2 # X tries to play invalid spot, then valid
    assert output.count('Player O turn') == 1

@patch('builtins.input', side_effect=['a b', '0 0']) # Test for ValueError
@patch('sys.stdout', new_callable=StringIO)
def test_start_value_error(mock_stdout, mock_input):
    game = TicTacToe()
    with patch('random.randint', return_value=1):
        game.start()
    output = mock_stdout.getvalue()
    assert "Invalid input. Please enter numbers." in output.replace("Enter row & column numbers to fix spot: \n", "")
    assert "Player X turn" in output
    assert game.board[0][0] == 'X'

def test_get_random_first_player():
    game = TicTacToe()
    result = game.get_random_first_player()
    assert result in [0, 1]