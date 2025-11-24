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

import sys
sys.path.insert(0, r'/home/vvdn/projects/sfit_unitest_19_9_2025/cloned_repos/py-tic-tac-toe')

import pytest
import random
from unittest.mock import patch, MagicMock

from py_tic_tac_toe.tic_tac_toe import TicTacToe

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
    game.fix_spot(0, 0, 'X')
    game.fix_spot(0, 1, 'X')
    game.fix_spot(0, 2, 'X')
    assert game.has_player_won('X') == True

def test_has_player_won_column():
    game = TicTacToe()
    game.create_board()
    game.fix_spot(0, 1, 'O')
    game.fix_spot(1, 1, 'O')
    game.fix_spot(2, 1, 'O')
    assert game.has_player_won('O') == True

def test_has_player_won_diagonal_main():
    game = TicTacToe()
    game.create_board()
    game.fix_spot(0, 0, 'X')
    game.fix_spot(1, 1, 'X')
    game.fix_spot(2, 2, 'X')
    assert game.has_player_won('X') == True

def test_has_player_won_diagonal_anti():
    game = TicTacToe()
    game.create_board()
    game.fix_spot(0, 2, 'O')
    game.fix_spot(1, 1, 'O')
    game.fix_spot(2, 0, 'O')
    assert game.has_player_won('O') == True

def test_has_player_won_no_win():
    game = TicTacToe()
    game.create_board()
    game.fix_spot(0, 0, 'X')
    game.fix_spot(1, 1, 'O')
    assert game.has_player_won('X') == False
    assert game.has_player_won('O') == False

def test_is_board_filled_true():
    game = TicTacToe()
    game.board = [['X', 'O', 'X'], ['O', 'X', 'O'], ['O', 'X', 'O']]
    assert game.is_board_filled() == True

def test_is_board_filled_false():
    game = TicTacToe()
    game.board = [['X', 'O', 'X'], ['O', '-', 'O'], ['O', 'X', 'O']]
    assert game.is_board_filled() == False

def test_swap_player_turn():
    game = TicTacToe()
    assert game.swap_player_turn('X') == 'O'
    assert game.swap_player_turn('O') == 'X'

@patch('builtins.input', side_effect=['1 1', '1 2', '1 3', '2 1', '2 2', '2 3', '3 1', '3 2', '3 3'])
@patch('random.randint', return_value=1)
def test_start_player_x_wins(mock_randint, mock_input):
    game = TicTacToe()
    with patch('builtins.print') as mock_print:
        game.start()
        mock_print.assert_any_call('Player X wins the game!')

@patch('builtins.input', side_effect=['1 1', '1 2', '1 3', '2 1', '2 2', '2 3', '3 1', '3 2', '3 3'])
@patch('random.randint', return_value=0)
def test_start_player_o_wins(mock_randint, mock_input):
    game = TicTacToe()
    with patch('builtins.print') as mock_print:
        game.start()
        mock_print.assert_any_call('Player O wins the game!')

@patch('builtins.input', side_effect=['1 1', '1 2', '1 3', '2 1', '2 2', '2 3', '3 1', '3 2', '3 3'])
@patch('random.randint', return_value=1)
def test_start_draw(mock_randint, mock_input):
    game = TicTacToe()
    game.board = [['X', 'O', 'X'], ['O', 'X', 'O'], ['O', 'X', 'O']]
    with patch('builtins.print') as mock_print:
        game.start()
        mock_print.assert_any_call('Match Draw!')

@patch('builtins.input', side_effect=['1 1', '1 2', '1 3', '2 1', '2 2', '2 3', '3 1', '3 2', '3 3'])
@patch('random.randint', return_value=1)
def test_start_invalid_input(mock_randint, mock_input):
    game = TicTacToe()
    with patch('builtins.print') as mock_print:
        game.start()
        mock_print.assert_any_call('Invalid spot. Try again!')

@patch('builtins.input', side_effect=['1 1', '1 2', '1 3', '2 1', '2 2', '2 3', '3 1', '3 2', '3 3'])
@patch('random.randint', return_value=1)
def test_start_value_error(mock_randint, mock_input):
    game = TicTacToe()
    with patch('builtins.print') as mock_print:
        game.start()
        mock_print.assert_any_call("Invalid input. Please enter two numbers separated by a space.")

if __name__ == "__main__":
    import pytest, sys
    sys.exit(pytest.main([__file__, "-v"]))