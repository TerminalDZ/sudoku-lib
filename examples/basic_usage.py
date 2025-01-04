"""
Basic usage example of the Sudoku library
"""

import numpy as np
from sudoku_lib import SudokuGame, SudokuSolver

def main():
    # Create a new game
    game = SudokuGame()
    
    # Generate a new puzzle
    puzzle = game.new_game(difficulty="medium")
    print("Generated Puzzle:")
    print(puzzle)
    
    # Create a solver
    solver = SudokuSolver(puzzle)
    
    # Solve the puzzle
    success, steps = solver.solve()
    
    if success:
        print("\nSolution:")
        print(solver.grid)
        print("\nSolving steps:")
        for step in steps:
            print(step)
    else:
        print("Could not solve the puzzle")
        
if __name__ == "__main__":
    main()
