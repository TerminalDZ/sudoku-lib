import pytest
import numpy as np
from sudoku_lib.solver import SudokuSolver

def test_solver_initialization():
    puzzle = np.zeros((9, 9), dtype=int)
    solver = SudokuSolver(puzzle)
    assert solver.grid.shape == (9, 9)
    assert np.array_equal(solver.grid, puzzle)

def test_solve_empty_puzzle():
    puzzle = np.zeros((9, 9), dtype=int)
    solver = SudokuSolver(puzzle)
    success, steps = solver.solve()
    assert success
    # Verify that the solution is valid
    assert all(np.sum(solver.grid, axis=0) == 45)  # All columns sum to 45
    assert all(np.sum(solver.grid, axis=1) == 45)  # All rows sum to 45

def test_solve_with_initial_values():
    # Create a puzzle with some initial values
    puzzle = np.zeros((9, 9), dtype=int)
    puzzle[0, 0] = 5
    puzzle[0, 1] = 3
    puzzle[1, 0] = 6
    
    solver = SudokuSolver(puzzle)
    success, steps = solver.solve()
    assert success
    # Check if initial values are preserved
    assert solver.grid[0, 0] == 5
    assert solver.grid[0, 1] == 3
    assert solver.grid[1, 0] == 6

def test_get_hint():
    puzzle = np.zeros((9, 9), dtype=int)
    solver = SudokuSolver(puzzle)
    hint = solver.get_hint()
    assert hint is not None
    row, col, value, message = hint
    assert 0 <= row < 9
    assert 0 <= col < 9
    assert 1 <= value <= 9
    assert isinstance(message, str)
