import numpy as np
import json
import os
from typing import List, Tuple, Set, Optional, Dict
from datetime import datetime

class SudokuSolver:
    DEFAULT_STRUCTURE = {
        "puzzles": {},
        "history": [],
        "player_solutions": {},
        "saved_games": {}
    }

    def __init__(self, grid: np.ndarray):
        self.grid = grid.copy()
        self.original_grid = grid.copy()
        self.used_hints = set()
        self.solutions_file = "sudoku_solutions.json"
        self.solutions_data = self.load_solutions_data()
        
    def load_solutions_data(self) -> Dict:
        """Load all solutions data from file."""
        if os.path.exists(self.solutions_file):
            try:
                with open(self.solutions_file, 'r') as f:
                    data = json.load(f)
                    # Ensure all required keys exist
                    for key in self.DEFAULT_STRUCTURE:
                        if key not in data:
                            data[key] = self.DEFAULT_STRUCTURE[key]
                    return data
            except:
                return self.DEFAULT_STRUCTURE.copy()
        
        # Create new file with default structure
        data = self.DEFAULT_STRUCTURE.copy()
        self.save_solutions_data(data)
        return data
        
    def save_solutions_data(self, data=None):
        """Save all solutions data to file."""
        if data is None:
            data = self.solutions_data
        try:
            with open(self.solutions_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving solutions data: {e}")
            
    def grid_to_key(self, grid: np.ndarray) -> str:
        """Convert grid to a string key for caching."""
        return ','.join(map(str, grid.flatten()))
        
    def save_puzzle_state(self, puzzle_type: str = "ai_solution", player_name: str = "AI", difficulty: str = "unknown"):
        """Save current puzzle state with metadata."""
        try:
            grid_key = self.grid_to_key(self.original_grid)
            current_time = datetime.now().isoformat()
            
            # Ensure puzzles key exists
            if "puzzles" not in self.solutions_data:
                self.solutions_data["puzzles"] = {}
            
            # Save the puzzle and its solution
            if grid_key not in self.solutions_data["puzzles"]:
                self.solutions_data["puzzles"][grid_key] = {
                    "original": self.original_grid.tolist(),
                    "solutions": [],
                    "first_solved": current_time,
                    "difficulty": difficulty
                }
                
            # Add this solution if it's unique
            solution_key = self.grid_to_key(self.grid)
            solution_entry = {
                "grid": self.grid.tolist(),
                "solver": player_name,
                "timestamp": current_time,
                "type": puzzle_type
            }
            
            # Ensure solutions list exists
            if "solutions" not in self.solutions_data["puzzles"][grid_key]:
                self.solutions_data["puzzles"][grid_key]["solutions"] = []
            
            if solution_key not in [self.grid_to_key(np.array(s["grid"])) 
                                  for s in self.solutions_data["puzzles"][grid_key]["solutions"]]:
                self.solutions_data["puzzles"][grid_key]["solutions"].append(solution_entry)
            
            # Ensure history exists
            if "history" not in self.solutions_data:
                self.solutions_data["history"] = []
            
            # Add to history
            history_entry = {
                "puzzle_key": grid_key,
                "solution_key": solution_key,
                "timestamp": current_time,
                "player": player_name,
                "type": puzzle_type,
                "difficulty": difficulty
            }
            self.solutions_data["history"].append(history_entry)
            
            # Ensure player_solutions exists
            if "player_solutions" not in self.solutions_data:
                self.solutions_data["player_solutions"] = {}
            
            # Save player-specific solutions
            if player_name != "AI":
                if player_name not in self.solutions_data["player_solutions"]:
                    self.solutions_data["player_solutions"][player_name] = []
                self.solutions_data["player_solutions"][player_name].append(history_entry)
            
            self.save_solutions_data()
        except Exception as e:
            print(f"Error saving puzzle state: {e}")
        
    def get_puzzle_history(self, puzzle_key: Optional[str] = None, 
                          player_name: Optional[str] = None) -> List[Dict]:
        """Get history of solutions for a specific puzzle or player."""
        history = self.solutions_data["history"]
        
        if puzzle_key:
            history = [h for h in history if h["puzzle_key"] == puzzle_key]
        if player_name:
            history = [h for h in history if h["player"] == player_name]
            
        return sorted(history, key=lambda x: x["timestamp"], reverse=True)
        
    def get_player_statistics(self, player_name: str) -> Dict:
        """Get statistics for a specific player."""
        player_history = self.get_puzzle_history(player_name=player_name)
        
        return {
            "total_puzzles_solved": len(player_history),
            "puzzles_by_difficulty": {
                diff: len([h for h in player_history if h["difficulty"] == diff])
                for diff in ["easy", "medium", "hard"]
            },
            "solution_dates": [h["timestamp"] for h in player_history]
        }

    def get_possible_values(self, row: int, col: int) -> Set[int]:
        """Get all possible values for a cell."""
        if self.grid[row][col] != 0:
            return set()
            
        values = set(range(1, 10))
        
        # Check row
        values -= set(self.grid[row])
        
        # Check column
        values -= set(self.grid[:, col])
        
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        box = self.grid[box_row:box_row + 3, box_col:box_col + 3]
        values -= set(box.flatten())
        
        return values
        
    def get_cell_candidates(self) -> List[Tuple[int, int, Set[int]]]:
        """Get all empty cells and their possible values."""
        candidates = []
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    possible = self.get_possible_values(i, j)
                    if possible:
                        candidates.append((i, j, possible))
        return candidates
        
    def solve(self) -> Tuple[bool, List[str]]:
        """Solve the puzzle using multiple strategies and caching."""
        grid_key = self.grid_to_key(self.original_grid)
        
        # Check if solution exists in cache
        if grid_key in self.solutions_data["puzzles"]:
            cached = self.solutions_data["puzzles"][grid_key]["solutions"][0]
            self.grid = np.array(cached['grid'])
            return True, [f"Found cached solution for puzzle {grid_key}"]
            
        steps = []
        original_grid = self.grid.copy()
        
        # Try logical solving methods first
        changed = True
        while changed:
            changed = False
            
            # Try naked singles
            for row, col, values in self.get_cell_candidates():
                if len(values) == 1:
                    value = values.pop()
                    self.grid[row][col] = value
                    steps.append(f"Found naked single {value} at row {row+1}, column {col+1}")
                    changed = True
                    
            # Try hidden singles
            if not changed:
                for row in range(9):
                    for num in range(1, 10):
                        if num not in self.grid[row]:
                            possible_cols = []
                            for col in range(9):
                                if self.grid[row][col] == 0 and num in self.get_possible_values(row, col):
                                    possible_cols.append(col)
                            if len(possible_cols) == 1:
                                col = possible_cols[0]
                                self.grid[row][col] = num
                                steps.append(f"Found hidden single {num} at row {row+1}, column {col+1}")
                                changed = True
                                
        # If logical methods don't complete the solution, use backtracking
        if np.any(self.grid == 0):
            steps.append("Using backtracking algorithm to complete the solution")
            if self._solve_backtracking(steps):
                steps.append("Solution found!")
                # Cache the solution
                self.save_puzzle_state()
                return True, steps
            else:
                self.grid = original_grid
                return False, steps
        
        # Cache the solution
        self.save_puzzle_state()
        return True, steps
        
    def _solve_backtracking(self, steps: List[str]) -> bool:
        """Backtracking algorithm with step recording."""
        empty = self._find_empty()
        if not empty:
            return True
            
        row, col = empty
        for num in range(1, 10):
            if self._is_valid(num, (row, col)):
                self.grid[row][col] = num
                steps.append(f"Trying {num} at row {row+1}, column {col+1}")
                
                if self._solve_backtracking(steps):
                    return True
                    
                self.grid[row][col] = 0
                steps.append(f"Backtracking: removing {num} from row {row+1}, column {col+1}")
                
        return False
        
    def _find_empty(self) -> Optional[Tuple[int, int]]:
        """Find an empty cell."""
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None
        
    def _is_valid(self, num: int, pos: Tuple[int, int]) -> bool:
        """Check if a number is valid in a given position."""
        # Check row
        for i in range(9):
            if self.grid[pos[0]][i] == num and pos[1] != i:
                return False
            
        # Check column
        for i in range(9):
            if self.grid[i][pos[1]] == num and pos[0] != i:
                return False
            
        # Check 3x3 box
        box_x = pos[1] // 3
        box_y = pos[0] // 3
        
        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x * 3, box_x*3 + 3):
                if self.grid[i][j] == num and (i,j) != pos:
                    return False
                    
        return True
        
    def validate_solution(self) -> Tuple[bool, List[str]]:
        """Validate the entire solution and return detailed feedback."""
        errors = []
        
        # Check rows
        for i in range(9):
            row = self.grid[i]
            if len(set(row)) != 9 or 0 in row:
                missing = set(range(1, 10)) - set(row)
                duplicates = [n for n in range(1, 10) if list(row).count(n) > 1]
                if duplicates:
                    errors.append(f"Row {i+1} contains duplicate numbers: {duplicates}")
                if missing and 0 not in row:
                    errors.append(f"Row {i+1} is missing numbers: {missing}")

        # Check columns
        for j in range(9):
            col = self.grid[:, j]
            if len(set(col)) != 9 or 0 in col:
                missing = set(range(1, 10)) - set(col)
                duplicates = [n for n in range(1, 10) if list(col).count(n) > 1]
                if duplicates:
                    errors.append(f"Column {j+1} contains duplicate numbers: {duplicates}")
                if missing and 0 not in col:
                    errors.append(f"Column {j+1} is missing numbers: {missing}")

        # Check 3x3 boxes
        for box_i in range(3):
            for box_j in range(3):
                box = self.grid[box_i*3:(box_i+1)*3, box_j*3:(box_j+1)*3].flatten()
                if len(set(box)) != 9 or 0 in box:
                    missing = set(range(1, 10)) - set(box)
                    duplicates = [n for n in range(1, 10) if list(box).count(n) > 1]
                    if duplicates:
                        errors.append(f"Box at position ({box_i+1},{box_j+1}) contains duplicate numbers: {duplicates}")
                    if missing and 0 not in box:
                        errors.append(f"Box at position ({box_i+1},{box_j+1}) is missing numbers: {missing}")

        # Check if puzzle is complete
        if np.any(self.grid == 0):
            errors.append("Puzzle is not complete - contains empty cells")

        return len(errors) == 0, errors

    def check_move(self, row: int, col: int, num: int) -> Tuple[bool, str]:
        """Check if a move is valid and return detailed feedback."""
        if self.grid[row][col] == num:
            return True, "Number already placed here"

        # Check row
        if num in self.grid[row]:
            return False, f"Number {num} already exists in row {row+1}"

        # Check column
        if num in self.grid[:, col]:
            return False, f"Number {num} already exists in column {col+1}"

        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        box = self.grid[box_row:box_row + 3, box_col:box_col + 3]
        if num in box:
            return False, f"Number {num} already exists in this 3x3 box"

        return True, "Valid move"

    def get_hint(self) -> Optional[Tuple[int, int, int, str]]:
        """Get a hint for the next move, avoiding previously hinted cells."""
        original_grid = self.grid.copy()
        
        # Try naked singles first (avoiding used hints)
        candidates = self.get_cell_candidates()
        for row, col, values in candidates:
            if len(values) == 1 and (row, col) not in self.used_hints:
                value = values.pop()
                self.used_hints.add((row, col))  # Mark this cell as used for hints
                return row, col, value, "This cell can only be {}".format(value)
                
        # Try hidden singles (avoiding used hints)
        for row in range(9):
            for num in range(1, 10):
                if num not in self.grid[row]:
                    possible_cols = []
                    for col in range(9):
                        if self.grid[row][col] == 0 and (row, col) not in self.used_hints and num in self.get_possible_values(row, col):
                            possible_cols.append(col)
                    if len(possible_cols) == 1:
                        col = possible_cols[0]
                        self.used_hints.add((row, col))  # Mark this cell as used for hints
                        return row, col, num, "Only this cell in row {} can be {}".format(row + 1, num)
                        
        # If no logical hints found, solve the puzzle and give the first different cell not previously hinted
        if self.solve()[0]:
            for i in range(9):
                for j in range(9):
                    if original_grid[i][j] == 0 and self.grid[i][j] != 0 and (i, j) not in self.used_hints:
                        self.used_hints.add((i, j))  # Mark this cell as used for hints
                        return i, j, self.grid[i][j], "Try {} here".format(self.grid[i][j])
                        
        return None

    def save_game_state(self, player_name: str, save_name: str = None):
        """Save current game state with a name."""
        if "saved_games" not in self.solutions_data:
            self.solutions_data["saved_games"] = {}
            
        if player_name not in self.solutions_data["saved_games"]:
            self.solutions_data["saved_games"][player_name] = {}
            
        current_time = datetime.now().isoformat()
        save_name = save_name or f"Save_{current_time}"
        
        save_state = {
            "grid": self.grid.tolist(),
            "original_grid": self.original_grid.tolist(),
            "timestamp": current_time,
            "used_hints": list(self.used_hints),
            "difficulty": self.solutions_data.get("puzzles", {})
                .get(self.grid_to_key(self.original_grid), {})
                .get("difficulty", "unknown")
        }
        
        self.solutions_data["saved_games"][player_name][save_name] = save_state
        self.save_solutions_data()
        return save_name
        
    def load_game_state(self, player_name: str, save_name: str) -> bool:
        """Load a saved game state."""
        try:
            if (player_name in self.solutions_data.get("saved_games", {}) and
                save_name in self.solutions_data["saved_games"][player_name]):
                
                save_state = self.solutions_data["saved_games"][player_name][save_name]
                self.grid = np.array(save_state["grid"])
                self.original_grid = np.array(save_state["original_grid"])
                self.used_hints = set(save_state["used_hints"])
                return True
        except Exception as e:
            print(f"Error loading game state: {e}")
        return False
        
    def get_saved_games(self, player_name: str) -> List[Dict]:
        """Get list of saved games for a player."""
        if player_name in self.solutions_data.get("saved_games", {}):
            saves = self.solutions_data["saved_games"][player_name]
            return [
                {
                    "name": name,
                    "timestamp": state["timestamp"],
                    "difficulty": state["difficulty"],
                    "progress": np.count_nonzero(np.array(state["grid"])) / 81 * 100
                }
                for name, state in saves.items()
            ]
        return []
        
    def delete_saved_game(self, player_name: str, save_name: str) -> bool:
        """Delete a saved game."""
        try:
            if (player_name in self.solutions_data.get("saved_games", {}) and
                save_name in self.solutions_data["saved_games"][player_name]):
                
                del self.solutions_data["saved_games"][player_name][save_name]
                self.save_solutions_data()
                return True
        except Exception as e:
            print(f"Error deleting saved game: {e}")
        return False
