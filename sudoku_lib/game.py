"""
Sudoku Game Module - Provides game logic and puzzle generation
"""

import numpy as np
from typing import Optional, Tuple
import random

class SudokuGame:
    """A Sudoku game manager with puzzle generation and validation."""
    
    def __init__(self):
        """Initialize the Sudoku game."""
        self.current_puzzle = None
        self.original_puzzle = None
        
    def new_game(self, difficulty: str = "medium") -> np.ndarray:
        """
        Generate a new Sudoku puzzle.
        
        Args:
            difficulty (str): Puzzle difficulty (easy/medium/hard)
            
        Returns:
            np.ndarray: Generated puzzle
        """
        # Generate a complete solution
        solution = self._generate_solution()
        
        # Remove numbers based on difficulty
        cells_to_remove = {
            "easy": 30,
            "medium": 40,
            "hard": 50
        }.get(difficulty.lower(), 40)
        
        puzzle = solution.copy()
        positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(positions)
        
        for i, j in positions[:cells_to_remove]:
            puzzle[i][j] = 0
            
        self.current_puzzle = puzzle.copy()
        self.original_puzzle = puzzle.copy()
        return puzzle
        
    def _generate_solution(self) -> np.ndarray:
        """
        Generate a complete valid Sudoku solution.
        
        Returns:
            np.ndarray: Complete Sudoku solution
        """
        grid = np.zeros((9, 9), dtype=int)
        
        # Fill diagonal boxes first (they are independent)
        for i in range(0, 9, 3):
            self._fill_box(grid, i, i)
            
        # Fill the rest
        self._solve_grid(grid)
        return grid
        
    def _fill_box(self, grid: np.ndarray, row: int, col: int):
        """
        Fill a 3x3 box with random numbers.
        
        Args:
            grid (np.ndarray): Grid to fill
            row (int): Starting row of box
            col (int): Starting column of box
        """
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        pos = 0
        
        for i in range(3):
            for j in range(3):
                grid[row + i][col + j] = numbers[pos]
                pos += 1
                
    def _solve_grid(self, grid: np.ndarray) -> bool:
        """
        Solve the grid using backtracking.
        
        Args:
            grid (np.ndarray): Grid to solve
            
        Returns:
            bool: True if solution found
        """
        empty = self._find_empty(grid)
        if not empty:
            return True
            
        row, col = empty
        for num in range(1, 10):
            if self._is_safe(grid, row, col, num):
                grid[row][col] = num
                
                if self._solve_grid(grid):
                    return True
                    
                grid[row][col] = 0
                
        return False
        
    def _find_empty(self, grid: np.ndarray) -> Optional[Tuple[int, int]]:
        """
        Find an empty cell in the grid.
        
        Args:
            grid (np.ndarray): Grid to search
            
        Returns:
            Optional[Tuple[int, int]]: Position of empty cell
        """
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return (i, j)
        return None
        
    def _is_safe(self, grid: np.ndarray, row: int, col: int, num: int) -> bool:
        """
        Check if number can be placed at position.
        
        Args:
            grid (np.ndarray): Grid to check
            row (int): Row to check
            col (int): Column to check
            num (int): Number to check
            
        Returns:
            bool: True if placement is valid
        """
        # Check row
        if num in grid[row]:
            return False
            
        # Check column
        if num in grid[:, col]:
            return False
            
        # Check box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if grid[i][j] == num:
                    return False
                    
        return True
        
    def verify_solution(self, grid: Optional[np.ndarray] = None) -> Tuple[bool, list]:
        """
        Verify if current grid state is valid.
        
        Args:
            grid (np.ndarray, optional): Grid to verify
            
        Returns:
            Tuple[bool, list]: (Is valid, List of errors)
        """
        if grid is None:
            grid = self.current_puzzle
            
        errors = []
        
        # Check rows
        for i in range(9):
            row = grid[i][grid[i] != 0]
            if len(row) != len(set(row)):
                errors.append(f"Row {i+1} contains duplicate numbers")
                
        # Check columns
        for j in range(9):
            col = grid[:, j][grid[:, j] != 0]
            if len(col) != len(set(col)):
                errors.append(f"Column {j+1} contains duplicate numbers")
                
        # Check boxes
        for box in range(9):
            row_start = (box // 3) * 3
            col_start = (box % 3) * 3
            box_values = []
            
            for i in range(row_start, row_start + 3):
                for j in range(col_start, col_start + 3):
                    if grid[i][j] != 0:
                        box_values.append(grid[i][j])
                        
            if len(box_values) != len(set(box_values)):
                errors.append(f"Box at ({row_start//3+1}, {col_start//3+1}) contains duplicate numbers")
                
        return len(errors) == 0, errors
