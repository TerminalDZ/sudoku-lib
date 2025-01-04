"""
Sudoku Solver Module - Provides advanced Sudoku solving capabilities
"""

import numpy as np
import json
import os
from typing import List, Tuple, Set, Optional, Dict
from datetime import datetime

class SudokuSolver:
    """A powerful Sudoku solver with multiple solving strategies and solution storage."""
    
    DEFAULT_STRUCTURE = {
        "puzzles": {},
        "history": [],
        "player_solutions": {},
        "saved_games": {}
    }

    def __init__(self, grid: np.ndarray, solutions_file: str = None):
        """
        Initialize the Sudoku solver.
        
        Args:
            grid (np.ndarray): Initial Sudoku grid (9x9)
            solutions_file (str, optional): Path to solutions storage file
        """
        self.grid = grid.copy()
        self.original_grid = grid.copy()
        self.used_hints = set()
        self.solutions_file = solutions_file or "sudoku_solutions.json"
        self.solutions_data = self.load_solutions_data()
        
    def load_solutions_data(self) -> Dict:
        """Load solutions data from file."""
        if os.path.exists(self.solutions_file):
            try:
                with open(self.solutions_file, 'r') as f:
                    data = json.load(f)
                    for key in self.DEFAULT_STRUCTURE:
                        if key not in data:
                            data[key] = self.DEFAULT_STRUCTURE[key]
                    return data
            except:
                return self.DEFAULT_STRUCTURE.copy()
        
        data = self.DEFAULT_STRUCTURE.copy()
        self.save_solutions_data(data)
        return data
        
    def save_solutions_data(self, data=None):
        """Save solutions data to file."""
        if data is None:
            data = self.solutions_data
        try:
            with open(self.solutions_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving solutions data: {e}")
            
    def grid_to_key(self, grid: np.ndarray) -> str:
        """Convert grid to string key for storage."""
        return ','.join(map(str, grid.flatten()))
        
    def save_puzzle_state(self, puzzle_type: str = "ai_solution", 
                         player_name: str = "AI", 
                         difficulty: str = "unknown"):
        """
        Save current puzzle state with metadata.
        
        Args:
            puzzle_type (str): Type of solution (ai_solution/player_solution)
            player_name (str): Name of the solver
            difficulty (str): Puzzle difficulty level
        """
        try:
            grid_key = self.grid_to_key(self.original_grid)
            current_time = datetime.now().isoformat()
            
            if "puzzles" not in self.solutions_data:
                self.solutions_data["puzzles"] = {}
            
            if grid_key not in self.solutions_data["puzzles"]:
                self.solutions_data["puzzles"][grid_key] = {
                    "original": self.original_grid.tolist(),
                    "solutions": [],
                    "first_solved": current_time,
                    "difficulty": difficulty
                }
                
            solution_key = self.grid_to_key(self.grid)
            solution_entry = {
                "grid": self.grid.tolist(),
                "solver": player_name,
                "timestamp": current_time,
                "type": puzzle_type
            }
            
            if "solutions" not in self.solutions_data["puzzles"][grid_key]:
                self.solutions_data["puzzles"][grid_key]["solutions"] = []
            
            if solution_key not in [self.grid_to_key(np.array(s["grid"])) 
                                  for s in self.solutions_data["puzzles"][grid_key]["solutions"]]:
                self.solutions_data["puzzles"][grid_key]["solutions"].append(solution_entry)
            
            if "history" not in self.solutions_data:
                self.solutions_data["history"] = []
            
            history_entry = {
                "puzzle_key": grid_key,
                "solution_key": solution_key,
                "timestamp": current_time,
                "player": player_name,
                "type": puzzle_type,
                "difficulty": difficulty
            }
            self.solutions_data["history"].append(history_entry)
            
            if "player_solutions" not in self.solutions_data:
                self.solutions_data["player_solutions"] = {}
            
            if player_name != "AI":
                if player_name not in self.solutions_data["player_solutions"]:
                    self.solutions_data["player_solutions"][player_name] = []
                self.solutions_data["player_solutions"][player_name].append(history_entry)
            
            self.save_solutions_data()
        except Exception as e:
            print(f"Error saving puzzle state: {e}")
            
    def save_game_state(self, player_name: str, save_name: str = None) -> str:
        """
        Save current game state.
        
        Args:
            player_name (str): Player's name
            save_name (str, optional): Custom save name
            
        Returns:
            str: Name of the save
        """
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
        """
        Load a saved game state.
        
        Args:
            player_name (str): Player's name
            save_name (str): Name of the save to load
            
        Returns:
            bool: True if loaded successfully
        """
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
        """
        Get list of saved games for a player.
        
        Args:
            player_name (str): Player's name
            
        Returns:
            List[Dict]: List of save game metadata
        """
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
        """
        Delete a saved game.
        
        Args:
            player_name (str): Player's name
            save_name (str): Name of the save to delete
            
        Returns:
            bool: True if deleted successfully
        """
        try:
            if (player_name in self.solutions_data.get("saved_games", {}) and
                save_name in self.solutions_data["saved_games"][player_name]):
                
                del self.solutions_data["saved_games"][player_name][save_name]
                self.save_solutions_data()
                return True
        except Exception as e:
            print(f"Error deleting saved game: {e}")
        return False
        
    def get_puzzle_history(self, puzzle_key: Optional[str] = None, 
                          player_name: Optional[str] = None) -> List[Dict]:
        """
        Get puzzle solving history.
        
        Args:
            puzzle_key (str, optional): Specific puzzle to get history for
            player_name (str, optional): Specific player's history
            
        Returns:
            List[Dict]: List of historical puzzle solutions
        """
        history = self.solutions_data["history"]
        if puzzle_key:
            history = [h for h in history if h["puzzle_key"] == puzzle_key]
        if player_name:
            history = [h for h in history if h["player"] == player_name]
        return history
        
    def get_player_statistics(self, player_name: str) -> Dict:
        """
        Get player's solving statistics.
        
        Args:
            player_name (str): Player's name
            
        Returns:
            Dict: Player statistics
        """
        player_history = self.get_puzzle_history(player_name=player_name)
        total_solved = len(player_history)
        
        difficulty_counts = {
            "easy": len([h for h in player_history if h["difficulty"] == "easy"]),
            "medium": len([h for h in player_history if h["difficulty"] == "medium"]),
            "hard": len([h for h in player_history if h["difficulty"] == "hard"])
        }
        
        return {
            "total_solved": total_solved,
            "difficulty_breakdown": difficulty_counts,
            "recent_games": player_history[-10:]  # Last 10 games
        }
        
    def solve(self) -> Tuple[bool, List[str]]:
        """
        Solve the Sudoku puzzle.
        
        Returns:
            Tuple[bool, List[str]]: (Success status, Solution steps)
        """
        grid_key = self.grid_to_key(self.original_grid)
        if grid_key in self.solutions_data["puzzles"]:
            # Load cached solution
            solution = self.solutions_data["puzzles"][grid_key]["solutions"][0]["grid"]
            self.grid = np.array(solution)
            return True, ["Using cached solution"]
            
        steps = []
        if self._solve_step_by_step(0, 0, steps):
            self.save_puzzle_state()
            return True, steps
        return False, steps
        
    def _solve_step_by_step(self, row: int, col: int, steps: List[str]) -> bool:
        """
        Recursive solving algorithm with step tracking.
        
        Args:
            row (int): Current row
            col (int): Current column
            steps (List[str]): List to store solving steps
            
        Returns:
            bool: True if solution found
        """
        if col == 9:
            row += 1
            col = 0
        if row == 9:
            return True
            
        if self.grid[row][col] != 0:
            return self._solve_step_by_step(row, col + 1, steps)
            
        for num in range(1, 10):
            if self._is_safe(row, col, num):
                self.grid[row][col] = num
                steps.append(f"Try {num} at position ({row+1}, {col+1})")
                
                if self._solve_step_by_step(row, col + 1, steps):
                    return True
                    
                self.grid[row][col] = 0
                steps.append(f"Backtrack: Remove {num} from ({row+1}, {col+1})")
                
        return False
        
    def _is_safe(self, row: int, col: int, num: int) -> bool:
        """
        Check if number can be placed at position.
        
        Args:
            row (int): Row to check
            col (int): Column to check
            num (int): Number to check
            
        Returns:
            bool: True if placement is valid
        """
        # Check row
        if num in self.grid[row]:
            return False
            
        # Check column
        if num in self.grid[:, col]:
            return False
            
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.grid[i][j] == num:
                    return False
                    
        return True
        
    def get_hint(self) -> Optional[Tuple[int, int, int, str]]:
        """
        Get a hint for the next move.
        
        Returns:
            Optional[Tuple[int, int, int, str]]: (Row, Column, Value, Hint message)
        """
        # Try to solve the puzzle
        original_grid = self.grid.copy()
        if self.solve()[0]:
            solution = self.grid.copy()
            self.grid = original_grid
            
            # Find first difference
            for i in range(9):
                for j in range(9):
                    if self.grid[i][j] == 0 and solution[i][j] != 0:
                        self.used_hints.add((i, j))
                        return i, j, solution[i][j], f"Try {solution[i][j]} here"
                        
        return None
