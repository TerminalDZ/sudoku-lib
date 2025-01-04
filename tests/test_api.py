"""
Tests for the Sudoku API endpoints
"""

import pytest
from fastapi.testclient import TestClient
from sudoku_lib.api import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "endpoints" in data

def test_openapi_documentation():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    
    # Verify API metadata
    assert schema["info"]["title"] == "Sudoku API"
    assert schema["info"]["version"] == "1.0.0"
    assert "description" in schema["info"]
    
    # Verify API tags
    tags = [tag["name"] for tag in schema["tags"]]
    assert "puzzles" in tags
    assert "solver" in tags
    assert "validation" in tags
    
    # Verify endpoints
    paths = schema["paths"]
    assert "/puzzle/{difficulty}" in paths
    assert "/solve" in paths
    assert "/validate" in paths
    assert "/hint" in paths

def test_docs_endpoint():
    response = client.get("/docs")
    assert response.status_code == 200
    assert "swagger" in response.text.lower()

def test_redoc_endpoint():
    response = client.get("/redoc")
    assert response.status_code == 200
    assert "redoc" in response.text.lower()

def test_get_puzzle():
    response = client.get("/puzzle/medium")
    assert response.status_code == 200
    data = response.json()
    assert "puzzle" in data
    assert "difficulty" in data
    assert data["difficulty"] == "medium"
    assert len(data["puzzle"]) == 9
    assert all(len(row) == 9 for row in data["puzzle"])

def test_get_puzzle_invalid_difficulty():
    response = client.get("/puzzle/invalid")
    assert response.status_code == 400
    assert "detail" in response.json()

def test_solve_puzzle():
    puzzle = [
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
    
    response = client.post("/solve", json={"puzzle": puzzle})
    assert response.status_code == 200
    data = response.json()
    assert "solution" in data
    assert "steps" in data
    assert "is_valid" in data
    assert data["is_valid"]

def test_validate_solution():
    # Valid solution
    valid_solution = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9]
    ]
    
    response = client.post("/validate", json={"puzzle": valid_solution})
    assert response.status_code == 200
    data = response.json()
    assert data["is_valid"]
    assert len(data["errors"]) == 0

def test_get_hint():
    puzzle = [
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
    
    response = client.post("/hint", json={"puzzle": puzzle})
    assert response.status_code == 200
    data = response.json()
    assert "row" in data
    assert "col" in data
    assert "value" in data
    assert "message" in data
