"""
Sudoku API Module - Provides REST API endpoints for Sudoku game
"""

from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import numpy as np
from typing import List, Optional, Dict, Any
from .game import SudokuGame
from .solver import SudokuSolver

app = FastAPI(
    title="Sudoku API",
    description="""
    A professional Sudoku API with puzzle generation, solving, and hint capabilities.
    
    ## Features
    
    * Generate new Sudoku puzzles with different difficulty levels
    * Solve puzzles using advanced AI algorithms
    * Get intelligent hints for next moves
    * Validate puzzle solutions
    
    ## Usage Examples
    
    Check out our [GitHub repository](https://github.com/terminaldz/sudoku-lib) for detailed examples and documentation.
    """,
    version="1.0.0",
    contact={
        "name": "Idriss Boukmouche",
        "email": "boukemoucheidriss@gmail.com",
        "url": "https://github.com/terminaldz/sudoku-lib"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    openapi_tags=[
        {
            "name": "puzzles",
            "description": "Operations for generating and managing Sudoku puzzles"
        },
        {
            "name": "solver",
            "description": "Puzzle solving and hint generation"
        },
        {
            "name": "validation",
            "description": "Solution validation and verification"
        }
    ]
)

# CORS middleware configuration
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

class SudokuGrid(BaseModel):
    """Pydantic model for Sudoku grid"""
    puzzle: List[List[int]] = Field(
        ...,
        description="9x9 grid where 0 represents empty cells",
        example=[
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
    )

def grid_to_list(grid: np.ndarray) -> List[List[int]]:
    """Convert numpy array to list of lists"""
    return grid.tolist()

def list_to_grid(puzzle_list: List[List[int]]) -> np.ndarray:
    """Convert list of lists to numpy array"""
    return np.array(puzzle_list)

@app.get("/",
    tags=["info"],
    summary="API Information",
    description="Get basic information about the API and available endpoints"
)
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Sudoku API",
        "version": "1.0.0",
        "endpoints": [
            "GET /puzzle/{difficulty}",
            "POST /solve",
            "POST /validate",
            "GET /hint"
        ]
    }

@app.get("/puzzle/{difficulty}",
    tags=["puzzles"],
    summary="Generate New Puzzle",
    description="""
    Generate a new Sudoku puzzle with the specified difficulty level.
    
    Available difficulty levels:
    * easy: 30 empty cells
    * medium: 40 empty cells
    * hard: 50 empty cells
    """
)
async def get_puzzle(difficulty: str):
    """Generate a new Sudoku puzzle with the specified difficulty level."""
    if difficulty not in ["easy", "medium", "hard"]:
        raise HTTPException(status_code=400, detail="Invalid difficulty level")
        
    try:
        sudoku = SudokuGame()
        puzzle = sudoku.new_game(difficulty)
        return {
            "puzzle": grid_to_list(puzzle),
            "difficulty": difficulty
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/solve",
    tags=["solver"],
    summary="Solve Puzzle",
    description="Solve a Sudoku puzzle and return the solution with steps"
)
async def solve_puzzle(grid: SudokuGrid):
    """Solve a Sudoku puzzle."""
    try:
        solver = SudokuSolver(np.array(grid.puzzle))
        success, steps = solver.solve()
        if success:
            solution = solver.grid.tolist()
            return {
                "solution": solution,
                "steps": steps,
                "is_valid": True
            }
        raise HTTPException(status_code=400, detail="No solution exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/hint",
    tags=["solver"],
    summary="Get Hint",
    description="Get a hint for the next move in the puzzle"
)
async def get_hint(grid: SudokuGrid):
    """Get a hint for the next move in a Sudoku puzzle."""
    try:
        solver = SudokuSolver(np.array(grid.puzzle))
        hint = solver.get_hint()
        if hint:
            row, col, value, message = hint
            return {
                "row": int(row),
                "col": int(col),
                "value": int(value),
                "message": message
            }
        raise HTTPException(status_code=400, detail="No hints available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/validate",
    tags=["validation"],
    summary="Validate Solution",
    description="Validate a completed Sudoku puzzle solution"
)
async def validate_solution(grid: SudokuGrid):
    """Validate a Sudoku puzzle solution."""
    try:
        # Convert grid to numpy array
        grid_array = np.array(grid.puzzle)
        errors = []
        
        # Check if grid is complete (no zeros)
        if 0 in grid_array:
            errors.append("Grid is incomplete")
            return {"is_valid": False, "errors": errors}
            
        # Check rows
        for i, row in enumerate(grid_array):
            if len(set(row)) != 9:
                errors.append(f"Invalid row {i+1}")
                
        # Check columns
        for i, col in enumerate(grid_array.T):
            if len(set(col)) != 9:
                errors.append(f"Invalid column {i+1}")
                
        # Check 3x3 boxes
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                box = grid_array[i:i+3, j:j+3].flatten()
                if len(set(box)) != 9:
                    errors.append(f"Invalid 3x3 box at position ({i//3+1}, {j//3+1})")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
