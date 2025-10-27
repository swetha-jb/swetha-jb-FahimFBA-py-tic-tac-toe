import sys, os, types
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '{repo_basename}')))


# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', f'{safe_repo_name}')))
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
import sys
import random
from unittest.mock import patch, MagicMock

sys.path.insert(0, r'/home/vvdn/projects/sfit_unitest_19_9_2025/cloned_repos/py-tic-tac-toe')

from tic_tac_toe import TicTacToe

class _WidgetMock:
    def __init__(self, *args, **kwargs):
        pass

def test_create_board():
    game = TicTacToe()
    game.create_board()
    assert game.board == [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

def test_get_random_first_player():
    game = TicTacToe()
    player_choice = game.get_random_first_player()
    assert player_choice in [0, 1]

def test_fix_spot():
    game = TicTacToe()
    game.create_board()
    game.fix_spot(0, 0, 'X')
    assert game.board[0][0] == 'X'
    game.fix_spot(1, 2, 'O')
    assert game.board[1][2] == 'O'

def test_has_player_won_row():
    game = TicTacToe()
    game.create_board()
    game.board = [['X', 'X', 'X'], ['-', '-', '-'], ['-', '-', '-']]
    assert game.has_player_won('X') is True

def test_has_player_won_column():
    game = TicTacToe()
    game.create_board()
    game.board = [['X', '-', '-'], ['X', '-', '-'], ['X', '-', '-']]
    assert game.has_player_won('X') is True

def test_has_player_won_diagonal_main():
    game = TicTacToe()
    game.create_board()
    game.board = [['X', '-', '-'], ['-', 'X', '-'], ['-', '-', 'X']]
    assert game.has_player_won('X') is True

def test_has_player_won_diagonal_anti():
    game = TicTacToe()
    game.create_board()
    game.board = [['-', '-', 'X'], ['-', 'X', '-'], ['X', '-', '-']]
    assert game.has_player_won('X') is True

def test_has_player_won_no_win():
    game = TicTacToe()
    game.create_board()
    game.board = [['X', 'O', '-'], ['-', 'X', '-'], ['-', '-', 'O']]
    assert game.has_player_won('X') is False
    assert game.has_player_won('O') is False

def test_is_board_filled_true():
    game = TicTacToe()
    game.board = [['X', 'O', 'X'], ['O', 'X', 'O'], ['O', 'X', 'O']]
    assert game.is_board_filled() is True

def test_is_board_filled_false():
    game = TicTacToe()
    game.board = [['X', 'O', '-'], ['O', 'X', 'O'], ['O', 'X', 'O']]
    assert game.is_board_filled() is False

def test_swap_player_turn():
    game = TicTacToe()
    assert game.swap_player_turn('X') == 'O'
    assert game.swap_player_turn('O') == 'X'

@patch('builtins.input', side_effect=['1 1', '1 2', '2 1', '2 2', '3 1', '3 2', '1 3', '2 3', '3 3'])
@patch('random.randint', return_value=1) # 'X' starts
def test_start_game_win_x(mock_randint, mock_input):
    game = TicTacToe()
    with patch('builtins.print') as mock_print:
        game.start()
        # Check if 'X' wins
        mock_print.assert_any_call('Player X wins the game!')

@patch('builtins.input', side_effect=['1 1', '1 2', '2 1', '2 2', '3 1', '3 2', '1 3', '2 3', '3 3'])
@patch('random.randint', return_value=0) # 'O' starts
def test_start_game_win_o(mock_randint, mock_input):
    game = TicTacToe()
    with patch('builtins.print') as mock_print:
        game.start()
        # Check if 'O' wins
        mock_print.assert_any_call('Player O wins the game!')

@patch('builtins.input', side_effect=['1 1', '1 2', '1 3', '2 1', '2 2', '2 3', '3 1', '3 2', '3 3'])
@patch('random.randint', return_value=1) # 'X' starts
def test_start_game_draw(mock_randint, mock_input):
    game = TicTacToe()
    with patch('builtins.print') as mock_print:
        game.start()
        mock_print.assert_any_call('Match Draw!')

@patch('builtins.input', side_effect=['1 1', '1 1', '1 2']) # Invalid move, then valid
@patch('random.randint', return_value=1) # 'X' starts
def test_start_game_invalid_move(mock_randint, mock_input):
    game = TicTacToe()
    with patch('builtins.print') as mock_print:
        game.start()
        mock_print.assert_any_call('Invalid spot. Try again!')
        # Check if the game eventually progresses after an invalid move
        mock_print.assert_any_call('Player O turn')

@patch('builtins.input', side_effect=['1 4', '1 1']) # Out of bounds, then valid
@patch('random.randint', return_value=1) # 'X' starts
def test_start_game_out_of_bounds_move(mock_randint, mock_input):
    game = TicTacToe()
    with patch('builtins.print') as mock_print:
        game.start()
        mock_print.assert_any_call('Invalid spot. Try again!')
        mock_print.assert_any_call('Player O turn')

@patch('builtins.input', side_effect=['a b', '1 1']) # Non-integer input, then valid
@patch('random.randint', return_value=1) # 'X' starts
def test_start_game_non_integer_input(mock_randint, mock_input):
    game = TicTacToe()
    with patch('builtins.print') as mock_print:
        game.start()
        mock_print.assert_any_call("invalid literal for int() with base 10: 'a'")
        mock_print.assert_any_call('Player O turn')


if __name__ == "__main__":
    import pytest, sys
    sys.exit(pytest.main([__file__, "-v"]))