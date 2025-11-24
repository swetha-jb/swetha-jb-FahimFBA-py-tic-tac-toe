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
from unittest.mock import patch, MagicMock
from tic_tac_toe import TicTacToe

class _WidgetMock:
    def __init__(self, *args, **kwargs):
        pass

    def __getattr__(self, name):
        return self

    def __call__(self, *args, **kwargs):
        return self

    def __setitem__(self, key, value):
        pass

    def __getitem__(self, key):
        return self

    def configure(self, **kwargs):
        pass

    def bind(self, event, handler):
        pass

    def grid(self, **kwargs):
        pass

    def pack(self, **kwargs):
        pass

    def place(self, **kwargs):
        pass

    def destroy(self):
        pass

    def get(self):
        return ""

    def set(self, value):
        pass

    def insert(self, index, string):
        pass

    def delete(self, first, last=None):
        pass

    def update(self):
        pass

    def mainloop(self):
        pass

    def quit(self):
        pass

    def destroy(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

@pytest.fixture
def tic_tac_toe_game():
    game = TicTacToe()
    game.create_board()
    return game

def test_create_board(tic_tac_toe_game):
    tic_tac_toe_game.create_board()
    assert tic_tac_toe_game.board == [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

def test_get_random_first_player(tic_tac_toe_game):
    player_choice = tic_tac_toe_game.get_random_first_player()
    assert player_choice in [0, 1]

def test_fix_spot(tic_tac_toe_game):
    tic_tac_toe_game.fix_spot(0, 0, 'X')
    assert tic_tac_toe_game.board[0][0] == 'X'

def test_has_player_won_row(tic_tac_toe_game):
    tic_tac_toe_game.board = [['X', 'X', 'X'], ['-', '-', '-'], ['-', '-', '-']]
    assert tic_tac_toe_game.has_player_won('X') is True

def test_has_player_won_column(tic_tac_toe_game):
    tic_tac_toe_game.board = [['X', '-', '-'], ['X', '-', '-'], ['X', '-', '-']]
    assert tic_tac_toe_game.has_player_won('X') is True

def test_has_player_won_diagonal_main(tic_tac_toe_game):
    tic_tac_toe_game.board = [['X', '-', '-'], ['-', 'X', '-'], ['-', '-', 'X']]
    assert tic_tac_toe_game.has_player_won('X') is True

def test_has_player_won_diagonal_anti(tic_tac_toe_game):
    tic_tac_toe_game.board = [['-', '-', 'X'], ['-', 'X', '-'], ['X', '-', '-']]
    assert tic_tac_toe_game.has_player_won('X') is True

def test_has_player_won_no_win(tic_tac_toe_game):
    tic_tac_toe_game.board = [['X', 'O', '-'], ['-', 'X', '-'], ['-', '-', 'O']]
    assert tic_tac_toe_game.has_player_won('X') is False
    assert tic_tac_toe_game.has_player_won('O') is False

def test_is_board_filled_true(tic_tac_toe_game):
    tic_tac_toe_game.board = [['X', 'O', 'X'], ['O', 'X', 'O'], ['O', 'X', 'O']]
    assert tic_tac_toe_game.is_board_filled() is True

def test_is_board_filled_false(tic_tac_toe_game):
    tic_tac_toe_game.board = [['X', 'O', '-'], ['O', 'X', 'O'], ['O', 'X', 'O']]
    assert tic_tac_toe_game.is_board_filled() is False

def test_swap_player_turn_x_to_o(tic_tac_toe_game):
    assert tic_tac_toe_game.swap_player_turn('X') == 'O'

def test_swap_player_turn_o_to_x(tic_tac_toe_game):
    assert tic_tac_toe_game.swap_player_turn('O') == 'X'

@patch('builtins.input', side_effect=['1 1', '1 2', '2 1', '2 2', '3 1', '3 2', '1 3', '2 3', '3 3'])
@patch('builtins.print')
def test_start_player_x_wins(mock_print, mock_input):
    with patch('random.randint', return_value=1): # Player X starts
        game = TicTacToe()
        game.start()
        mock_print.assert_any_call('Player X wins the game!')

@patch('builtins.input', side_effect=['1 1', '1 2', '2 1', '2 2', '3 1', '3 2', '1 3', '2 3', '3 3'])
@patch('builtins.print')
def test_start_player_o_wins(mock_print, mock_input):
    with patch('random.randint', return_value=0): # Player O starts
        game = TicTacToe()
        game.start()
        mock_print.assert_any_call('Player O wins the game!')

@patch('builtins.input', side_effect=['1 1', '1 2', '1 3', '2 1', '2 2', '2 3', '3 1', '3 2', '3 3'])
@patch('builtins.print')
def test_start_match_draw(mock_print, mock_input):
    with patch('random.randint', return_value=1): # Player X starts
        game = TicTacToe()
        game.start()
        mock_print.assert_any_call('Match Draw!')

@patch('builtins.input', side_effect=['1 1', '1 1', '1 2']) # Test invalid move
@patch('builtins.print')
def test_start_invalid_move(mock_print, mock_input):
    with patch('random.randint', return_value=1): # Player X starts
        game = TicTacToe()
        game.start()
        mock_print.assert_any_call('Invalid spot. Try again!')

@patch('builtins.input', side_effect=['a b', '1 2']) # Test invalid input type
@patch('builtins.print')
def test_start_invalid_input_type(mock_print, mock_input):
    with patch('random.randint', return_value=1): # Player X starts
        game = TicTacToe()
        game.start()
        mock_print.assert_any_call("invalid literal for int() with base 10: 'a'")


if __name__ == "__main__":
    import pytest, sys
    sys.exit(pytest.main([__file__, "-v"]))