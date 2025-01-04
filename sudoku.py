import numpy as np
import random

class SudokuGame:
    def __init__(self):
        self.current_puzzle = None
        self.solution = None
        
    def generate_puzzle(self, difficulty='medium'):
        # Create an empty 9x9 grid
        grid = np.zeros((9, 9), dtype=int)
        
        # Fill diagonal 3x3 boxes first (these are independent)
        for i in range(0, 9, 3):
            self._fill_box(grid, i, i)
            
        # Fill the rest of the grid
        self._solve_grid(grid)
        
        # Remove numbers according to difficulty
        self._remove_numbers(grid, difficulty)
        
        return grid.copy()
    
    def _fill_box(self, grid, row, col):
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        index = 0
        for i in range(3):
            for j in range(3):
                grid[row + i][col + j] = numbers[index]
                index += 1
    
    def _is_valid(self, grid, num, pos):
        # Check row
        for x in range(9):
            if grid[pos[0]][x] == num and pos[1] != x:
                return False
        
        # Check column
        for x in range(9):
            if grid[x][pos[1]] == num and pos[0] != x:
                return False
        
        # Check 3x3 box
        box_x = pos[1] // 3
        box_y = pos[0] // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if grid[i][j] == num and (i, j) != pos:
                    return False
        
        return True
    
    def _find_empty(self, grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return (i, j)
        return None
    
    def _solve_grid(self, grid):
        find = self._find_empty(grid)
        if not find:
            return True
            
        row, col = find
        for num in range(1, 10):
            if self._is_valid(grid, num, (row, col)):
                grid[row][col] = num
                
                if self._solve_grid(grid):
                    return True
                    
                grid[row][col] = 0
        return False
    
    def _remove_numbers(self, grid, difficulty):
        difficulties = {
            'easy': 30,
            'medium': 40,
            'hard': 50
        }
        
        cells_to_remove = difficulties.get(difficulty, 40)
        cells = [(i, j) for i in range(9) for j in range(9)]
        
        for _ in range(cells_to_remove):
            if not cells:
                break
            cell = random.choice(cells)
            cells.remove(cell)
            grid[cell[0]][cell[1]] = 0
    
    def new_game(self, difficulty='medium'):
        """Start a new game with the specified difficulty."""
        self.current_puzzle = self.generate_puzzle(difficulty)
        self.solution = self.current_puzzle.copy()
        self._solve_grid(self.solution)  # Keep a solved version
        return self.current_puzzle
    
    def make_move(self, row, col, num):
        """Make a move in the current puzzle."""
        if self.current_puzzle[row][col] != 0:
            return False
            
        if num == 0:  # Clear the cell
            self.current_puzzle[row][col] = 0
            return True
            
        # Check if the move is valid
        if self._is_valid(self.current_puzzle, num, (row, col)):
            self.current_puzzle[row][col] = num
            return True
            
        return False
    
    def is_complete(self):
        """Check if the puzzle is complete."""
        return not self._find_empty(self.current_puzzle)
    
    def get_solution(self):
        """Get the solution for the current puzzle."""
        return self.solution.copy()
