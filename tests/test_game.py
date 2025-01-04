import pytest
import numpy as np
from sudoku_lib.game import SudokuGame

def test_new_game_creation():
    game = SudokuGame()
    puzzle = game.new_game(difficulty="medium")
    assert isinstance(puzzle, np.ndarray)
    assert puzzle.shape == (9, 9)
    # Check if the puzzle has some empty cells (zeros)
    assert np.sum(puzzle == 0) > 0

def test_invalid_difficulty():
    game = SudokuGame()
    with pytest.raises(ValueError):
        game.new_game(difficulty="invalid")

def test_verify_solution():
    game = SudokuGame()
    # Create a simple valid solution
    solution = np.array([
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [7, 8, 9, 1, 2, 3, 4, 5, 6],
        [2, 3, 1, 5, 6, 4, 8, 9, 7],
        [5, 6, 4, 8, 9, 7, 2, 3, 1],
        [8, 9, 7, 2, 3, 1, 5, 6, 4],
        [3, 1, 2, 6, 4, 5, 9, 7, 8],
        [6, 4, 5, 9, 7, 8, 3, 1, 2],
        [9, 7, 8, 3, 1, 2, 6, 4, 5]
    ])
    is_valid = game.verify_solution(solution)
    assert is_valid

def test_invalid_solution():
    game = SudokuGame()
    # Create an invalid solution (repeated numbers in a row)
    invalid_solution = np.array([
        [1, 1, 3, 4, 5, 6, 7, 8, 9],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [7, 8, 9, 1, 2, 3, 4, 5, 6],
        [2, 3, 1, 5, 6, 4, 8, 9, 7],
        [5, 6, 4, 8, 9, 7, 2, 3, 1],
        [8, 9, 7, 2, 3, 1, 5, 6, 4],
        [3, 1, 2, 6, 4, 5, 9, 7, 8],
        [6, 4, 5, 9, 7, 8, 3, 1, 2],
        [9, 7, 8, 3, 1, 2, 6, 4, 5]
    ])
    is_valid, errors = game.verify_solution(invalid_solution)
    assert not is_valid
    assert len(errors) > 0
    assert "Row 1 contains duplicate numbers" in errors
