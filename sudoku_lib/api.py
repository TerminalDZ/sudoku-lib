"""
Sudoku API Module - Provides REST API endpoints for Sudoku game
"""

from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field
import numpy as np
from typing import List, Optional, Dict, Any
from .game import SudokuGame
from .solver import SudokuSolver

app = FastAPI(
    title="Sudoku API",
    description="""
    A comprehensive REST API for Sudoku puzzle generation, solving, and game management.
    
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

class SudokuGrid(BaseModel):
    """A 9x9 Sudoku grid"""
    grid: List[List[int]] = Field(
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

class PuzzleResponse(BaseModel):
    """Response model for puzzle generation"""
    puzzle: List[List[int]] = Field(..., description="Generated Sudoku puzzle")
    difficulty: str = Field(..., description="Puzzle difficulty level")

class SolutionRequest(BaseModel):
    """Request model for puzzle solving"""
    puzzle: List[List[int]] = Field(..., description="Puzzle to solve")

class SolutionResponse(BaseModel):
    """Response model for puzzle solution"""
    solution: List[List[int]] = Field(..., description="Solved puzzle")
    steps: List[str] = Field(..., description="Solution steps")
    is_valid: bool = Field(..., description="Whether the solution is valid")

class HintResponse(BaseModel):
    """Response model for hints"""
    row: int = Field(..., description="Row index (0-8)")
    col: int = Field(..., description="Column index (0-8)")
    value: int = Field(..., description="Value to place (1-9)")
    message: str = Field(..., description="Hint message")

class ValidationResponse(BaseModel):
    """Response model for solution validation"""
    is_valid: bool = Field(..., description="Whether the solution is valid")
    errors: List[str] = Field(..., description="List of validation errors")

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
    response_model=PuzzleResponse,
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
async def get_puzzle(
    difficulty: str = Path(
        ...,
        description="Puzzle difficulty level",
        example="medium",
        regex="^(easy|medium|hard)$"
    )
):
    """Generate a new Sudoku puzzle with specified difficulty"""
    try:
        game = SudokuGame()
        puzzle = game.new_game(difficulty)
        return {
            "puzzle": grid_to_list(puzzle),
            "difficulty": difficulty
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/solve",
    response_model=SolutionResponse,
    tags=["solver"],
    summary="Solve Puzzle",
    description="Solve a Sudoku puzzle using advanced solving algorithms"
)
async def solve_puzzle(request: SolutionRequest):
    """Solve a Sudoku puzzle"""
    puzzle = list_to_grid(request.puzzle)
    solver = SudokuSolver(puzzle)
    success, steps = solver.solve()
    
    if not success:
        raise HTTPException(
            status_code=400,
            detail="No solution exists for this puzzle"
        )
    
    return {
        "solution": grid_to_list(solver.grid),
        "steps": steps,
        "is_valid": True
    }

@app.post("/validate",
    response_model=ValidationResponse,
    tags=["validation"],
    summary="Validate Solution",
    description="Check if a Sudoku puzzle solution is valid"
)
async def validate_puzzle(request: SolutionRequest):
    """Validate a Sudoku puzzle solution"""
    puzzle = list_to_grid(request.puzzle)
    game = SudokuGame()
    is_valid, errors = game.verify_solution(puzzle)
    
    return {
        "is_valid": is_valid,
        "errors": errors
    }

@app.post("/hint",
    response_model=HintResponse,
    tags=["solver"],
    summary="Get Hint",
    description="Get a hint for the next move in the puzzle"
)
async def get_hint(request: SolutionRequest):
    """Get a hint for the next move"""
    puzzle = list_to_grid(request.puzzle)
    solver = SudokuSolver(puzzle)
    hint = solver.get_hint()
    
    if hint is None:
        raise HTTPException(
            status_code=404,
            detail="No hint available for this puzzle state"
        )
    
    row, col, value, message = hint
    return {
        "row": row,
        "col": col,
        "value": value,
        "message": message
    }
