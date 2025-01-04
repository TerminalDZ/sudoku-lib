# Sudoku AI Library

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Code Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen)

A comprehensive Python library for Sudoku puzzle generation, solving, and game management, featuring an AI-powered solver and a RESTful API.

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
- [Development](#development)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **🎮 Puzzle Generation**: Create Sudoku puzzles with varying difficulty levels
- **🤖 AI Solver**: Advanced algorithm for solving puzzles efficiently
- **🌐 REST API**: Complete HTTP API for puzzle operations
- **💡 Hint System**: Intelligent hint generation for next moves
- **✅ Validation**: Comprehensive puzzle validation and error checking
- **📊 Game Statistics**: Track solving progress and performance

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install from PyPI

```bash
pip install sudoku-iba-lib
```

### Install from Source

```bash
git clone https://github.com/terminaldz/sudoku-lib.git
cd sudoku-lib
pip install -e ".[dev]"
```

## 🎯 Quick Start

### Basic Usage

```python
from sudoku_lib.game import SudokuGame
from sudoku_lib.solver import SudokuSolver

# Create a new game
game = SudokuGame()
puzzle = game.new_game("medium")

# Solve the puzzle
solver = SudokuSolver(puzzle)
solution, steps = solver.solve()

# Get a hint
hint = solver.get_hint()
```

### GUI Application

```python
from sudoku_lib.gui import SudokuGUI

# Launch the GUI
app = SudokuGUI()
app.run()
```

## 🌐 API Reference

### Starting the API Server

```bash
# Development server
uvicorn sudoku_lib.api:app --reload

# Production server
uvicorn sudoku_lib.api:app --host 0.0.0.0 --port 8000
```

### Interactive Documentation

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### API Endpoints

#### Generate Puzzle

```python
import requests

# Get a medium difficulty puzzle
response = requests.get("http://localhost:8000/puzzle/medium")
puzzle = response.json()["puzzle"]
```

#### Solve Puzzle

```python
# Solve a puzzle
solution = requests.post(
    "http://localhost:8000/solve",
    json={"puzzle": puzzle}
).json()
```

#### Get Hint

```python
# Get next move hint
hint = requests.post(
    "http://localhost:8000/hint",
    json={"puzzle": puzzle}
).json()
```

#### Validate Solution

```python
# Check solution validity
result = requests.post(
    "http://localhost:8000/validate",
    json={"puzzle": solution}
).json()
```

For more examples, see [examples/api_usage.py](examples/api_usage.py).

## 🛠️ Development

### Project Structure

```
sudoku_lib/
├── api.py          # REST API implementation
├── game.py         # Core game logic
├── solver.py       # AI solver implementation


tests/
├── test_api.py     # API tests
├── test_game.py    # Game logic tests
└── test_solver.py  # Solver tests

examples/
├── basic_usage.py  # Basic library usage
└── api_usage.py    # API usage examples
```

### Setup Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows

# Install development dependencies
pip install -e ".[dev]"
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=sudoku_lib --cov-report=term-missing

# Run specific test file
pytest tests/test_api.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for all public functions
- Add tests for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

Idriss Boukmouche - boukemoucheidriss@gmail.com

Project Link: [https://github.com/terminaldz/sudoku-lib](https://github.com/terminaldz/sudoku-lib)

---

Made with ❤️ by [Idriss Boukmouche](https://github.com/terminaldz)

