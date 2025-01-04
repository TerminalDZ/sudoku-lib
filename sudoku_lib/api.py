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
    title="Sudoku IBA API",
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

@app.options("/{path:path}")
async def options_handler(request: Request):
    return JSONResponse(
        status_code=200,
        content={"detail": "OK"}
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
    response_model=Dict[str, List[List[int]]],
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
        title="Difficulty Level",
        description="The difficulty level of the puzzle (easy, medium, or hard)",
        regex="^(easy|medium|hard)$"
    )
):
    """Generate a new Sudoku puzzle with the specified difficulty level."""
    try:
        sudoku = SudokuGame()
        puzzle = sudoku.new_game(difficulty)
        return {"puzzle": grid_to_list(puzzle)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/solve", tags=["solver"])
async def solve_puzzle(grid: SudokuGrid):
    """Solve a Sudoku puzzle."""
    try:
        solver = SudokuSolver(np.array(grid.grid))
        success, steps = solver.solve()
        if success:
            return {"solution": solver.grid.tolist(), "steps": steps}
        raise HTTPException(status_code=400, detail="No solution exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/hint", tags=["solver"])
async def get_hint(grid: SudokuGrid):
    """Get a hint for the next move in a Sudoku puzzle."""
    try:
        solver = SudokuSolver(np.array(grid.grid))
        hint = solver.get_hint()
        if hint:
            row, col, value, message = hint
            return {
                "row": int(row),
                "column": int(col),
                "value": int(value),
                "message": message
            }
        raise HTTPException(status_code=400, detail="No hints available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/validate", tags=["validation"])
async def validate_solution(grid: SudokuGrid):
    """Validate a Sudoku puzzle solution."""
    try:
        # Convert grid to numpy array
        grid_array = np.array(grid.grid)
        
        # Check if grid is complete (no zeros)
        if 0 in grid_array:
            return {"valid": False, "reason": "Grid is incomplete"}
            
        # Check rows
        for row in grid_array:
            if len(set(row)) != 9:
                return {"valid": False, "reason": "Invalid row"}
                
        # Check columns
        for col in grid_array.T:
            if len(set(col)) != 9:
                return {"valid": False, "reason": "Invalid column"}
                
        # Check 3x3 boxes
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                box = grid_array[i:i+3, j:j+3].flatten()
                if len(set(box)) != 9:
                    return {"valid": False, "reason": "Invalid 3x3 box"}
                    
        return {"valid": True, "reason": "Solution is valid"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
