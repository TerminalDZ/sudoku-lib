# Sudoku Library

A comprehensive Python library for Sudoku puzzle generation, solving, and game management. This library provides both the core solving algorithms and a complete game implementation with GUI support.

## Features

### Core Library Features
- 🧩 Puzzle generation with multiple difficulty levels
- 🤖 Advanced solving algorithms
- 💾 Solution caching and persistence
- 📊 Player statistics tracking
- 💾 Game state saving/loading
- ✅ Solution verification

### GUI Application Features
- 🎮 Modern, intuitive interface
- 🎯 Multiple difficulty levels
- 🔢 Input validation
- 💡 Hint system
- 📈 Progress tracking

## Installation

```bash
pip install sudoku-lib
```

Or install from source:

```bash
git clone https://github.com/terminaldz/sudoku-lib
cd sudoku-lib
pip install -r requirements.txt
```

## Library Usage

### Basic Usage

```python
from sudoku_lib import SudokuGame, SudokuSolver
import numpy as np

# Create a new game
game = SudokuGame()
puzzle = game.new_game(difficulty="medium")

# Create a solver
solver = SudokuSolver(puzzle)

# Solve the puzzle
success, steps = solver.solve()
if success:
    print("Solution found!")
    print(solver.grid)
```

### Advanced Features

1. **Game State Management**:
```python
# Save game state
save_name = solver.save_game_state("player1", "my_save")

# Load game state
solver.load_game_state("player1", "my_save")

# Get saved games
saves = solver.get_saved_games("player1")
```

2. **Player Statistics**:
```python
# Get player stats
stats = solver.get_player_statistics("player1")
print(f"Total solved: {stats['total_solved']}")
print(f"Difficulty breakdown: {stats['difficulty_breakdown']}")
```

3. **Hint System**:
```python
# Get a hint
hint = solver.get_hint()
if hint:
    row, col, value, message = hint
    print(f"Hint: {message}")
```

## GUI Application

The library includes a complete GUI application built with PySide6:

```python
from sudoku_lib.gui import SudokuGUI
from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
window = SudokuGUI()
window.show()
sys.exit(app.exec())
```

## Modern Sudoku with AI Solver

A comprehensive Python library and application for Sudoku puzzle generation, solving, and gameplay. This project combines traditional Sudoku gameplay with advanced solving algorithms, providing both a powerful library and a sleek, user-friendly interface.

## Workflow

### CI/CD Pipelines

The project uses GitHub Actions for continuous integration and deployment:

#### Continuous Integration (`ci.yml`)
- Runs on every push and pull request to main branch
- Tests against Python 3.8, 3.9, 3.10, and 3.11
- Performs:
  - Code linting with flake8
  - Type checking with mypy
  - Unit tests with pytest
  - Code coverage reporting to Codecov

#### Security Scanning (`codeql.yml`)
- CodeQL analysis for security vulnerabilities
- Runs on push, pull requests, and weekly schedule
- Analyzes Python codebase for security issues

#### Publication (`publish.yml`)
- Triggered on release publication
- Builds and publishes package to PyPI
- Requires PyPI API token in repository secrets

### Development Workflow
1. **Setup Development Environment**
   ```bash
   # Clone the repository
   git clone https://github.com/terminaldz/sudoku-lib
   cd sudoku-lib
   
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install development dependencies
   pip install -e ".[dev]"
   ```

2. **Making Changes**
   - Create a new branch for your feature/fix
   - Write tests for new functionality
   - Ensure all tests pass locally
   - Update documentation as needed

3. **Code Quality**
   ```bash
   # Run linting
   flake8 sudoku_lib tests
   
   # Run type checking
   mypy sudoku_lib
   
   # Run tests with coverage
   pytest --cov=sudoku_lib tests/
   ```

4. **Submitting Changes**
   - Push changes to your fork
   - Create a pull request with a clear description
   - Ensure CI checks pass
   - Request review from maintainers

### Release Workflow
1. **Version Update**
   - Update version in `setup.py`
   - Update CHANGELOG.md
   - Create release notes

2. **Package Release**
   ```bash
   # Build distribution
   python -m build
   
   # Upload to PyPI
   python -m twine upload dist/*
   ```

## Features

#### Core Library Features
- 🧩 Puzzle generation with multiple difficulty levels
- 🤖 Advanced solving algorithms:
  - Naked Singles detection
  - Hidden Singles detection
  - Advanced backtracking algorithm
- 💾 Solution caching and persistence
- 📊 Player statistics tracking
- 💾 Game state saving/loading
- ✅ Solution verification

#### GUI Application Features
- 🎮 Modern, intuitive graphical interface
- 🎯 Three difficulty levels (Easy, Medium, Hard)
- 🔢 Input validation and error checking
- 💡 Smart hint system
- 📝 Step-by-step solution visualization
- 📈 Player statistics and history
- 💾 Progress saving and loading

## Installation

```bash
pip install sudoku-lib
```

Or install from source:

```bash
git clone https://github.com/terminaldz/sudoku-lib
cd sudoku-lib
pip install -r requirements.txt
```

## Library Usage

### Basic Usage

```python
from sudoku_lib import SudokuGame, SudokuSolver
import numpy as np

# Create a new game
game = SudokuGame()
puzzle = game.new_game(difficulty="medium")

# Create a solver
solver = SudokuSolver(puzzle)

# Solve the puzzle
success, steps = solver.solve()
if success:
    print("Solution found!")
    print(solver.grid)
```

### Advanced Features

1. **Game State Management**:
```python
# Save game state
save_name = solver.save_game_state("player1", "my_save")

# Load game state
solver.load_game_state("player1", "my_save")

# Get saved games
saves = solver.get_saved_games("player1")
```

2. **Player Statistics**:
```python
# Get player stats
stats = solver.get_player_statistics("player1")
print(f"Total solved: {stats['total_solved']}")
print(f"Difficulty breakdown: {stats['difficulty_breakdown']}")
```

3. **Hint System**:
```python
# Get a hint
hint = solver.get_hint()
if hint:
    row, col, value, message = hint
    print(f"Hint: {message}")
```

## GUI Application

Launch the graphical interface:

```python
python sudoku_gui.py
```

### Game Controls:
- Select difficulty level from dropdown
- Click "New Game" to start
- Click cells to select them
- Use number buttons or keyboard to input values
- Use "Clear" to remove numbers
- Click "Get Hint" for suggestions
- Use "Solve with AI" to see the complete solution

## Project Structure

```
sudoku_lib/
├── __init__.py
├── solver.py     # Core solving algorithms
├── game.py       # Game logic and generation
└── gui.py        # GUI implementation

examples/
└── basic_usage.py

tests/
└── test_sudoku.py
```

## Data Storage

Game data is stored in `sudoku_solutions.json` with the following structure:
```json
{
  "puzzles": {
    "puzzle_key": {
      "original": [...],
      "solutions": [...],
      "first_solved": "timestamp",
      "difficulty": "level"
    }
  },
  "saved_games": {
    "player_name": {
      "save_name": {
        "grid": [...],
        "original_grid": [...],
        "timestamp": "2025-01-04...",
        "used_hints": [],
        "difficulty": "medium"
      }
    }
  },
  "player_solutions": {
    "player_name": [...]
  }
}
```

## Dependencies

- Python 3.8+
- PySide6
- NumPy
- Requirements listed in `requirements.txt`

## Contributing

Contributions are welcome! Please feel free to submit pull requests or create issues for bugs and feature requests.

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

Created by Idriss Boukmouche

## API Documentation

### SudokuGame Class

```python
class SudokuGame:
    def new_game(difficulty: str) -> np.ndarray:
        """Generate a new puzzle with specified difficulty"""
        
    def verify_solution(grid: np.ndarray) -> Tuple[bool, list]:
        """Verify if solution is valid"""
```

### SudokuSolver Class

```python
class SudokuSolver:
    def solve() -> Tuple[bool, List[str]]:
        """Solve the puzzle and return steps"""
        
    def get_hint() -> Optional[Tuple[int, int, int, str]]:
        """Get next move hint"""
        
    def save_game_state(player_name: str, save_name: str) -> str:
        """Save current game state"""
        
    def load_game_state(player_name: str, save_name: str) -> bool:
        """Load saved game state"""
